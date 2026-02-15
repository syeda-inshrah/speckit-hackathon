"""Groq Agent with MCP Tool Integration"""
import json
import re
from typing import List, Dict, Any, Optional
from uuid import UUID
from groq import Groq

from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import settings
from src.mcp_server.server import (
    _add_task,
    _list_tasks,
    _complete_task,
    _update_task,
    _delete_task
)


class GroqMCPAgent:
    """Groq Agent that uses MCP tools for task operations"""

    def __init__(self):
        self.client = Groq(
            api_key=settings.GROQ_API_KEY,
            base_url=settings.GROQ_BASE_URL
        )
        self.model = settings.GROQ_MODEL

    async def run_agent(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        user_id: UUID,
        session: AsyncSession,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run Groq agent with MCP tool integration

        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages
            user_id: The user's UUID
            session: Database session for MCP tools
            context: Optional context dictionary

        Returns:
            Dictionary containing the response and tool execution results
        """
        try:
            # Step 1: Analyze user intent with Groq
            intent_analysis = await self._analyze_intent(user_message, conversation_history)

            # Step 2: Execute MCP tools based on intent
            tool_results = await self._execute_mcp_tools(
                intent_analysis,
                user_id,
                session
            )

            # Step 3: Generate natural language response
            final_response = await self._generate_response(
                user_message,
                conversation_history,
                tool_results
            )

            return {
                "content": final_response,
                "tool_calls": intent_analysis.get("tools", []),
                "tool_results": tool_results
            }

        except Exception as e:
            print(f"[GroqMCP] Error: {str(e)}")
            return {
                "content": "I apologize, but I encountered an error processing your request. Please try again.",
                "tool_calls": [],
                "tool_results": []
            }

    async def _analyze_intent(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Analyze user intent and determine which MCP tools to call"""

        # Build messages for intent analysis
        messages = [
            {
                "role": "system",
                "content": """You are an intent analyzer for a todo task management system.
Analyze the user's message and determine which MCP tool(s) to call.

Available MCP Tools:
1. add_task - Create a new task (requires: title, optional: description)
2. list_tasks - List tasks (optional: completed filter)
3. complete_task - Mark task as complete (requires: task_id)
4. update_task - Update task (requires: task_id, optional: title, description)
5. delete_task - Delete task (requires: task_id)

Respond with JSON in this format:
{
  "intent": "create_task|list_tasks|complete_task|update_task|delete_task|general_chat",
  "tool": "add_task|list_tasks|complete_task|update_task|delete_task|null",
  "parameters": {
    "title": "extracted title",
    "description": "extracted description",
    "task_id": "extracted task id",
    "completed": true/false/null
  },
  "confidence": 0.0-1.0
}

Examples:
- "Add a task to buy groceries" -> {"intent": "create_task", "tool": "add_task", "parameters": {"title": "buy groceries"}}
- "Show me all my tasks" -> {"intent": "list_tasks", "tool": "list_tasks", "parameters": {"completed": null}}
- "Mark task 5 as done" -> {"intent": "complete_task", "tool": "complete_task", "parameters": {"task_id": 5}}
"""
            }
        ]

        # Add recent conversation context
        for msg in conversation_history[-3:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        messages.append({
            "role": "user",
            "content": f"Analyze this message: {user_message}"
        })

        # Call Groq for intent analysis
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            temperature=0.3,  # Lower temperature for more consistent intent detection
            max_tokens=500,
        )

        response_text = response.choices[0].message.content

        # Extract JSON from response
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                intent_data = json.loads(json_match.group())
            else:
                # Fallback to simple keyword matching
                intent_data = self._fallback_intent_detection(user_message)
        except json.JSONDecodeError:
            intent_data = self._fallback_intent_detection(user_message)

        print(f"[GroqMCP] Intent detected: {intent_data.get('intent')}")
        return intent_data

    def _fallback_intent_detection(self, user_message: str) -> Dict[str, Any]:
        """Simple keyword-based intent detection as fallback"""
        msg_lower = user_message.lower()

        # Create task
        if any(kw in msg_lower for kw in ["add task", "create task", "new task", "make a task"]):
            # Extract title
            title = user_message
            for prefix in ["add task to ", "create task to ", "new task to ", "add task ", "create task ", "new task "]:
                if prefix in msg_lower:
                    idx = msg_lower.index(prefix)
                    title = user_message[idx + len(prefix):].strip()
                    break

            return {
                "intent": "create_task",
                "tool": "add_task",
                "parameters": {"title": title},
                "confidence": 0.8
            }

        # List tasks
        elif any(kw in msg_lower for kw in ["list tasks", "show tasks", "my tasks", "what tasks", "all tasks"]):
            return {
                "intent": "list_tasks",
                "tool": "list_tasks",
                "parameters": {"completed": None},
                "confidence": 0.9
            }

        # Complete task
        elif any(kw in msg_lower for kw in ["complete", "done", "finish", "mark as complete"]):
            # Try to extract task ID
            task_id_match = re.search(r'task\s+(\d+)', msg_lower)
            if task_id_match:
                return {
                    "intent": "complete_task",
                    "tool": "complete_task",
                    "parameters": {"task_id": int(task_id_match.group(1))},
                    "confidence": 0.85
                }
            return {
                "intent": "complete_task",
                "tool": "complete_task",
                "parameters": {},
                "confidence": 0.5
            }

        # Delete task
        elif any(kw in msg_lower for kw in ["delete", "remove", "cancel task"]):
            task_id_match = re.search(r'task\s+(\d+)', msg_lower)
            if task_id_match:
                return {
                    "intent": "delete_task",
                    "tool": "delete_task",
                    "parameters": {"task_id": int(task_id_match.group(1))},
                    "confidence": 0.85
                }
            return {
                "intent": "delete_task",
                "tool": "delete_task",
                "parameters": {},
                "confidence": 0.5
            }

        # General chat
        return {
            "intent": "general_chat",
            "tool": None,
            "parameters": {},
            "confidence": 0.7
        }

    async def _execute_mcp_tools(
        self,
        intent_analysis: Dict[str, Any],
        user_id: UUID,
        session: AsyncSession
    ) -> List[Dict[str, Any]]:
        """Execute MCP tools based on intent analysis"""

        tool_name = intent_analysis.get("tool")
        parameters = intent_analysis.get("parameters", {})

        if not tool_name:
            return []

        results = []
        user_id_str = str(user_id)

        try:
            if tool_name == "add_task":
                title = parameters.get("title", "").strip()
                description = parameters.get("description")

                if title:
                    result = await _add_task(
                        session=session,
                        user_id=user_id_str,
                        title=title,
                        description=description
                    )
                    results.append({
                        "tool": "add_task",
                        "result": result
                    })
                    print(f"[GroqMCP] MCP Tool: add_task -> {result.get('message')}")

            elif tool_name == "list_tasks":
                completed = parameters.get("completed")
                result = await _list_tasks(
                    session=session,
                    user_id=user_id_str,
                    completed=completed
                )
                results.append({
                    "tool": "list_tasks",
                    "result": result
                })
                print(f"[GroqMCP] MCP Tool: list_tasks -> {result.get('message')}")

            elif tool_name == "complete_task":
                task_id = parameters.get("task_id")
                if task_id:
                    result = await _complete_task(
                        session=session,
                        user_id=user_id_str,
                        task_id=task_id
                    )
                    results.append({
                        "tool": "complete_task",
                        "result": result
                    })
                    print(f"[GroqMCP] MCP Tool: complete_task -> {result.get('message')}")

            elif tool_name == "update_task":
                task_id = parameters.get("task_id")
                title = parameters.get("title")
                description = parameters.get("description")

                if task_id:
                    result = await _update_task(
                        session=session,
                        user_id=user_id_str,
                        task_id=task_id,
                        title=title,
                        description=description
                    )
                    results.append({
                        "tool": "update_task",
                        "result": result
                    })
                    print(f"[GroqMCP] MCP Tool: update_task -> {result.get('message')}")

            elif tool_name == "delete_task":
                task_id = parameters.get("task_id")
                if task_id:
                    result = await _delete_task(
                        session=session,
                        user_id=user_id_str,
                        task_id=task_id
                    )
                    results.append({
                        "tool": "delete_task",
                        "result": result
                    })
                    print(f"[GroqMCP] MCP Tool: delete_task -> {result.get('message')}")

        except Exception as e:
            print(f"[GroqMCP] Tool execution error: {str(e)}")
            results.append({
                "tool": tool_name,
                "result": {
                    "success": False,
                    "message": f"Error executing tool: {str(e)}"
                }
            })

        return results

    async def _generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        tool_results: List[Dict[str, Any]]
    ) -> str:
        """Generate natural language response based on tool results"""

        if not tool_results:
            # No tools executed, generate general response
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful AI assistant for managing todo tasks.
Be conversational and friendly. Help users understand what you can do."""
                }
            ]

            for msg in conversation_history[-5:]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            messages.append({
                "role": "user",
                "content": user_message
            })

            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
                max_tokens=300,
            )

            return response.choices[0].message.content

        # Generate response based on tool results
        tool_summaries = []
        for tool_exec in tool_results:
            tool_name = tool_exec["tool"]
            result = tool_exec["result"]

            if result.get("success"):
                if tool_name == "add_task":
                    tool_summaries.append(f"✓ Created task: '{result.get('title')}'")
                elif tool_name == "list_tasks":
                    tasks = result.get("tasks", [])
                    if tasks:
                        task_list = "\n".join([
                            f"{'✓' if t['completed'] else '○'} Task {t['id']}: {t['title']}"
                            for t in tasks
                        ])
                        tool_summaries.append(f"Here are your tasks:\n{task_list}")
                    else:
                        tool_summaries.append("You don't have any tasks yet.")
                elif tool_name == "complete_task":
                    tool_summaries.append(f"✓ Completed task: '{result.get('title')}'")
                elif tool_name == "update_task":
                    tool_summaries.append(f"✓ Updated task: '{result.get('title')}'")
                elif tool_name == "delete_task":
                    tool_summaries.append(f"✓ Deleted task")
            else:
                tool_summaries.append(f"⚠ {result.get('message', 'Operation failed')}")

        return "\n\n".join(tool_summaries) if tool_summaries else "I've processed your request."


# Lazy initialization - create instance only when needed
_groq_mcp_agent_instance = None

def get_groq_mcp_agent() -> GroqMCPAgent:
    """Get or create the GroqMCPAgent singleton instance"""
    global _groq_mcp_agent_instance
    if _groq_mcp_agent_instance is None:
        _groq_mcp_agent_instance = GroqMCPAgent()
    return _groq_mcp_agent_instance

# For backward compatibility
groq_mcp_agent = None  # Will be initialized on first use
