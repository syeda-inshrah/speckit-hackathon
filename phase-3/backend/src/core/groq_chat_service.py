"""Direct Groq integration for chat without MCP complexity"""
import json
from typing import List, Dict, Any, Optional
from uuid import UUID
from groq import Groq

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.core.config import settings
from src.models.task import Task


class GroqChatService:
    """Simple Groq chat service with direct task operations"""

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
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
        Run the Groq chat agent with direct task operations

        Args:
            user_message: The user's message
            conversation_history: Previous conversation messages
            user_id: The user's UUID
            session: Database session for task operations
            context: Optional context dictionary

        Returns:
            Dictionary containing the response and tool execution results
        """
        try:
            # Build conversation messages
            messages = []

            # System message with task management capabilities
            system_message = {
                "role": "system",
                "content": """You are a helpful AI assistant for managing todo tasks.
You can help users:
- Create new tasks
- List their tasks
- Mark tasks as complete
- Update task details
- Delete tasks

When a user asks to create a task, extract the task title and description.
When listing tasks, show them in a clear format.
Be conversational and helpful."""
            }
            messages.append(system_message)

            # Add conversation history
            for msg in conversation_history[-10:]:  # Last 10 messages for context
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Call Groq API
            print(f"[Groq] Sending request to {self.model}...")
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
            )

            # Extract response
            assistant_message = chat_completion.choices[0].message.content
            print(f"[Groq] Response received: {len(assistant_message)} characters")

            # Detect task operations from user message
            task_operations = []
            user_message_lower = user_message.lower()

            # Create task - improved detection
            if any(keyword in user_message_lower for keyword in [
                "create task", "add task", "new task", "make a task",
                "create a task", "add a task", "make task"
            ]):
                # Extract task title (improved extraction)
                title = user_message

                # Remove common prefixes
                for prefix in [
                    "create task to ", "add task to ", "new task to ",
                    "create a task to ", "add a task to ", "make a task to ",
                    "create task ", "add task ", "new task ",
                    "create a task ", "add a task ", "make a task "
                ]:
                    if prefix in user_message_lower:
                        idx = user_message_lower.index(prefix)
                        title = user_message[idx + len(prefix):]
                        break

                # Clean up title
                title = title.strip().rstrip('.')

                if title and len(title) > 3:  # Valid title
                    # Create the task
                    new_task = Task(
                        user_id=user_id,
                        title=title,
                        description=f"Created via chat",
                        completed=False
                    )
                    session.add(new_task)
                    await session.commit()
                    await session.refresh(new_task)

                    task_operations.append({
                        "operation": "create_task",
                        "task_id": str(new_task.id),
                        "title": new_task.title,
                        "details": f"Task created successfully"
                    })

                    # Update assistant message to confirm
                    assistant_message = f"✓ I've created the task: '{new_task.title}'\n\nWhat would you like to do next?"
                    print(f"[Groq] Created task: {new_task.title} (ID: {new_task.id})")
                else:
                    assistant_message = "I'd be happy to create a task for you! What would you like the task to be?"

            # List tasks
            elif any(keyword in user_message_lower for keyword in ["list tasks", "show tasks", "my tasks", "what tasks"]):
                result = await session.execute(
                    select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
                )
                tasks = result.scalars().all()

                task_list = []
                for task in tasks:
                    status = "✓" if task.completed else "○"
                    task_list.append(f"{status} {task.title}")

                if task_list:
                    assistant_message = f"Here are your tasks:\n\n" + "\n".join(task_list)
                else:
                    assistant_message = "You don't have any tasks yet. Would you like to create one?"

                task_operations.append({
                    "operation": "list_tasks",
                    "task_id": None,
                    "title": None,
                    "details": f"Found {len(tasks)} tasks"
                })
                print(f"[Groq] Listed {len(tasks)} tasks")

            # Mark complete
            elif any(keyword in user_message_lower for keyword in ["complete", "done", "finish", "mark as complete"]):
                # Try to find task by title mention
                result = await session.execute(
                    select(Task).where(Task.user_id == user_id, Task.completed == False)
                )
                tasks = result.scalars().all()

                if tasks:
                    # Mark first incomplete task as complete (simple logic)
                    task = tasks[0]
                    task.completed = True
                    await session.commit()

                    task_operations.append({
                        "operation": "complete_task",
                        "task_id": str(task.id),
                        "title": task.title,
                        "details": f"Task marked as complete"
                    })
                    assistant_message = f"Great! I've marked '{task.title}' as complete. ✓"
                    print(f"[Groq] Completed task: {task.title}")

            return {
                "content": assistant_message,
                "tool_calls": [],
                "tool_results": task_operations
            }

        except Exception as e:
            print(f"[Groq] Error: {str(e)}")
            raise Exception(f"Groq chat error: {str(e)}")


# Singleton instance
groq_chat_service = GroqChatService()
