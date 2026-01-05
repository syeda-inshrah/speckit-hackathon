# Test Contract: Task Operations

**Feature**: Phase I - In-Memory Python Console Todo App
**Date**: 2025-12-01
**Status**: Final
**Derived from**: spec.md FR-001 through FR-015

## Contract Overview

This contract defines testable behaviors for all task operations (Create, Read, Update, Delete, Mark Complete) that must be implemented to satisfy functional requirements.

## Testable Behaviors

### T1: Add Task Behavior

**Requirement**: FR-002, FR-003, FR-004

**Given**: Empty task list
**When**: User provides a valid task title (1-200 characters)
**Then**:
- Task is created with a unique sequential ID starting at 1
- Task has completed = False by default
- Task has created_at = current timestamp
- Task is added to in-memory task list
- Success message displays to user: Task [ID] created successfully

**Edge Cases**:
- When user provides title but skips optional description: Task created with description = None
- When user provides title with >200 characters: Error message Title exceeds 200 characters
- When user provides empty/whitespace-only title: Error message Title cannot be empty

---

### T2: Get Task Behavior

**Requirement**: FR-009

**Given**: Task exists in list with ID X
**When**: User requests task by ID X
**Then**: Return Task object with all fields (id, title, description, completed, created_at)

**Given**: Task does not exist with ID X
**When**: User requests task by ID X
**Then**: Return None

---

### T3: Update Task Behavior

**Requirement**: FR-006

**Given**: Task exists in list with ID X
**When**: User provides updated title and/or description
**Then**:
- Task fields are updated in in-memory list
- Unchanged fields preserve their values
- Success message displays: Task [ID] updated successfully

**Given**: Task does not exist with ID X
**When**: User attempts to update
**Then**: Error message displays: Task not found without modifying any task

---

### T4: Delete Task Behavior

**Requirement**: FR-007

**Given**: Task exists in list with ID X
**When**: User confirms deletion (y/yes)
**Then**:
- Task is removed from in-memory list
- Success message displays: Task [ID] deleted

**Given**: Task exists in list with ID X
**When**: User declines deletion (n/no or any non-yes response)
**Then**: Task is NOT deleted from list
- Message displays: Deletion cancelled

**Given**: Task does not exist with ID X
**When**: User attempts to delete
**Then**: Error message displays: Task not found without asking for confirmation

---

### T5: Toggle Complete Behavior

**Requirement**: FR-008

**Given**: Task exists in list with ID X and completed = False
**When**: User marks task complete
**Then**: Task.completed = True
- Success message displays: Task [ID] completed

**Given**: Task exists in list with ID X and completed = True
**When**: User marks task complete (toggle)
**Then**: Task.completed = False
- Success message displays: Task [ID] marked incomplete

**Given**: Task does not exist with ID X
**When**: User attempts to toggle status
**Then**: Error message displays: Task not found

---

### T6: View Tasks Behavior

**Requirement**: FR-005

**Given**: Task list contains N tasks
**When**: User requests to view all tasks
**Then**: Display list of all tasks showing:
- Task ID
- Task title
- Status indicator (✓ for complete, ✗ for incomplete)
- Creation date/time

**Given**: Task list is empty
**When**: User requests to view all tasks
**Then**: Display message: No tasks found

---

## Implementation Notes

- All operations must return immediately (no blocking)
- All error messages must be user-friendly and descriptive
- Task IDs must be preserved when tasks are deleted (gaps allowed)
- Status indicators must use visual symbols (✓ and ✗) for quick recognition

## Success Criteria

- All 6 testable behaviors implemented correctly
- All edge cases handled gracefully
- All error messages clear and actionable
