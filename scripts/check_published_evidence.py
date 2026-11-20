"""Verify the published GPAI manuscripts, reviewer decisions and receipt against their public records."""
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "docs/case-study/v3-review"


def read(name):
    return json.loads((CASE / name).read_bytes())


def checksum(name):
    return hashlib.sha256((CASE / name).read_bytes()).hexdigest()


def verify():
    records = read("records.json")
    initial, final = (checksum(f"reports/{name}.md") for name in ("initial", "final"))
    if (initial, final) != (records["initial_artifact_sha256"], records["final_artifact_sha256"]):
        raise ValueError("The retained manuscripts differ from their recorded hashes")
    for name, run in records["runs"].items():
        findings = set()
        for row in run["responses"]:
            original = read(row["file"])
            if checksum(row["file"]) != row["public_sha256"] or original["input_version"] != row["input_version"]:
                raise ValueError("Changed response or review input: " + row["file"])
            if row["artifact_sha256"] != (final if row["role"] == "acceptance" else initial):
                raise ValueError("Response bound to a different manuscript: " + row["file"])
            if not row["local_path_replaced"] and row["original_sha256"] != row["public_sha256"]:
                raise ValueError("Unexplained change to original: " + row["file"])
            if row["role"] == "reviewer":
                findings.update(row["slot"] + "/" + item["finding_id"] for item in original["findings"])
        audit = read(name + "/originals/audit.json")
        groups = audit["disposition_groups"]
        decided = list(audit["dispositions"]) + [key for group in groups for key in group["finding_ids"]]
        if Counter(decided) != Counter({key: 1 for key in findings}):
            raise ValueError("Missing or duplicated finding in " + name)
        if name == "live" and (len(findings), len(audit["dispositions"]), len(groups)) != (39, 9, 8):
            raise ValueError("Published live audit totals differ from source")
        if name == "control" and sorted((group["decision"], len(group["finding_ids"])) for group in groups) != [
                ("confirmed_defect", 4), ("no_change", 4)]:
            raise ValueError("Disagreement control differs from recorded decisions")
    receipt = read("live/receipt.json")
    if (receipt["status"] != "pass" or receipt["artifacts"][receipt["artifact"]] != final or
            read("live/originals/acceptance.json")["result"] != "pass" or
            read("live/finish.json")["artifact_sha256"] != final):
        raise ValueError("Final manuscript, independent check and delivery receipt differ")
    active = Counter()
    peak = 0
    for item in read("live/turn-events.json"):
        if item["event"] not in ("turn/start", "turn/completed"):
            raise ValueError("Unknown host event")
        run = item["run"]
        active[run] += 1 if item["event"] == "turn/start" else -1
        if active[run] < 0:
            raise ValueError("Unexpected completion in a host invocation")
        peak = max(peak, active[run])
    if peak != 2:
        raise ValueError("Published host invocation peak differs from the event record")
    print("Verified the GPAI manuscripts, original responses, 39 findings / 17 decisions, "
          "separate four-reviewer control, per-invocation peak of two, and final receipt.")


if __name__ == "__main__":
    verify()
