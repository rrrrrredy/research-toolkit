"""Bound reviewer subprocesses and their descendants without invoking a shell."""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys


class ProcessCleanupError(OSError):
    """Do not retry an execution whose local cancellation could not be confirmed."""


class WindowsJob:
    def __init__(self):
        import ctypes as c
        from ctypes import wintypes as w

        class Limits(c.Structure):
            _fields_ = [("process_time", c.c_int64), ("job_time", c.c_int64),
                        ("flags", w.DWORD), ("min_working_set", c.c_size_t),
                        ("max_working_set", c.c_size_t), ("active_limit", w.DWORD),
                        ("affinity", c.c_size_t), ("priority", w.DWORD), ("scheduling", w.DWORD)]

        class Extended(c.Structure):
            _fields_ = [("basic", Limits), ("io", c.c_uint64 * 6),
                        ("process_memory", c.c_size_t), ("job_memory", c.c_size_t),
                        ("peak_process_memory", c.c_size_t), ("peak_job_memory", c.c_size_t)]

        self.c = c
        self.api = c.WinDLL("kernel32", use_last_error=True)
        signatures = {
            "CreateJobObjectW": ([c.c_void_p, w.LPCWSTR], w.HANDLE),
            "SetInformationJobObject": ([w.HANDLE, c.c_int, c.c_void_p, w.DWORD], w.BOOL),
            "OpenProcess": ([w.DWORD, w.BOOL, w.DWORD], w.HANDLE),
            "AssignProcessToJobObject": ([w.HANDLE, w.HANDLE], w.BOOL),
            "TerminateJobObject": ([w.HANDLE, w.UINT], w.BOOL),
            "CloseHandle": ([w.HANDLE], w.BOOL),
        }
        for name, (args, result) in signatures.items():
            function = getattr(self.api, name)
            function.argtypes, function.restype = args, result
        self.handle = self.api.CreateJobObjectW(None, None)
        if not self.handle:
            raise c.WinError(c.get_last_error())
        limits = Extended()
        limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.api.SetInformationJobObject(self.handle, 9, c.byref(limits), c.sizeof(limits)):
            error = c.WinError(c.get_last_error())
            self.close()
            raise error

    def attach(self, pid):
        process = self.api.OpenProcess(0x0101, False, pid)  # SET_QUOTA | TERMINATE
        if not process:
            raise self.c.WinError(self.c.get_last_error())
        try:
            if not self.api.AssignProcessToJobObject(self.handle, process):
                raise self.c.WinError(self.c.get_last_error())
        finally:
            self.api.CloseHandle(process)

    def terminate(self):
        if not self.api.TerminateJobObject(self.handle, 1):
            raise self.c.WinError(self.c.get_last_error())

    def close(self):
        if self.handle:
            self.api.CloseHandle(self.handle)
            self.handle = None


# The gate reads exactly one byte before spawning. The parent attaches the gate
# to its job first, so even immediately spawned grandchildren belong to that job.
WINDOWS_GATE = ("import json,os,subprocess,sys; "
                "ready=os.read(0,1); "
                "sys.exit(subprocess.call(json.loads(sys.argv[1])) if ready==b'1' else 1)")


def run_bounded(command, wire, cwd, timeout):
    job = WindowsJob() if os.name == "nt" else None
    argv = [sys.executable, "-c", WINDOWS_GATE, json.dumps(command)] if job else command
    process = None

    def stop():
        try:
            if job:
                job.terminate()
            else:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            if process.poll() is None:
                process.kill()
            process.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ProcessCleanupError(f"Local process cleanup is unconfirmed for PID {process.pid}.") from exc

    try:
        process = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, cwd=cwd, start_new_session=not bool(job),
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        if job:
            job.attach(process.pid)
        try:
            stdout, stderr = process.communicate((('1' if job else '') + wire).encode('utf-8'), timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            stop()
            try:
                stdout, stderr = process.communicate(timeout=5)
            except subprocess.TimeoutExpired as drain_error:
                raise ProcessCleanupError("Local process pipes remained active after cancellation.") from drain_error
            exc.output, exc.stderr = stdout, stderr
            raise
        return subprocess.CompletedProcess(command, process.returncode,
            stdout.decode('utf-8'), stderr.decode('utf-8'))
    finally:
        try:
            if process is not None:
                stop()
                for stream in (process.stdin, process.stdout, process.stderr):
                    if stream:
                        stream.close()
        finally:
            if job:
                job.close()
