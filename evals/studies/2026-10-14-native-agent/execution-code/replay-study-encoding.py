"""Replay the observed Windows JSON transport failure; no model call."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent
REPO = BASE / "research-toolkit"
OUT = BASE / "output/native-toolkit-20261014"
sys.path.insert(0, str(REPO / "scripts"))
import research_workflow as w

source = (OUT / "authors/toolkit/sources/scale.txt").read_text(encoding="utf-8")
assert "\ue200" in source
brief = json.loads((OUT / "authors/toolkit/work/state/progress.json").read_text(encoding="utf-8"))["brief"]
results = {}
for label, script in (("before", OUT / "authors/toolkit/toolkit/scripts/research_workflow.py"),
                      ("after", REPO / "scripts/research_workflow.py")):
    workspace = OUT / "encoding-replay" / label
    w.start(workspace, "probe", brief, profile="full")
    root = workspace / "probe"
    w.save_text(root, "source.md", source)
    w.save_text(root, "final.md", "# Transport probe\nThe source describes SWE-Bench Pro.\n")
    w.save_text(root, "data/source_registry.csv", "source_id,title,url,source_type,read_scope,read_evidence\nS1,SWE-Bench Pro,https://scale.com/blog/swe-bench-pro,primary,full_text,source.md\n")
    w.save_text(root, "data/claims_registry.csv", "claim_id,claim,claim_type,supporting_sources\nC1,Source describes SWE-Bench Pro,verified_fact,S1\n")
    request = {"task": "probe", "evidence_paths": ["source.md"], "reviewer": "self", "config": {
        "reviewers": [{"id": "primary", "backend": "self", "model": "author-context"}]}}
    result = subprocess.run([sys.executable, str(script), "review", "--workspace", str(workspace)],
                            input=json.dumps(request).encode("utf-8"), capture_output=True,
                            env={**os.environ, "PYTHONIOENCODING": "gbk", "PYTHONUTF8": "0"}, timeout=30)
    (workspace / "stdout.bin").write_bytes(result.stdout)
    (workspace / "stderr.txt").write_bytes(result.stderr)
    valid = False
    try:
        response = json.loads(result.stdout.decode("utf-8"))
        valid = response.get("action_required") == "self_review"
    except (UnicodeError, ValueError): pass
    results[label] = {"exit_code": result.returncode, "valid_utf8_json": valid,
                      "action_required": response.get("action_required") if result.returncode == 0 else None,
                      "citation_character_preserved": "\ue200".encode("utf-8") in result.stdout,
                      "unicode_encode_error": b"UnicodeEncodeError" in result.stderr,
                      "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
                      "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest()}
assert results["before"]["exit_code"] == 1 and results["before"]["unicode_encode_error"]
assert results["after"]["exit_code"] == 0 and results["after"]["citation_character_preserved"]
(OUT / "encoding-replay/results.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
print(json.dumps(results, indent=2))
