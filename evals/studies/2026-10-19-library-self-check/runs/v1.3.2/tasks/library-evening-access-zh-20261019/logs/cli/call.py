"""Retain an actual workflow CLI invocation without overwriting earlier records."""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

action, request, prefix = sys.argv[1:]
command = [sys.executable, "-B", "-X", "utf8", "toolkit/scripts/research_workflow.py",
           action, "--workspace", "tasks", "--request", request]
started = datetime.now(timezone.utc).isoformat()
with open(prefix + ".response.json", "xb") as output, \
     open(prefix + ".stderr.txt", "xb") as errors, \
     open(prefix + ".invocation.json", "x", encoding="utf-8") as record:
    result = subprocess.run(command, stdout=output, stderr=errors, check=False)
    json.dump({"command": command, "started_utc": started,
               "finished_utc": datetime.now(timezone.utc).isoformat(),
               "exit_code": result.returncode}, record, ensure_ascii=False, indent=2)
    record.write("\n")
print(Path(prefix + ".response.json").read_text(encoding="utf-8"), end="")
errors = Path(prefix + ".stderr.txt").read_text(encoding="utf-8")
if errors:
    print(errors, file=sys.stderr, end="")
print(f"CLI exit code: {result.returncode}", file=sys.stderr)
sys.exit(result.returncode)
