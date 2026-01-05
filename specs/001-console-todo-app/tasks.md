# Tasks: Phase I - In-Memory Python Console Todo App

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

---

# Tasks

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools
- [ ] T004 [P] Create placeholder files for all planned source files

**Purpose**: Project initialization and basic structure

**Dependencies**: None - can proceed immediately

**Files Created**:
- `src/models/task.py`
- `src/services/task_manager.py`
- `src/services/cli_interface.py`
- `src/cli/main.py`
- `src/cli/menu.py`
- `src/lib/validators.py`
- `tests/contract/`
- `tests/integration/`
- `tests/unit/`

---

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T004 Setup database schema and migrations framework
- [ ] T005 [P] Implement authentication/authorization framework
- [ ] T006 [P] Setup API routing and middleware structure
- [ ] T007 Create base models/entities that all stories depend on
- [ ] T008 Configure error handling and logging infrastructure
- [ ] T009 Setup environment configuration management

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**Critical**: No user story work can begin until this phase is complete

---

## Phase 3: User Story 1 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]
Users can create new tasks and view them in a list format through a console interface.

**Independent Test**: [How to verify this story works on its own]
Can be fully tested by creating tasks and verifying they appear in list, delivering immediate value as a simple task tracker even without update/delete capabilities.

### Tests for User Story 1 (OPTIONAL ⚠️)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for Add Task in tests/contract/test_add_task.py
- [ ] T011 [P] [US1] Contract test for View Tasks in tests/contract/test_view_tasks.py
- [ ] T012 [P] [US1] Integration test for Create and View workflow in tests/integration/test_create_view.py

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create Task entity model in src/models/task.py with type hints
- [ ] T013 [P] [US1] Create Task entity model in src/models/task.py with type hints
- [ ] T014 [P] [US1] Implement TaskManager service in src/services/task_manager.py with methods:
  - `add_task(self, title: str, description: Optional[str]) -> Task`
  - `get_task(self, task_id: int) -> Optional[Task]`
  - `get_all_tasks(self) -> List[Task]`
- [ ] T015 [P] [US1] Implement CLI interface handler in src/services/cli_interface.py
- [ ] T016 [P] [US1] Implement menu display in src/cli/menu.py with 6 options
- [ ] T017 [P] [US1] Implement application entry point in src/cli/main.py
- [ ] T018 [P] [US1] Add validation and error handling in src/lib/validators.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: [Brief description of what this story delivers]
Users can track progress on their tasks by marking them as complete or incomplete through the console interface.

**Independent Test**: [How to verify this story works on its own]
Can be tested by creating a task, marking it complete, viewing updated list, and toggling it back to incomplete - providing value as a basic completion tracker.

### Tests for User Story 2 (OPTIONAL ⚠️)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T019 [P] [US2] Contract test for Mark Complete in tests/contract/test_mark_complete.py
- [ ] T020 [P] [US2] Integration test for Mark and Toggle workflow in tests/integration/test_mark_toggle.py

### Implementation for User Story 2

- [ ] T021 [P] [US2] Add method `toggle_complete(self, task_id: int) -> bool` to TaskManager service
- [ ] T022 [P] [US2] Update CLI interface in src/services/cli_interface.py to support mark complete operation
- [ ] T023 [P] [US2] Update menu.py to include Mark Complete option

**Checkpoint**: At this point, User Story 2 should be fully functional and testable independently.

**Dependencies**: Can start after User Story 1 (complete) - can integrate with task model and manager

---

## Phase 5: User Story 3 - Update Task Details (Priority: P2)

**Goal**: [Brief description of what this story delivers]
Users can modify existing task information (title and/or description) when plans change through the console interface.

**Independent Test**: [How to verify this story works on its own]
Can be tested by creating a task, updating its title/description, and verifying that changes are reflected - delivering value as a flexible task tracker.

### Tests for User Story 3 (OPTIONAL ⚠️)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T024 [P] [US2] Contract test for Update Task in tests/contract/test_update_task.py
- [ ] T025 [P] [US2] Integration test for Update workflow in tests/integration/test_update.py

### Implementation for User Story 3

- [ ] T026 [P] [US2] Add method `update_task(self, task_id: int, title: Optional[str], description: Optional[str]) -> bool` to TaskManager service
- [ ] T027 [P] [US2] Update CLI interface in src/services/cli_interface.py to support update operation with prompts
- [ ] T028 [P] [US2] Update menu.py to include Update Task option

**Checkpoint**: At this point, User Story 3 should be fully functional and testable independently.

**Dependencies**: Can start after User Story 1 (complete) - uses existing Task model and manager

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P3)

**Goal**: [Brief description of what this story delivers]
Users can remove tasks they no longer need from the list through the console interface with confirmation.

**Independent Test**: [How to verify this story works on its own]
Can be tested by creating multiple tasks, deleting one by ID with confirmation, and verifying it's removed from list - providing value for task list management.

### Tests for User Story 4 (OPTIONAL ⚠️)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T029 [P] [US3] Contract test for Delete Task in tests/contract/test_delete_task.py
- [ ] T030 [P] [US3] Integration test for Delete with confirmation workflow in tests/integration/test_delete.py

### Implementation for User Story 4

- [ ] T031 [P] [US3] Add method `delete_task(self, task_id: int) -> bool` to TaskManager service
- [ ] T032 [P] [US3] Update CLI interface in src/services/cli_interface.py to support delete operation with confirmation
- [ ] T033 [P] [US3] Update menu.py to include Delete Task option

**Checkpoint**: At this point, User Story 4 should be fully functional and testable independently.

**Dependencies**: Can start after User Story 1 (complete) - uses existing Task model and manager

---

## Phase N: Polish & Cross-Cutting Concerns

- [ ] T034 Documentation updates in docs/README.md
- [ ] T035 Code cleanup and refactoring
- [ ] T036 Performance optimization across all stories
- [ ] T037 Additional unit tests (if requested) in tests/unit/
- [ ] T038 Security hardening

**Purpose**: Improvements that affect multiple user stories.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: BLOCKS all user stories (US1, US2, US3, US4) - MUST complete first
- **User Story 1 (US1)**: No story dependencies - can start after Phase 2
- **User Story 2 (US2)**: Can start after US1 complete - can integrate with existing model/manager
- **User Story 3 (US3)**: Can start after US1 complete - can integrate with existing model/manager
- **User Story 4 (US4)**: Can start after US1 complete - can integrate with existing model/manager
- **Polish (Phase N)**: Depends on all desired user stories being complete

### Execution Order

**Recommended Approach (Parallel After Foundation):**
1. Complete Phase 1 (Setup)
2. Complete Phase 2 (Foundational)
3. **PARALLEL START**: US1, US2, US3, US4 can proceed in parallel (if team capacity allows)
4. Complete Phase N (Polish)

**Sequential Approach (Single Developer):**
1. Complete Phase 1
2. Complete Phase 2
3. Complete US1
4. Complete US2
5. Complete US3
6. Complete US4
7. Complete Phase N

---

## Dependencies Section

| Task | Depends On | Description |
|-------|-----------|-------------|
| T001 | None | Setup phase - no dependencies |
| T002 | None | Setup phase - no dependencies |
| T003 | None | Setup phase - no dependencies |
| T004 | None | Setup phase - no dependencies |
| T010 | T012 | US1 test depends on Task entity model |
| T011 | T012 | US1 test depends on View operation implemented |
| T012 | T010, T013 | US1 implementation depends on Task model and TaskManager |
| T014 | T012 | US1 integration test depends on CLI complete |
| T015 | T012 | US1 integration test depends on CLI complete |
| T017 | T012, T013 | US1 menu depends on Task entity and CLI interface |
| T018 | T012, T013, T017 | US1 entry point depends on components and services |
| T019 | T018 | US1 validation depends on validators lib |
| T020 | T018 | US1 main.py depends on entry point |
| T019 | T021 | US2 Mark Complete depends on TaskManager (US1) |
| T022 | T021 | US2 CLI depends on TaskManager (US1) |
| T023 | T022 | US2 menu depends on Mark Complete operation |
| T024 | T026 | US3 Update Task depends on TaskManager (US1) |
| T025 | T024 | US3 CLI depends on TaskManager (US1) |
| T026 | T025 | US3 CLI depends on Update operation |
| T027 | T026 | US3 menu depends on Update Task operation |
| T031 | T021 | US4 Delete Task depends on TaskManager (US1) |
| T032 | T031 | US4 CLI depends on TaskManager (US1) |
| T033 | T032 | US4 menu depends on Delete Task operation |
| T034 | T017 | Polish depends on all core components |
| T035 | T017 | Polish documentation updates README.md |
| T036 | T017 | Polish code cleanup after all stories |

---

## Parallel Opportunities

All Setup tasks (T001-T004) can run in parallel.
After Phase 2 completes, user stories US1, US2, US3, US4 can proceed in parallel by different team members.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 (Setup)
2. Complete Phase 2 (Foundational)
3. Complete US1: Create Task model + TaskManager + CLI interface
4. **STOP AND VALIDATE**: Test US1 independently
5. Deploy/demo if ready

This delivers: Users can create and view tasks in console (core value as MVP).

### Incremental Delivery

Once MVP complete, proceed to US2, US3, US4 in any order or parallel.

---

## Notes

- **[P] markers**: Tasks T021, T022, T026, T031 can run in parallel with US1 (different files)
- **[Story] labels**: US1, US2, US3, US4 map tasks to user stories for traceability
- **File paths**: All paths are relative to repository root
- **Tests**: Marked ⚠️ are OPTIONAL - only generate if explicitly requested in spec
- **MVP**: User Story 1 provides minimum viable product value (create + view tasks)
