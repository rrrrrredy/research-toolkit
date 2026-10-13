#!/usr/bin/env python3
"""Read-only reconstruction of the eight prospective feedback probes."""
import base64
import argparse
import csv
import io
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

import run_blinded_evals as h
from summarize_development_pilot import safe

ROOT = Path(__file__).resolve().parents[1] / "evals/diagnostics/2026-10-13-feedback-probes"


def derive(root):
    plan = h.read(root / "plan.json")
    h.require(h.sha(h.encode(plan)) == h.read(root / "commitment.json")["plan_sha256"], "Feedback commitment mismatch")
    public = h.read(root / "public-manifest.json") if (root / "public-manifest.json").exists() else None
    transforms = {}
    if public:
        for name, digest in public["sha256"].items():
            h.require(h.sha(safe(root, name).read_bytes()) == digest, "Feedback public artifact changed")
        transforms = {row["original_path"]: row for row in public["transformations"]}
    for name, digest in h.read(root / "manifest.json")["sha256"].items():
        actual = transforms[name]["original_sha256"] if name in transforms else h.sha(safe(root, name).read_bytes())
        h.require(actual == digest, "Original feedback artifact hash mismatch")
    for name, digest in plan["code_sha256"].items():
        raw = base64.b64decode(safe(root, name + ".b64").read_bytes().strip(), validate=True)
        transformation = transforms.get(name + ".b64")
        if transformation:
            h.require(h.sha(raw) == transformation["public_decoded_sha256"] and digest == transformation["original_decoded_sha256"], "Redacted code archive mapping mismatch")
        else:
            h.require(h.sha(raw) == digest, "Feedback code archive mismatch")
    for name, text in plan["methods"].items():
        h.require(h.sha(text.encode()) == plan["method_sha256"][name], "Feedback method mismatch")
    tasks = {task["task_id"]: task for task in plan["tasks"]}
    rows, usage, elapsed = [], {}, {}
    for item in plan["requests"]:
        provider = item["provider"]
        settings = plan["models"][provider]
        folder = root / "attempts" / item["id"]
        task = tasks[item["task_id"]]
        h.require(json.loads(item["messages"][1]["content"]) == {"brief": task["brief"], "sources": task["sources"]}, "Probe source packet mismatch")
        expected = {"model": settings["model"], "messages": item["messages"], "stream": False,
                    settings["completion_parameter"]: settings["max_completion_tokens"], "thinking": {"type": settings["thinking"]}}
        h.require(h.read(folder / "request.json") == expected, "Feedback request differs from frozen plan")
        execution = h.read(folder / "execution.json")
        usage.setdefault(provider, {})
        elapsed[provider] = elapsed.get(provider, 0) + execution["elapsed_seconds"]
        for key, value in (execution.get("usage") or {}).items():
            if type(value) is int:
                usage[provider][key] = usage[provider].get(key, 0) + value
        row = {"id": item["id"], "provider": provider, "condition": item["condition"], "task_id": item["task_id"], "status": "unresolved"}
        if execution["status"] == "response_complete":
            response = h.read(folder / "response.json")
            content = (folder / "content.txt").read_bytes().decode("utf-8")
            h.require(content == response["choices"][0]["message"]["content"] and execution["usage"] == response["usage"], "Feedback raw content/usage mismatch")
            h.require(execution["model_returned"] == response["model"] in settings["accepted_model_ids"], "Feedback model alias mismatch")
            try:
                parsed, _ = h.parse_output(content, settings, "author")
            except (ValueError, TypeError):
                h.require((folder / "invalid.json").exists() and not (folder / "parsed.json").exists(), "Lost feedback format failure")
            else:
                h.require(parsed == h.read(folder / "parsed.json"), "Feedback parse mismatch")
                report = parsed["report"]
                actual = len(report.split()) if task["language"] == "en" else sum(not c.isspace() for c in report)
                row.update(status="parsed", length={"actual": actual, "minimum": task["minimum"], "maximum": task["maximum"],
                           "unit": "whitespace_words" if task["language"] == "en" else "nonwhitespace_characters",
                           "scope": "complete_report_including_markup_and_citations", "within_range": task["minimum"] <= actual <= task["maximum"]},
                           literal_process_clues=re.findall(r"independent review|未经独立|独立评审|Research Toolkit|\bchecklist\b|\bprofile\b", report, re.IGNORECASE))
        rows.append(row)
    results = h.read(root / "results.json")
    h.require([{k: row[k] for k in ("id", "status")} for row in rows] == results["results"], "Feedback result correspondence mismatch")
    h.require(len(rows) == results["requests_attempted"] == plan["max_requests"] == 8 and not results["previous_results_replaced"], "Feedback request accounting changed")
    return {"requests": 8, "format_valid": sum(r["status"] == "parsed" for r in rows),
            "length_valid": sum(r.get("length", {}).get("within_range", False) for r in rows),
            "literal_clue_reports": sum(bool(r.get("literal_process_clues")) for r in rows),
            "rows": rows, "usage": usage, "elapsed_seconds_sum": {k: round(v, 3) for k, v in elapsed.items()},
            "quality_adjudication": "separate condition-aware implementation-assistant observations", "general_efficacy_established": False}


def verify(root=ROOT):
    result = derive(root)
    h.require(result == h.read(root / "analysis.json"), "Feedback analysis differs from first evidence")
    observations = h.read(root / "adjudication.json")
    h.require({row["id"] for row in observations["reports"]} == {row["id"] for row in result["rows"]}, "Feedback source-check coverage mismatch")
    h.require(not observations["previous_results_replaced"], "Feedback must not rewrite older results")
    return result


class DeliveryControls(unittest.TestCase):
    def gate(self, task, report):
        import research_workflow as w
        from profile_policy import CHECKLIST
        with tempfile.TemporaryDirectory() as temporary, patch.dict("os.environ", {"RESEARCH_TOOLKIT_REVIEW_CONFIG": "", "RESEARCH_TOOLKIT_REVIEW_BACKEND": ""}):
            workspace = Path(temporary)
            w.start(workspace, "probe", {"question": task["brief"], "audience": "Fictional task reader",
                    "scope": "Only supplied S1 and S2", "output": "final.md", "depth": "Short decision note",
                    "evidence_standard": "The supplied fictional source text"}, profile="lite")
            root = workspace / "probe"
            w.save_text(root, "final.md", report)
            registry = io.StringIO(newline="")
            writer = csv.writer(registry)
            writer.writerow(["source_id", "title", "url", "source_type", "read_scope", "read_evidence"])
            for source in task["sources"]:
                name = source["id"] + ".md"
                w.save_text(root, name, source["text"])
                writer.writerow([source["id"], "Fictional " + source["id"], name, "primary", "full_text", name])
            w.save_text(root, "data/source_registry.csv", registry.getvalue())
            claim = "First-year budget is at most 10 units" if task["language"] == "en" else "June total water is 180 cubic metres"
            w.save_text(root, "data/claims_registry.csv", "claim_id,claim,claim_type,supporting_sources\nC1," + claim + ",verified_fact,S1\n")
            w.status(workspace, "probe", stage="draft")
            unit = "whitespace_words" if task["language"] == "en" else "nonwhitespace_characters"
            w.save_text(root, "state/requirements.jsonl", json.dumps({"requirement_id": "brief-length", "summary": task["brief"],
                        "status": "satisfied", "evidence": "final.md", "length_constraint": {"unit": unit,
                        "scope": "whole_artifact", "min": task["minimum"], "max": task["maximum"]}}) + "\n")
            checks, errors = w.inspect_length_constraints(root, "final.md")
            result = w.finish(workspace, "probe", "Gate test only; no independent review or semantic certification.",
                              checklist={key: {"passed": True, "evidence": "Synthetic assertion against final.md and S1.md; length must be checked by the tool"} for key in CHECKLIST})
            return result, checks, errors, (root / "state/final_checklist.json").exists()

    def test_all_five_real_length_failures_reject_false_checklist_passes(self):
        analysis = verify()
        tasks = {t["task_id"]: t for t in h.read(ROOT / "plan.json")["tasks"]}
        failed = [row for row in analysis["rows"] if not row["length"]["within_range"]]
        self.assertEqual(len(failed), 5)
        for row in failed:
            with self.subTest(id=row["id"]):
                report = h.read(ROOT / "attempts" / row["id"] / "parsed.json")["report"]
                result, checks, errors, receipt = self.gate(tasks[row["task_id"]], report)
                self.assertEqual(checks[0]["actual"], row["length"]["actual"])
                self.assertTrue(errors)
                self.assertFalse(result["completed"])
                self.assertFalse(receipt)

    def test_two_editorial_controls_pass_the_existing_length_gate(self):
        tasks = {t["task_id"]: t for t in h.read(ROOT / "plan.json")["tasks"]}
        controls = h.read(ROOT / "editorial-controls.json")["controls"]
        self.assertEqual(len(controls), 2)
        for control in controls:
            with self.subTest(id=control["task_id"]):
                result, checks, errors, receipt = self.gate(tasks[control["task_id"]], control["report"])
                self.assertFalse(errors)
                self.assertTrue(result["completed"], result)
                self.assertTrue(receipt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = verify()
    print(json.dumps({key: result[key] for key in ("requests", "format_valid", "length_valid", "literal_clue_reports", "general_efficacy_established")}))
    if args.self_test:
        unittest.main(argv=[__file__])
