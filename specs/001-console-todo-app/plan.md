# Implementation Plan: Phase I - In-Memory Python Console Todo App

**Branch**: 001-console-todo-app | **Date**: 2025-12-01 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from specs/001-console-todo-app/spec.md

**Note**: This template is filled in by `/sp.plan` command. See `.specify/templates/commands/plan.md` for execution workflow.

## Summary

[Extract from feature spec: Primary requirement (create/view/update/delete/mark tasks) + technical approach (in-memory Python console app with clean code structure, type hints, error handling)]

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Built-in libraries only (standard library for in-memory storage and CLI)
**Storage**: In-memory (no persistence between sessions)
**Testing**: pytest (test-driven development required per constitution)
**Target Platform**: Linux/macOS/Windows (console application, platform-agnostic)
**Project Type**: Single project (console app)
**Performance Goals**: Instant user feedback (operations complete in <100ms), fast task list rendering (<50ms for up to 50 tasks)
**Constraints**: Must use UV package manager, no external dependencies preferred, type hints required on all functions/methods
**Scale/Scope**: Single user session, supports unlimited tasks during session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined based on constitution file]

- Python 3.13+ requirement: PASS - Specified as Python 3.13+ in requirements
- Type hints requirement: PASS - Constitution requires type hints
- Clean code principles: PASS - Constitution requires clean code structure
- Spec-driven development: PASS - Following Spec-Kit workflow (Specify → Plan → Tasks → Implement)
- In-memory storage: PASS - Spec requires in-memory storage for Phase I
- No manual coding: PASS - Constitution requires Claude Code implementation only
- Error handling: PASS - Spec requires graceful error handling

**All gates passed** - No constitution violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py          # Task data model with type hints
├── services/
│   ├── task_manager.py  # In-memory task storage and operations
│   └── cli_interface.py # Command-line interface handler
├── cli/
│   ├── main.py           # Application entry point
│   └── menu.py           # Menu display and navigation
└── lib/
    └── validators.py     # Input validation utilities

tests/
├── contract/
│   └── test_task_operations.py    # Test all task operations
├── integration/
│   └── test_cli_workflows.py       # Test complete user workflows
└── unit/
    ├── test_task_manager.py           # Test task storage logic
    ├── test_validators.py            # Test input validation
    └── test_cli_interface.py          # Test CLI components
```

**Structure Decision**: Single project structure selected as this is Phase I console application. The layout separates concerns: models (data), services (business logic), cli (presentation), and lib (utilities). Tests are organized by type (contract, integration, unit). All code uses type hints and follows clean code principles per constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|

No violations detected - Constitution check passed successfully.

---

## Phase 0: Research

[No NEEDS CLARIFICATION markers in Technical Context - skipping Phase 0 research]

**Research**: All technical decisions are well-defined in specification and constitution. Python standard library provides all needed functionality (dict, list, datetime, input/output). No external dependencies or research required for this phase.

---

## Phase 1: Design & Contracts

**Prerequisites:** Phase 0 complete (no research needed)

### 1. Data Model Design

**Entity**: Task

**Fields**:
- `id: int` - Unique sequential identifier (auto-incrementing)
- `title: str` - Required, 1-200 characters, non-empty
- `description: str | None` - Optional, up to 1000 characters
- `completed: bool` - Default False, toggleable
- `created_at: datetime` - Auto-assigned on creation

**Validation Rules** (from FR-009, FR-010):
- ID must exist in task list
- ID must be numeric
- Title cannot be empty or whitespace-only
- Title max 200 characters
- Description max 1000 characters (if provided)

**State Transitions**: None required (no workflow beyond CRUD)

---

### 2. CLI Interface Contracts

**File**: `src/cli/menu.py` and `src/cli/main.py`

**Menu Structure** (from FR-001):
```text
=== Todo App ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Choice [1-6]: _
```

**Input Prompts** (per operation):
- Add Task: "Enter task title: ", "Enter task description (optional, press Enter to skip): "
- Update Task: "Enter task ID to update: ", "Enter new title (press Enter to keep current): ", "Enter new description (press Enter to keep current): "
- Delete Task: "Enter task ID to delete: ", "Confirm deletion? (y/n): "
- Mark Complete: "Enter task ID to toggle status: "

**Feedback Messages** (from FR-011):
- Success: "Task [ID] [action] successfully" or "[action] completed"
- Error: "Task not found", "Invalid task ID", "Title cannot be empty"
- Cancellation: "Deletion cancelled", "Update cancelled"
- Empty list: "No tasks found"

---

### 3. Service Layer Contracts

**File**: `src/services/task_manager.py`

**Class**: `TaskManager`

**Methods** (with type hints):
```python
class TaskManager:
    def __init__(self) -> None
    def add_task(self, title: str, description: Optional[str]) -> Task
    def get_task(self, task_id: int) -> Optional[Task]
    def get_all_tasks(self) -> List[Task]
    def update_task(self, task_id: int, title: Optional[str], description: Optional[str]) -> bool
    def delete_task(self, task_id: int) -> bool
    def toggle_complete(self, task_id: int) -> bool
    def task_exists(self, task_id: int) -> bool
```

**Implementation Notes**:
- Use `List[Task]` for in-memory storage
- Auto-increment task IDs (counter starting at 1)
- Return `Task` objects from all methods for validation
- Handle edge cases: non-existent ID, empty input

---

## Complexity Tracking

No complexity issues requiring tradeoffs. Design follows clean code principles and constitutional requirements.

---

## Additional Sections (Not Required for Phase I)

### API Endpoints
Not applicable - Phase I is a console application with no API.

### External Integrations
Not applicable - Phase I uses no external services.

### Deployment Strategy
Not applicable - Phase I is a local console application.

### Testing Strategy
See Test Plan section below.

---

## Testing Strategy

### Contract Tests

**File**: `tests/contract/test_task_operations.py`

**Test Cases** (per functional requirement):
```python
def test_add_task_creates_with_unique_id():
    # Verify: New task gets sequential ID, defaults to incomplete

def test_add_task_validates_title():
    # Verify: Empty/whitespace title rejected

def test_get_task_by_id():
    # Verify: Retrieve task by correct ID returns Task object

def test_get_task_nonexistent_id():
    # Verify: Non-existent ID returns None

def test_update_task_fields():
    # Verify: Title/description fields update correctly

def test_delete_task_requires_confirmation():
    # Verify: Task removed only after confirmation

def test_toggle_complete_switches_status():
    # Verify: Complete/Incomplete status toggles
```

---

### Integration Tests

**File**: `tests/integration/test_cli_workflows.py`

**User Workflows** (per user stories):

**Story 1 - Create and View Tasks (P1)**:
```python
def test_create_task_and_view_list():
    # Given: Empty task list
    # When: User adds task "Buy groceries"
    # Then: Task appears in list view with ID and status
```

**Story 2 - Mark Complete/Incomplete (P2)**:
```python
def test_mark_complete_and_toggle_back():
    # Given: Task exists with incomplete status
    # When: User marks task complete
    # Then: Status updates to complete, displays in list view
    # When: User marks same task complete again
    # Then: Status toggles back to incomplete
```

**Story 3 - Update Task Details (P2)**:
```python
def test_update_task_title_description():
    # Given: Task exists with title and description
    # When: User updates title field
    # Then: Only title changes, description preserved
```

**Story 4 - Delete Tasks (P3)**:
```python
def test_delete_with_confirmation():
    # Given: Task exists
    # When: User deletes and confirms
    # Then: Task removed from list
    # When: User deletes without confirmation
    # Then: Task NOT removed
```

---

### Unit Tests

**Files**:
- `tests/unit/test_task_manager.py`
- `tests/unit/test_validators.py`
- `tests/unit/test_cli_interface.py`

**Coverage Goals** (TDD):
- Task storage logic: 100% code coverage
- Input validation: 100% coverage of validation rules
- CLI components: 90%+ coverage of menu display/navigation

---

## Next Steps

After this plan is approved, proceed to:
1. `/sp.tasks` - Generate actionable tasks from this plan
2. `/sp.implement` - Execute tasks to implement Phase I console app
3. Create quickstart guide for developers

---

**Plan Status**: Complete - Ready for task breakdown

**Constitution Compliance**: All checks passed ✅
