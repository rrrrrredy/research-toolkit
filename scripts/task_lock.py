"""Fail-fast, process-owned locks for cooperating local task operations."""
from contextlib import contextmanager
import os
from pathlib import Path
import threading

_held = threading.local()


@contextmanager
def task_lock(root: Path):
    # Reentrant only for this thread/process (start may read its own status).
    identity = (os.getpid(), str(root.resolve()))
    held = getattr(_held, "paths", set())
    if identity in held:
        yield
        return
    # Keep the inode/file in place: unlinking after release could split waiters
    # across two independent locks. OS ownership, not file existence, is the lock.
    lock_path = (root / ".research-toolkit.lock").resolve()
    lock_path.relative_to(root.resolve())
    with lock_path.open("a+b") as stream:
        try:
            if os.name == "nt":
                import msvcrt
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise ValueError("This task already has an active operation or its lock is unavailable. "
                             "Wait for that operation to finish; do not start duplicate reviews.") from exc
        _held.paths = held | {identity}
        try:
            yield
        finally:
            _held.paths = held
            if os.name == "nt":
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
