"""Persistence helpers for saving and loading todo tasks to JSON."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

_JSON_INDENT = 2
_ENCODING = "utf-8"


def _serialize_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert in-memory task dicts into JSON-serializable objects."""
    serialized: List[Dict[str, Any]] = []
    for task in tasks:
        obj = dict(task)
        created_at = obj.get("created_at")
        if isinstance(created_at, datetime):
            obj["created_at"] = created_at.isoformat()
        serialized.append(obj)
    return serialized


def _deserialize_tasks(data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    """Convert JSON-loaded task dicts into in-memory objects with datetime."""
    tasks: List[Dict[str, Any]] = []
    max_id = 0
    for item in data:
        task = dict(item)
        created_at = task.get("created_at")
        if isinstance(created_at, str):
            try:
                task["created_at"] = datetime.fromisoformat(created_at)
            except ValueError:
                print(
                    "Warning: Skipping task with invalid created_at timestamp.",
                    file=sys.stderr,
                )
                continue
        elif not isinstance(created_at, datetime):
            task["created_at"] = datetime.now()
        task_id = task.get("id")
        if isinstance(task_id, int):
            max_id = max(max_id, task_id)
        tasks.append(task)
    next_id = max_id + 1 if max_id > 0 else 1
    return tasks, next_id


def load_tasks_from_file(file_path: str) -> Tuple[List[Dict[str, Any]], int]:
    """Load tasks from JSON file, returning tasks list and next ID."""
    path = Path(file_path)
    if not path.exists():
        return [], 1

    try:
        raw = path.read_text(encoding=_ENCODING)
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("tasks.json must contain a list")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Warning: Could not load tasks from {path}: {exc}", file=sys.stderr)
        return [], 1

    return _deserialize_tasks(data)


def save_tasks_to_file(tasks: List[Dict[str, Any]], file_path: str) -> bool:
    """Persist given tasks to JSON file. Returns True on success."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = _serialize_tasks(tasks)

    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding=_ENCODING, delete=False, dir=str(path.parent)
        ) as tmp:
            json.dump(serialized, tmp, ensure_ascii=False, indent=_JSON_INDENT)
            tmp.flush()
            os.fsync(tmp.fileno())
            temp_name = tmp.name
        os.replace(temp_name, path)
        return True
    except OSError as exc:
        print(f"Error: Failed to save tasks to {path}: {exc}", file=sys.stderr)
        try:
            if "temp_name" in locals():
                Path(temp_name).unlink(missing_ok=True)
        except OSError:
            pass
        return False
