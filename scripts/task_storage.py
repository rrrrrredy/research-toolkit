"""Shared task-local reads and writes; no research or orchestration decisions."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()


def safe_path(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name or ':' in name or '\\' in name:
        raise ValueError('Use a task-relative path with forward slashes.')
    if name.startswith('/') or any(p in {'.', '..', ''} for p in name.split('/')):
        raise ValueError('Path must stay inside the task directory.')
    path = (root / name).resolve()
    path.relative_to(root.resolve())
    return path


def load(root, name):
    return json.loads(safe_path(root, name).read_text(encoding='utf-8'))


def task_root(workspace: Path, task: str, *, create=False) -> Path:
    if not isinstance(task, str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}', task):
        raise ValueError('Task ID must use letters, numbers, underscores or hyphens.')
    workspace = workspace.expanduser().resolve()
    root = (workspace / task).resolve()
    root.relative_to(workspace)
    if create:
        root.mkdir(parents=True, exist_ok=True)
    elif not root.is_dir():
        raise ValueError('Task does not exist. Start it first.')
    return root


def save(root, name, data):
    save_text(root, name, json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def save_text(root, name, content):
    path = safe_path(root, name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
