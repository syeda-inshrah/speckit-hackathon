# Data Model: Phase I - In-Memory Python Console Todo App

**Date**: 2025-12-01
**Status**: Final
**Derived from**: plan.md

## Entity: Task

### Purpose
Represents a single todo item that can be created, viewed, updated, deleted, and marked complete/incomplete by users through the command-line interface.

### Fields

| Field | Type | Required | Validation | Description |
|-------|------|---------|------------|-------------|
| `id` | `int` | Yes | Auto-assigned, unique, sequential starting at 1 | Unique identifier for the task |
| `title` | `str` | Yes | Non-empty, stripped, max 200 characters | Human-readable task name |
| `description` | `str \| None` | No | Max 1000 characters if provided | Optional additional details about the task |
| `completed` | `bool` | No | Default `False` | Completion status: `True` = complete, `False` = incomplete |
| `created_at` | `datetime` | No | Auto-assigned on creation | Timestamp of when task was created |

### Type Definition

```python
from datetime import datetime
from typing import Optional

class Task:
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
```

**Type Hints**: Required per constitution on all functions/methods using this data model.

### Validation Rules

**From Functional Requirements:**
- FR-009: `task_id` must exist in task list before any operation
- FR-009: `task_id` must be numeric (positive integer)
- FR-010: `title` cannot be empty or whitespace-only
- FR-002: `title` maximum length is 200 characters
- FR-002: `description` maximum length is 1000 characters (if provided)

**Validation Implementation**:
```python
def validate_task_id(task_id: str) -> bool:
    """Validate task ID exists and is numeric."""
    return task_id.isdigit() and int(task_id) > 0

def validate_title(title: str) -> bool:
    """Validate title is non-empty and not whitespace-only."""
    return len(title.strip()) > 0 and len(title) <= 200

def validate_description(description: Optional[str]) -> bool:
    """Validate description length if provided."""
    if description is None:
        return True
    return len(description) <= 1000
```

### State Transitions

Task state can transition through the following operations:

| Operation | State Change | Reversible |
|-----------|-------------|------------|
| Create | New task created | Yes (delete) |
| Update | Title/description fields modified | Yes (update with previous values) |
| Delete | Task removed from list | No |
| Mark Complete | `completed` toggles `True` ↔ `False` | Yes (toggle again) |

No complex state machines required - simple CRUD operations with in-memory storage.

### Relationships

No relationships defined - Phase I is a single-user console application with in-memory storage. Tasks exist independently with no foreign keys or references to other entities.
