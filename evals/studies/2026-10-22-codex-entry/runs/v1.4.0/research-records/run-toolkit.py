"""Run one local Toolkit CLI request and preserve its actual response."""
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
label, operation, request_name = sys.argv[1:]
request = root / request_name
log = root / "research-records" / "toolkit-calls"
log.mkdir(parents=True, exist_ok=True)
argv = [sys.executable, "-B", str(root / "toolkit/scripts/research_workflow.py"),
        operation, "--workspace", str(root / "tasks"), "--request", str(request)]
with (log / f"{label}.request.json").open("x", encoding="utf-8") as stream:
    stream.write(request.read_text(encoding="utf-8"))
with (log / f"{label}.command.json").open("x", encoding="utf-8") as stream:
    json.dump({"argv": argv, "cwd": str(root)}, stream, ensure_ascii=False, indent=2)
env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
result = subprocess.run(argv, cwd=root, env=env, capture_output=True)
for suffix, content in [("response.json", result.stdout), ("stderr.txt", result.stderr)]:
    with (log / f"{label}.{suffix}").open("xb") as stream:
        stream.write(content)
with (log / f"{label}.exit-code.txt").open("x", encoding="utf-8") as stream:
    stream.write(str(result.returncode) + "\n")
sys.stdout.buffer.write(result.stdout)
sys.stderr.buffer.write(result.stderr)
raise SystemExit(result.returncode)
