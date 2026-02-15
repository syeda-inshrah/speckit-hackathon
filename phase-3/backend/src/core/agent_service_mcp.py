"""OpenAI Agents SDK service with MCP Server integration"""
import json
import asyncio
from typing import List, Dict, Any, Optional
from uuid import UUID

from agents import Agent, Runner, function_tool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import settings


class MCPAgentService:
    """Service for managing OpenAI Agents SDK with MCP Server backend"""

    def __init__(self):
        self.agent_name = settings.AGENT_NAME
        self.agent_instructions = settings.AGENT_INSTRUCTIONS
        self.model = settings.OPENROUTER_MODEL
        self.agent = None
        self.mcp_session: Optional[ClientSession] = None
        self.mcp_tools = []
        self.openai_tools = []

    async def initialize_mcp_connection(self):
        """Initialize connection to MCP server"""
        if self.mcp_session is not None:
            return  # Already connected

        # Configure MCP server parameters - use virtual environment Python
        import sys
        import os

        # Get the virtual environment's Python executable
        python_executable = sys.executable

        # Set up environment to include the project root in PYTHONPATH
        env = os.environ.copy()
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        env["PYTHONPATH"] = project_root

        server_params = StdioServerParameters(
            command=python_executable,
            args=["-m", "src.mcp_server.server"],
            env=env
        )

        # Connect to MCP server
        try:
            # Note: We need to keep the connection alive, so we'll store the context managers
            self.read_stream, self.write_stream = await stdio_client(server_params).__aenter__()
            self.mcp_session = await ClientSession(self.read_stream, self.write_stream).__aenter__()

            # Initialize the session
            await self.mcp_session.initialize()

            # Get available tools from MCP server
            tools_response = await self.mcp_session.list_tools()
            self.mcp_tools = tools_response.tools if hasattr(tools_response, 'tools') else []

            # Convert MCP tools to OpenAI function format
            self._convert_mcp_tools_to_openai()

            print(f"[MCP] Server connected. Available tools: {[t.name for t in self.mcp_tools]}")

        except Exception as e:
            print(f"[MCP] Failed to connect to MCP server: {str(e)}")
            raise

    def _convert_mcp_tools_to_openai(self):
        """Convert MCP tools to OpenAI Agents SDK function tools"""
        self.openai_tools = []

        for mcp_tool in self.mcp_tools:
            # Create a wrapper function for each MCP tool using a factory
            wrapper = self._create_mcp_tool_wrapper(
                mcp_tool.name,
                mcp_tool.description
            )
            self.openai_tools.append(wrapper)

    def _create_mcp_tool_wrapper(self, tool_name: str, tool_description: str):
        """Factory function to create MCP tool wrapper with proper closure"""

        @function_tool
        async def mcp_tool_wrapper(**kwargs) -> dict:
            """Wrapper that routes calls to MCP server"""
            try:
                # Call the MCP server tool
                result = await self.mcp_session.call_tool(
                    name=tool_name,  # Captured from factory parameter
                    arguments=kwargs
                )

                # Extract text content from MCP response
                if result and len(result.content) > 0:
                    content = result.content[0]
                    if hasattr(content, 'text'):
                        return json.loads(content.text)

                return {"success": False, "message": "No response from MCP server"}

            except Exception as e:
                return {
                    "success": False,
                    "message": f"MCP tool execution error: {str(e)}"
                }

        # Set the function metadata
        mcp_tool_wrapper.__name__ = tool_name
        mcp_tool_wrapper.__doc__ = tool_description

        return mcp_tool_wrapper

    async def _initialize_agent(self):
        """Initialize the agent with MCP-backed tools"""
        if self.agent is None:
            # Ensure MCP connection is established
            await self.initialize_mcp_connection()

            # Set OpenAI API configuration based on selected provider
            import os

            if settings.LLM_PROVIDER.upper() == "GROQ":
                # Use Groq API (OpenAI-compatible)
                os.environ["OPENAI_API_KEY"] = settings.GROQ_API_KEY
                os.environ["OPENAI_BASE_URL"] = settings.GROQ_BASE_URL
                self.model = settings.GROQ_MODEL
                print(f"[MCP] Using Groq API with model: {self.model}")
            else:
                # Default to OpenRouter API (OpenAI-compatible)
                os.environ["OPENAI_API_KEY"] = settings.OPENROUTER_API_KEY
                os.environ["OPENAI_BASE_URL"] = settings.OPENROUTER_BASE_URL
                self.model = settings.OPENROUTER_MODEL
                print(f"[MCP] Using OpenRouter API with model: {self.model}")

            # Create the agent with MCP-backed function tools
            self.agent = Agent(
                name=self.agent_name,
                instructions=self.agent_instructions,
                model=self.model,
                tools=self.openai_tools
            )

            print(f"[MCP] Agent initialized with {len(self.openai_tools)} MCP-backed tools")

    async def run_agent(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        user_id: UUID,
        session: AsyncSession,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run the agent with OpenAI Agents SDK and MCP tools

        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages
            user_id: The user's UUID (passed to tools via MCP)
            session: Database session (not used directly, MCP server handles DB)
            context: Optional context dictionary

        Returns:
            Dictionary containing the response and tool execution results
        """
        try:
            # Ensure agent is initialized with MCP connection
            await self._initialize_agent()

            # Build the conversation messages
            messages = []
            for msg in conversation_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            # Add the current user message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Prepare context (user_id will be passed to MCP tools via arguments)
            agent_context = context or {}
            agent_context["user_id"] = str(user_id)

            # Run the agent with Runner
            result = await Runner.run(
                starting_agent=self.agent,
                input=messages,
                context=agent_context
            )

            # Extract response from Result
            response_data = {
                "content": "",
                "tool_calls": [],
                "tool_results": []
            }

            # Get the final output
            if hasattr(result, "final_output"):
                response_data["content"] = result.final_output
            elif hasattr(result, "output"):
                response_data["content"] = result.output

            # Extract tool calls from result items
            if hasattr(result, "items"):
                for item in result.items:
                    # Check if this is a tool call item
                    if hasattr(item, "tool_name"):
                        response_data["tool_calls"].append({
                            "function": {
                                "name": item.tool_name,
                                "arguments": getattr(item, "tool_input", {})
                            }
                        })

                        # Check if there's a tool result
                        if hasattr(item, "tool_output"):
                            response_data["tool_results"].append({
                                "result": item.tool_output
                            })

            return response_data

        except Exception as e:
            raise Exception(f"Agent execution error: {str(e)}")

    async def cleanup(self):
        """Clean up MCP connection"""
        if self.mcp_session:
            try:
                await self.mcp_session.__aexit__(None, None, None)
                await self.write_stream.__aexit__(None, None, None)
                print("✅ MCP connection closed")
            except Exception as e:
                print(f"⚠️ Error closing MCP connection: {str(e)}")


# Singleton instance
mcp_agent_service = MCPAgentService()
