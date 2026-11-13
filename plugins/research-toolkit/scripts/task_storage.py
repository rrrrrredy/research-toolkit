"""Shared task-local reads and writes; no research or orchestration decisions."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()


def file_io_path(path):
    """Keep Windows task files and their longer backup paths accessible."""
    value = str(Path(path).resolve())
    if os.name == 'nt' and not value.startswith('\\\\?\\'):
        value = '\\\\?\\UNC\\' + value[2:] if value.startswith('\\\\') else '\\\\?\\' + value
    return Path(value)


def safe_path(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name or ':' in name or '\\' in name:
        raise ValueError('Use a task-relative path with forward slashes.')
    if name.startswith('/') or any(p in {'.', '..', ''} for p in name.split('/')):
        raise ValueError('Path must stay inside the task directory.')
    path = (root / name).resolve()
    path.relative_to(root.resolve())
    return path


def load(root, name):
    try:
        value = json.loads(safe_path(root, name).read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        raise ValueError(f'{name}: invalid JSON at line {exc.lineno}, column {exc.colno}. Preserve the file and recover its saved version.') from None
    if name == 'state/progress.json':
        if not isinstance(value, dict):
            raise ValueError(f'{name}: expected a JSON object, not {type(value).__name__}.')
        if 'brief' in value and not isinstance(value['brief'], dict):
            raise ValueError(f'{name}: brief must be a JSON object.')
    return value


def task_root(workspace: Path, task: str, *, create=False) -> Path:
    if not isinstance(task, str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}', task):
        raise ValueError('Task ID must use letters, numbers, underscores or hyphens.')
    workspace = workspace.expanduser().resolve()
    root = (workspace / task).resolve()
    root.relative_to(workspace)
    root = file_io_path(root)
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
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                         dir=path.parent, prefix='.' + path.name + '.', suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if path.exists():
            shutil.copymode(path, temporary)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
