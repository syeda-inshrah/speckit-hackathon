# Quickstart Guide: Phase I - Console Todo App

**Date**: 2025-12-01
**Purpose**: Get developers started quickly with Phase I console todo app

## Prerequisites

- Python 3.13+ installed
- UV package manager installed
- Basic Python knowledge

## Installation

```bash
# Clone repository (if applicable)
git clone <repo-url>
cd hackathon-02

# Install dependencies with UV
uv pip install pytest

# Verify installation
python --version
pytest --version
```

## Project Structure

```
src/
├── models/
│   └── task.py          # Task data model
├── services/
│   ├── task_manager.py  # Task storage and operations
│   └── cli_interface.py # CLI handler
├── cli/
│   ├── main.py           # Application entry
│   └── menu.py           # Menu display
└── lib/
    └── validators.py     # Input validation
```

## Running the Application

```bash
# Run console app
python src/cli/main.py

# Or with UV
uv run python src/cli/main.py
```

## Workflow Example

```text
=== Todo App ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Choice [1-6]: 1

Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): Milk, eggs, bread

Task created successfully! Task ID: 1
```

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/contract/test_task_operations.py

# Run with coverage
pytest --cov=src --cov-report=html tests/
```

## Development Tips

1. **Type Hints Required**: All functions and classes must include proper type hints
2. **Clean Code**: Follow PEP 8 guidelines, use descriptive names
3. **Error Handling**: All user input must be validated and provide clear feedback
4. **TDD Workflow**: Write test first, then implement to make it pass

## Next Steps

1. Review `plan.md` for detailed architecture
2. Run `/sp.tasks` to get task breakdown
3. Run `/sp.implement` to execute implementation
```
