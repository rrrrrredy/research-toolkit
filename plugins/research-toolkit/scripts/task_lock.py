"""Fail-fast, process-owned locks for cooperating local task operations."""
from contextlib import contextmanager
import os
from pathlib import Path
import threading
from task_storage import file_io_path

_held = threading.local()
BUSY = ("This task already has an active operation or its lock is unavailable. "
        "Wait for that operation to finish; do not start duplicate reviews.")


def lock_windows_reader(stream):
    # The CRT's LK_NBRLCK is exclusive too. LockFileEx can share byte zero
    # between readers and conflicts with the existing CRT writer lock.
    import ctypes
    from ctypes import wintypes
    import msvcrt

    class Overlapped(ctypes.Structure):
        _fields_ = [("internal", ctypes.c_size_t), ("internal_high", ctypes.c_size_t),
                    ("offset", wintypes.DWORD), ("offset_high", wintypes.DWORD), ("event", wintypes.HANDLE)]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    handle = wintypes.HANDLE(msvcrt.get_osfhandle(stream.fileno()))
    if not kernel.LockFileEx(handle, 1, 0, 1, 0, ctypes.byref(Overlapped())):  # FAIL_IMMEDIATELY
        raise ctypes.WinError(ctypes.get_last_error())


@contextmanager
def task_lock(root: Path, *, read_only=False):
    # Reentrant only for this thread/process (start may read its own status).
    root = file_io_path(root)
    identity = (os.getpid(), str(root.resolve()))
    held = getattr(_held, "paths", set())
    if identity in held:
        yield
        return
    # Keep the inode/file in place: unlinking after release could split waiters
    # across two independent locks. OS ownership, not file existence, is the lock.
    lock_path = (root / ".research-toolkit.lock").resolve()
    lock_path.relative_to(root.resolve())
    if read_only:
        try:
            stream = lock_path.open("rb")
        except FileNotFoundError:
            # Archived or pre-lock task. A cooperating writer must create this
            # permanent file before changing any records. Discard an overlapping read.
            try:
                yield
            finally:
                if lock_path.exists():
                    raise ValueError(BUSY)
            return
    else:
        stream = lock_path.open("a+b")
    with stream:
        try:
            if os.name == "nt":
                import msvcrt
                stream.seek(0)
                if read_only:
                    lock_windows_reader(stream)
                else:
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                mode = fcntl.LOCK_SH if read_only else fcntl.LOCK_EX
                fcntl.flock(stream.fileno(), mode | fcntl.LOCK_NB)
        except OSError as exc:
            raise ValueError(BUSY) from exc
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
