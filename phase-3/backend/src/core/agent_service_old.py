"""OpenAI Agents SDK service layer for AI-powered chat functionality"""
from openai import OpenAI
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.core.config import settings
import json


# Define MCP Tools using Pydantic schemas
class AddTaskInput(BaseModel):
    """Input schema for adding a task"""
    title: str = Field(..., description="The title of the task")
    description: Optional[str] = Field(None, description="Optional description of the task")


class ListTasksInput(BaseModel):
    """Input schema for listing tasks"""
    completed: Optional[bool] = Field(None, description="Filter by completion status (true for completed, false for incomplete, omit for all)")


class CompleteTaskInput(BaseModel):
    """Input schema for completing a task"""
    task_id: int = Field(..., description="The ID of the task to complete")


class UpdateTaskInput(BaseModel):
    """Input schema for updating a task"""
    task_id: int = Field(..., description="The ID of the task to update")
    title: Optional[str] = Field(None, description="New title for the task")
    description: Optional[str] = Field(None, description="New description for the task")


class DeleteTaskInput(BaseModel):
    """Input schema for deleting a task"""
    task_id: int = Field(..., description="The ID of the task to delete")


class AgentService:
    """Service for managing OpenAI Agents SDK with OpenRouter"""

    def __init__(self):
        # Initialize OpenAI client with OpenRouter configuration
        self.client = OpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL
        )
        self.model = settings.OPENROUTER_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE

    def get_agent_instructions(self) -> str:
        """Get the agent instructions"""
        return settings.AGENT_INSTRUCTIONS

    def get_tools_definition(self) -> List[Dict[str, Any]]:
        """Get MCP tools definition for OpenAI function calling"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task for the user",
                    "parameters": AddTaskInput.model_json_schema()
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks, optionally filtered by completion status",
                    "parameters": ListTasksInput.model_json_schema()
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": CompleteTaskInput.model_json_schema()
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update a task's title or description",
                    "parameters": UpdateTaskInput.model_json_schema()
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": DeleteTaskInput.model_json_schema()
                }
            }
        ]

    async def run_agent(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Run the agent with OpenRouter

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            tools: Optional list of tool definitions for function calling

        Returns:
            Dictionary containing the response and any tool calls
        """
        try:
            # Add system message with agent instructions if not present
            if not messages or messages[0].get("role") != "system":
                messages.insert(0, {
                    "role": "system",
                    "content": self.get_agent_instructions()
                })

            # Prepare the request
            request_params = {
                "model": self.model,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                # OpenRouter-specific headers
                "extra_headers": {
                    "HTTP-Referer": settings.FRONTEND_URL,
                    "X-Title": "Todo AI Assistant"
                }
            }

            # Add tools if provided
            if tools:
                request_params["tools"] = tools
                request_params["tool_choice"] = "auto"

            # Make the API call
            response = self.client.chat.completions.create(**request_params)

            # Extract the response
            message = response.choices[0].message

            result = {
                "content": message.content,
                "role": message.role,
                "tool_calls": []
            }

            # Extract tool calls if present
            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tool_call in message.tool_calls:
                    result["tool_calls"].append({
                        "id": tool_call.id,
                        "type": tool_call.type,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": json.loads(tool_call.function.arguments)
                        }
                    })

            return result

        except Exception as e:
            raise Exception(f"Agent execution error: {str(e)}")

    async def run_with_tools(
        self,
        messages: List[Dict[str, str]],
        tool_executor: Any
    ) -> Dict[str, Any]:
        """
        Run the agent with automatic tool execution

        Args:
            messages: List of message dictionaries
            tool_executor: Function to execute tools

        Returns:
            Final agent response after tool execution
        """
        tools = self.get_tools_definition()

        # Initial agent call
        response = await self.run_agent(messages, tools)

        # If no tool calls, return response
        if not response.get("tool_calls"):
            return response

        # Execute tools and get final response
        tool_results = []
        for tool_call in response["tool_calls"]:
            function_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]

            # Execute the tool
            result = await tool_executor(function_name, arguments)
            tool_results.append({
                "tool_call_id": tool_call["id"],
                "result": result
            })

        # Add assistant message with tool calls
        messages.append({
            "role": "assistant",
            "content": response.get("content") or "",
            "tool_calls": response["tool_calls"]
        })

        # Add tool results
        for tool_result in tool_results:
            messages.append({
                "role": "tool",
                "tool_call_id": tool_result["tool_call_id"],
                "content": json.dumps(tool_result["result"])
            })

        # Get final response
        final_response = await self.run_agent(messages, tools=None)

        return {
            "content": final_response.get("content", ""),
            "tool_calls": response["tool_calls"],
            "tool_results": tool_results
        }


# Singleton instance
agent_service = AgentService()
