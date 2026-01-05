"""CLI interface handler for console todo application.

Coordinates between user input and service layer.
"""

from typing import Dict, Any


class CLIInterface:
    """Handles CLI menu, user input, and command routing."""

    def __init__(self, task_manager: Any) -> None:
        """
        Initialize CLI interface.

        Args:
            task_manager: TaskManager instance for service operations
        """
        self.task_manager = task_manager

    def display_menu(self) -> None:
        """
        Display main menu with 6 options.
        """
        print("\n=== Todo App ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Complete/Incomplete")
        print("6. Exit")
        print("\nChoice [1-6]: ", end="")

    def get_user_choice(self) -> int:
        """
        Get and validate user's menu choice.

        Returns:
            Valid integer 1-6
        """
        while True:
            try:
                choice = input().strip()
                if choice.isdigit() and 1 <= int(choice) <= 6:
                    return int(choice)
                print("Invalid choice. Please enter a number between 1 and 6.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return -1

    def handle_add_task(self) -> Dict[str, Any]:
        """
        Handle Add Task workflow.
        """
        print("\n--- Add Task ---")
        title = input("Enter task title: ").strip()
        description = input("Enter task description (optional, press Enter to skip): ").strip()
        description = None if not description else description

        result = self.task_manager.add_task(title, description)
        print(f"\n{result['message']}")

        return result

    def handle_view_tasks(self) -> Dict[str, Any]:
        """
        Handle View Tasks workflow.
        """
        print("\n--- View Tasks ---")

        tasks = self.task_manager.get_all_tasks()

        if not tasks:
            print("No tasks found")
            return {"status": "info", "message": "No tasks found"}

        self._display_tasks(tasks)

        return {"status": "success", "tasks": tasks}

    def handle_update_task(self) -> Dict[str, Any]:
        """
        Handle Update Task workflow.
        """
        print("\n--- Update Task ---")

        task_id_str = input("Enter task ID to update: ").strip()
        if not task_id_str.isdigit():
            print("Invalid task ID")
            return {"status": "error", "message": "Invalid task ID"}

        task_id = int(task_id_str)

        task = self.task_manager.get_task(task_id)
        if task is None:
            print("Task not found")
            return {"status": "error", "message": "Task not found"}

        print(f"Current: {task['title']}")
        print(f"Description: {task['description'] or 'N/A'}")

        title = input("Enter new title (press Enter to keep current): ").strip()
        description = input("Enter new description (press Enter to keep current): ").strip()
        description = None if not description else description

        if not title:
            title = None

        result = self.task_manager.update_task(task_id, title=title, description=description)
        print(f"\n{result['message']}")

        return result

    def handle_delete_task(self) -> Dict[str, Any]:
        """
        Handle Delete Task workflow.
        """
        print("\n--- Delete Task ---")

        task_id_str = input("Enter task ID to delete: ").strip()
        if not task_id_str.isdigit():
            print("Invalid task ID")
            return {"status": "error", "message": "Invalid task ID"}

        task_id = int(task_id_str)

        task = self.task_manager.get_task(task_id)
        if task is None:
            print("Task not found")
            return {"status": "error", "message": "Task not found"}

        print(f"Task: {task['title']}")
        confirmation = input("Confirm deletion? (y/n): ").strip().lower()

        if confirmation != "y":
            print("Deletion cancelled")
            return {"status": "cancelled", "message": "Deletion cancelled"}

        result = self.task_manager.delete_task(task_id)
        print(f"\n{result['message']}")

        return result

    def handle_mark_complete(self) -> Dict[str, Any]:
        """
        Handle Mark Complete/Incomplete workflow.
        """
        print("\n--- Mark Complete/Incomplete ---")

        task_id_str = input("Enter task ID to mark: ").strip()
        if not task_id_str.isdigit():
            print("Invalid task ID")
            return {"status": "error", "message": "Invalid task ID"}

        task_id = int(task_id_str)

        task = self.task_manager.get_task(task_id)
        if task is None:
            print("Task not found")
            return {"status": "error", "message": "Task not found"}

        current_status = "completed" if task["completed"] else "incomplete"
        print(f"Current status: {current_status}")

        result = self.task_manager.toggle_complete(task_id)
        print(f"\n{result['message']}")

        return result

    def _display_tasks(self, tasks: list) -> None:
        """Display task list with status indicators."""
        if not tasks:
            return

        print("\n" + "=" * 60)
        print(f"{'ID':<5} {'Status':<10} {'Title':<40} {'Created At':>20}")
        print("=" * 60)

        for task in tasks:
            status = "✓" if task["completed"] else "✗"
            created_at = task["created_at"].strftime("%Y-%m-%d %H:%M")
            title = task["title"][:37]
            description = task["description"][:37] if task["description"] else ""

            print(f"{task['id']:<5} {status:<10} {title:<40} {description:<40} {created_at:>20}")
