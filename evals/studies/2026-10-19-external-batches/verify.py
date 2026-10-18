"""Read-only checks for the 2026-10-19 external eval ingest. No model calls."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / "2026-10-16-external-batches"

TASK_IDS = [
    "ev-battery-second-life-business-zh-20261016-retest",
    "iIoT-predictive-maintenance-arr-zh-20261016",
    "guide-fund-hardtech-return-ratio-zh-20261016",
    "bank-chatbot-deflection-evidence-en-20261016-retest",
    "scope3-factor-rfq-evidence-en-20261016",
    "regional-bank-llm-credit-memo-controls-en-20261016",
    "bank-wm-structured-marketing-zh-20261017-retest",
    "personal-ai-false-proposition-zh-20261017",
    "bank-llm-explainability-production-bar-zh-20261017",
    "open-weight-saas-lockin-en-20261017-retest",
    "law-firm-llm-signed-advice-bar-en-20261017",
    "explainable-ai-procurement-evidence-bar-en-20261017",
]

DAY16 = "f31345c5a994a8f1574d946388ee58fe1177ede2"
DAY17 = "fedf7cde832139c86cad585883cb5ec2f666427f"

REQUIRED = (
    "case.json",
    "request.json",
    "task_spec.md",
    "final.md",
    "finish.json",
    "check_delivery.out",
    "delivery_message.md",
    "sources/manifest.json",
)

DISCLOSURE_MARKERS = ("合成", "虚构", "synthetic", "fictional")
TEXT_SUFFIXES = {".json", ".md", ".py", ".out", ".txt"}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(path: Path) -> str:
    data = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def disclosed_synthetic(text: str) -> bool:
    lowered = text.lower()
    return any(marker in text or marker in lowered for marker in DISCLOSURE_MARKERS)


def main() -> None:
    manifest = read_json(HERE / "manifest.json")
    require(manifest["task_ids"] == TASK_IDS, "task id list drifted")
    require(manifest["task_count"] == 12, "task_count")
    require(manifest["distinct_research_questions"] == 12, "distinct question count")
    freeze = manifest["freeze_commits"]
    require(freeze["2026-10-16-v1"]["commit"] == DAY16, "2026-10-16-v1 freeze commit")
    require(freeze["2026-10-16-v1"]["version"] == "1.1.0", "2026-10-16-v1 version")
    require(freeze["2026-10-16-v1"]["runs"] == 6, "2026-10-16-v1 runs")
    require(freeze["2026-10-17-v2"]["commit"] == DAY17, "2026-10-17-v2 freeze commit")
    require(freeze["2026-10-17-v2"]["version"] == "1.3.0", "2026-10-17-v2 version")
    require(freeze["2026-10-17-v2"]["runs"] == 6, "2026-10-17-v2 runs")
    require(freeze["2026-10-17-v2"]["day3_baseline_commit"] == DAY16, "v2 baseline")
    require(manifest["excluded"] == [
        "runs/2026-10-14/_superseded-vs-compare",
        "runs/2026-10-14/_superseded-topic-redo-short",
        "eval-queue/2026-10-17-gate/2026-10-17-v1",
        "2026-10-18-v1",
    ], "excluded batches")

    questions = {}
    task_dirs = sorted(path.name for path in (HERE / "tasks").iterdir() if path.is_dir())
    require(task_dirs == sorted(TASK_IDS), "task directory set")
    for row in manifest["tasks"]:
        task_id = row["task_id"]
        root = HERE / "tasks" / task_id
        require(root.is_dir(), "missing task " + task_id)
        for relative in REQUIRED:
            require((root / relative).is_file(), f"{task_id} missing {relative}")
        case = read_json(root / "case.json")
        request = read_json(root / "request.json")
        require(case["task_id"] == task_id, task_id + " case id")
        require(request["task"] == task_id, task_id + " request id")
        require(case["research_question"] == request["brief"]["question"], task_id + " question")
        require(case["research_question"] == row["research_question"], task_id + " manifest question")
        require(case["language"] == request["language"] == row["language"], task_id + " language")
        require(case["profile"] == request["profile"] == row["profile"] == "lite", task_id + " profile")
        require(case["kind"] == row["kind"], task_id + " kind")
        require(case["independent_review"] is False, task_id + " independence flag")
        require(case["factual_authority"] is False, task_id + " factual authority")
        require(case["sources_disclosed_synthetic"] is True, task_id + " synthetic flag")
        require(case["review_mode"] == "author_self_check" == row["review_mode"], task_id + " review mode")
        require(case["revisions"] == 0 == row["revisions"], task_id + " revisions")
        expected_commit = DAY17 if row["batch_id"] == "2026-10-17-v2" else DAY16
        expected_version = "1.3.0" if row["batch_id"] == "2026-10-17-v2" else "1.1.0"
        require(case["toolkit_commit"] == expected_commit == row["toolkit_commit"], task_id + " commit")
        require(case["toolkit_version"] == expected_version == row["toolkit_version"], task_id + " version")
        mechanical = case["mechanical"]
        require(mechanical["lite_checklist"] == "checklist_complete", task_id + " checklist field")
        require(mechanical["full_delivery_gate"] == "skipped", task_id + " full gate")
        require(mechanical["research_review"] == "skipped", task_id + " research review")
        require(mechanical["semantic_quality_certified"] is False, task_id + " semantic flag")
        pack = read_json(root / "sources" / "manifest.json")
        require(pack["source_pack_id"] == task_id, task_id + " pack id")
        require(pack["kind"] == "synthetic" and pack["factual_authority"] is False, task_id + " pack")
        source_files = sorted((root / "sources").glob("S*.md"))
        require([path.stem for path in source_files] == pack["source_ids"] == row["source_ids"], task_id + " source ids")
        require(source_files, task_id + " has no sources")
        for path in source_files:
            require(disclosed_synthetic(path.read_text(encoding="utf-8")), "source missing synthetic disclosure: " + str(path))
        check = (root / "check_delivery.out").read_text(encoding="utf-8")
        require("Lite checklist: checklist_complete" in check, task_id + " checklist")
        require("SKIP research_review: profile=lite" in check, task_id + " skipped review")
        require("PASS: mechanical delivery checks" not in check, task_id + " unexpected full pass")
        copied = row["copied_unchanged_from"]
        require(case["copied_unchanged_from"] == copied == pack["copied_unchanged_from"], task_id + " lineage id")
        if copied:
            provenance = root / "sources" / "COPY_PROVENANCE.txt"
            require(provenance.is_file(), task_id + " provenance")
            require(copied in provenance.read_text(encoding="utf-8"), task_id + " provenance names earlier pack")
            prior_root = PRIOR / "tasks" / copied
            require(prior_root.is_dir(), "missing earlier pack " + copied)
            prior_case = read_json(prior_root / "case.json")
            same = prior_case["research_question"] == case["research_question"]
            require(same is row["question_text_identical_to_copied_pack"], task_id + " question lineage")
            require(same is case["question_text_identical_to_copied_pack"], task_id + " case question lineage")
            prior_files = sorted((prior_root / "sources").glob("S*.md"))
            require([path.name for path in prior_files] == [path.name for path in source_files], task_id + " lineage names")
            for prior_path, path in zip(prior_files, source_files):
                require(digest(prior_path) == digest(path), task_id + " source bytes drifted from " + copied)
        else:
            require(not (root / "sources" / "COPY_PROVENANCE.txt").exists(), task_id + " unexpected provenance")
            require(row["question_text_identical_to_copied_pack"] is None, task_id + " lineage flag")
        if row["batch_id"] == "2026-10-17-v2":
            require(row["outer_grok_note"] is True, task_id + " outer flag")
            require(mechanical["outer_grok_note"] == "recorded_pass_not_toolkit_independent_review", task_id + " outer field")
            review = (root / "review" / "outer_grok_review.md").read_text(encoding="utf-8")
            require(review.startswith("# 外层 Grok 评价"), task_id + " outer heading")
            require("非 Full" in review and "达标" in review, task_id + " outer boundary")
        else:
            require(row["outer_grok_note"] is False, task_id + " outer flag")
            require(mechanical["outer_grok_note"] is None, task_id + " outer field")
            require(not (root / "review").exists(), task_id + " unexpected review")
        questions[task_id] = case["research_question"]

    require(len(set(questions.values())) == 12, "distinct questions")
    lineage = manifest["question_lineage"]
    require(len(lineage) == 4, "lineage rows")
    for item in lineage:
        require(item["task_id"] in questions, "lineage task")
        earlier = read_json(PRIOR / "tasks" / item["earlier_task_id"] / "case.json")
        same = earlier["research_question"] == questions[item["task_id"]]
        require(same is item["same_question_text"], item["task_id"] + " lineage note")

    for relative in (
        "batches/2026-10-16-confirmed/DAILY_BRIEF.md",
        "batches/2026-10-16-confirmed/SUMMARY.json",
        "batches/2026-10-17-confirmed/DAILY_BRIEF.md",
        "batches/2026-10-17-confirmed/SUMMARY.json",
        "batches/2026-10-17-confirmed/OUTER_REVIEW_BATCH_SUMMARY.md",
    ):
        require((HERE / relative).is_file(), "missing " + relative)
    day16 = read_json(HERE / "batches/2026-10-16-confirmed/SUMMARY.json")
    day17 = read_json(HERE / "batches/2026-10-17-confirmed/SUMMARY.json")
    require(day16["toolkit_commit"] == DAY16 and day16["toolkit_version"] == "1.1.0", "day16 summary")
    require(day17["toolkit_commit"] == DAY17 and day17["toolkit_version"] == "1.3.0", "day17 summary")
    require(day16["batch"] == "2026-10-16-v1" and day17["batch"] == "2026-10-17-v2", "summary batch ids")
    require("unavailable" in day16["independent_review_backend"], "day16 backend")
    require("unavailable" in day17["independent_review_backend"], "day17 backend")
    require(day17["prior_batch_superseded"] == "2026-10-17-v1", "v1 superseded marker")
    require([row["task"] for row in day16["results"]] == TASK_IDS[:6], "day16 order")
    require([row["task"] for row in day17["results"]] == TASK_IDS[6:], "day17 order")
    outer = (HERE / "batches/2026-10-17-confirmed/OUTER_REVIEW_BATCH_SUMMARY.md").read_text(encoding="utf-8")
    require("非 Full" in outer or "≠ Full" in outer, "outer summary boundary")
    for task_id in TASK_IDS[6:]:
        require(task_id in outer, "outer summary missing " + task_id)

    for path in HERE.rglob("*"):
        posix = path.relative_to(HERE).as_posix()
        require("_superseded" not in posix, "superseded material ingested: " + posix)
        require("2026-10-18" not in posix, "next window ingested: " + posix)
        require("v1-superseded" not in posix, "v1 gate ingested: " + posix)

    for name in ("README.md", "README.zh-CN.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        require(DAY16 in text and DAY17 in text, name + " freeze commits")
        for task_id in TASK_IDS:
            require(task_id in text, name + " missing " + task_id)
            require(questions[task_id] in text, name + " missing question for " + task_id)
        require("synthetic" in text.lower() or "合成" in text, name + " synthetic disclosure")
        require("2026-10-18-v1" in text, name + " next-window exclusion")
        require("2026-10-17-v1" in text, name + " v1 exclusion")

    hashes = read_json(HERE / "artifact-hashes.json")
    files = {
        path.relative_to(HERE).as_posix()
        for path in HERE.rglob("*")
        if path.is_file() and path.name != "artifact-hashes.json" and "__pycache__" not in path.parts
    }
    require(files == set(hashes), "public file inventory changed")
    for name, expected in hashes.items():
        require(digest(HERE / name) == expected, "changed public bytes: " + name)
    print("PASS: 12 external eval runs, freeze commits, synthetic sources, Lite mechanical outcomes")


if __name__ == "__main__":
    main()
