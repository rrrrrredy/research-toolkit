"""Run one local Toolkit request and retain its exact input/output."""
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

root = Path(__file__).resolve().parent.parent
operation, request_name = sys.argv[1:3]
request = root / "records" / "toolkit-calls" / request_name
prefix = request.with_suffix("")
response = prefix.with_name(prefix.name + ".response.json")
stderr = prefix.with_name(prefix.name + ".stderr.txt")
metadata = prefix.with_name(prefix.name + ".execution.json")
for output in (response, stderr, metadata):
    if output.exists():
        raise FileExistsError(output)
command = [sys.executable, "-B", str(root / "toolkit/scripts/research_workflow.py"),
           operation, "--workspace", str(root / "tasks"), "--request", str(request)]
started = datetime.now(timezone.utc).isoformat()
result = subprocess.run(command, cwd=root, capture_output=True)
response.write_bytes(result.stdout)
stderr.write_bytes(result.stderr)
metadata.write_text(json.dumps({"command": command, "request": str(request.relative_to(root)),
    "started_at": started, "finished_at": datetime.now(timezone.utc).isoformat(),
    "returncode": result.returncode}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
sys.stdout.buffer.write(result.stdout)
sys.stderr.buffer.write(result.stderr)
sys.exit(result.returncode)
