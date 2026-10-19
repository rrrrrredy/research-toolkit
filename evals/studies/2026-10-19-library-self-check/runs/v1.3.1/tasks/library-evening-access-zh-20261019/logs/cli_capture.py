"""Run the existing workflow CLI and retain its actual UTF-8 I/O."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
action, request = sys.argv[1:]
task_dir = Path("tasks/library-evening-access-zh-20261019")
request_path = Path(request)
log_dir = task_dir / "logs/api"
log_dir.mkdir(exist_ok=True)
prefix = request_path.stem
command = [sys.executable, "-B", "toolkit/scripts/research_workflow.py",
           action, "--workspace", "tasks", "--request", str(request_path)]
environment = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8",
                   PYTHONDONTWRITEBYTECODE="1")
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
with (log_dir / f"{prefix}.response.json").open("xb") as output, \
        (log_dir / f"{prefix}.stderr.txt").open("xb") as errors, \
        (log_dir / f"{prefix}.run.json").open("x", encoding="utf-8") as run_log:
    result = subprocess.run(command, stdout=output, stderr=errors, env=environment)
    json.dump({"command": command, "request": str(request_path),
               "started_at": started,
               "finished_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "exit_code": result.returncode}, run_log, ensure_ascii=False, indent=2)
    run_log.write("\n")
print((log_dir / f"{prefix}.response.json").read_text(encoding="utf-8"))
stderr = (log_dir / f"{prefix}.stderr.txt").read_text(encoding="utf-8")
if stderr:
    print(stderr, file=sys.stderr)
sys.exit(result.returncode)
