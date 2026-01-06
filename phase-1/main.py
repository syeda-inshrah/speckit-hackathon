# Main entry point for console todo application
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.task_manager import TaskManager
from services.cli_interface import CLIInterface


def main():
    """Run to console todo application."""
    task_manager = TaskManager()
    cli_interface = CLIInterface(task_manager)

    while True:
        cli_interface.display_menu()
        choice = cli_interface.get_user_choice()

        if choice == -1:
            task_manager._save_tasks()
            print("\nExiting...")
            return 0
        elif choice == 6:
            task_manager._save_tasks()
            print("\nGoodbye!")
            return 0
        elif choice == 1:
            cli_interface.handle_add_task()
        elif choice == 2:
            cli_interface.handle_view_tasks()
        elif choice == 3:
            cli_interface.handle_update_task()
        elif choice == 4:
            cli_interface.handle_delete_task()
        elif choice == 5:
            cli_interface.handle_mark_complete()

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    exit(main())
