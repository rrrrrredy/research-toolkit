"""Read-only checks for the 2026-10-16 external eval ingest. No model calls."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

TASK_IDS = [
    "api-price-war-cloud-bundling-zh-retest-20261014",
    "enterprise-kb-llm-liability-zh-20261014",
    "ev-battery-second-life-business-zh-20261014",
    "bank-chatbot-deflection-evidence-en-retest-20261014",
    "open-weight-saas-lockin-en-20261014",
    "private-credit-onchain-settlement-en-20261014",
    "enterprise-kb-llm-liability-zh-20261015-full",
    "dongshu-xisuan-training-procurement-zh-20261015",
    "bank-wm-structured-marketing-zh-20261015",
    "private-credit-onchain-settlement-en-20261015-full",
    "saas-frontier-ai-pricing-residency-en-20261015",
    "tokenized-deposit-cash-equivalent-en-20261015",
]

FULL_IDS = {
    "enterprise-kb-llm-liability-zh-20261015-full",
    "private-credit-onchain-settlement-en-20261015-full",
}

DAY1 = "45bfc5e38f62f563bb8b800acbdbcb3fd2e27bd3"
DAY2 = "f31345c5a994a8f1574d946388ee58fe1177ede2"

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


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


# Text evidence is hashed as LF. Windows checkouts may rewrite these suffixes to CRLF.
TEXT_SUFFIXES = {".json", ".md", ".py", ".out", ".txt"}


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
    require(manifest["distinct_research_questions"] == 10, "distinct question count")
    freeze = manifest["freeze_commits"]
    require(freeze["2026-10-14"]["commit"] == DAY1, "Day-1 freeze commit")
    require(freeze["2026-10-14"]["version"] == "1.0.0", "Day-1 version")
    require(freeze["2026-10-15-v1"]["commit"] == DAY2, "Day-2 freeze commit")
    require(freeze["2026-10-15-v1"]["version"] == "1.1.0", "Day-2 version")
    require(freeze["2026-10-15-v1"]["day1_baseline_commit"] == DAY1, "Day-2 baseline")
    require(manifest["excluded"] == [
        "runs/2026-10-14/_superseded-vs-compare",
        "runs/2026-10-14/_superseded-topic-redo-short",
    ], "excluded batches")

    questions = {}
    for row in manifest["tasks"]:
        task_id = row["task_id"]
        root = HERE / "tasks" / task_id
        require(root.is_dir(), "missing task " + task_id)
        for relative in REQUIRED:
            require((root / relative).is_file(), f"{task_id} missing {relative}")
        case = read_json(root / "case.json")
        request = read_json(root / "request.json")
        require(case["task_id"] == task_id, task_id + " case id")
        require(case["research_question"] == request["brief"]["question"], task_id + " question")
        require(case["research_question"] == row["research_question"], task_id + " manifest question")
        require(case["language"] == request["language"] == row["language"], task_id + " language")
        require(case["profile"] == request["profile"] == row["profile"], task_id + " profile")
        require(case["independent_review"] is False, task_id + " independence flag")
        require(case["factual_authority"] is False, task_id + " factual authority")
        require(case["sources_disclosed_synthetic"] is True, task_id + " synthetic flag")
        expected_commit = DAY2 if row["batch_id"] == "2026-10-15-v1" else DAY1
        require(case["toolkit_commit"] == expected_commit == row["toolkit_commit"], task_id + " commit")
        pack = read_json(root / "sources" / "manifest.json")
        require(pack["source_pack_id"] == task_id, task_id + " pack id")
        require(pack["kind"] == "synthetic" and pack["factual_authority"] is False, task_id + " pack")
        source_files = sorted((root / "sources").glob("S*.md"))
        require([path.stem for path in source_files] == pack["source_ids"] == row["source_ids"], task_id + " source ids")
        require(source_files, task_id + " has no sources")
        for path in source_files:
            require(disclosed_synthetic(path.read_text(encoding="utf-8")), "source missing synthetic disclosure: " + str(path))
        check = (root / "check_delivery.out").read_text(encoding="utf-8")
        if task_id in FULL_IDS:
            require(case["profile"] == "full", task_id + " profile")
            require(case["review_mode"] == "same_session_degraded", task_id + " review mode")
            require("PASS: mechanical delivery checks" in check, task_id + " mechanical pass")
            review = (root / "review" / "same_session_review.md").read_text(encoding="utf-8")
            require(review.startswith("# Same-session review (NOT independent)"), task_id + " review heading")
            require("degraded" in review.lower(), task_id + " degraded")
            require("not independent" in review.lower() or "非独立" in review, task_id + " non-independence")
            require((root / "sources" / "COPY_PROVENANCE.txt").is_file(), task_id + " provenance")
        else:
            require(case["profile"] == "lite", task_id + " profile")
            require(case["review_mode"] == "author_self_check", task_id + " review mode")
            require("Lite checklist: checklist_complete" in check, task_id + " checklist")
            require(not (root / "review").exists(), task_id + " unexpected review")
        questions[task_id] = case["research_question"]

    pairs = manifest["repeated_research_questions"]
    require(len(pairs) == 2, "repeated pairs")
    for pair in pairs:
        ids = pair["task_ids"]
        require(len(ids) == 2 and questions[ids[0]] == questions[ids[1]], "repeated question mismatch")
    require(len(set(questions.values())) == 10, "distinct questions")

    for relative in (
        "batches/2026-10-14-confirmed/DAILY_BRIEF.md",
        "batches/2026-10-14-confirmed/SUMMARY.json",
        "batches/2026-10-15-confirmed/DAILY_BRIEF.md",
        "batches/2026-10-15-confirmed/SUMMARY.json",
    ):
        require((HERE / relative).is_file(), "missing " + relative)
    day1 = read_json(HERE / "batches/2026-10-14-confirmed/SUMMARY.json")
    day2 = read_json(HERE / "batches/2026-10-15-confirmed/SUMMARY.json")
    require(day1["toolkit_commit"] == DAY1 and day2["toolkit_commit"] == DAY2, "summary commits")
    require(day2["independent_review_backend"] == "unavailable", "backend availability")
    require("not independent" in day2["full_review_mode_actual"], "summary review mode")
    require([row["task"] for row in day1["results"]] == TASK_IDS[:6], "day-1 order")
    require([row["task"] for row in day2["results"]] == TASK_IDS[6:], "day-2 order")

    for path in HERE.rglob("*"):
        require("_superseded" not in path.as_posix(), "superseded material ingested: " + path.as_posix())

    hashes = read_json(HERE / "artifact-hashes.json")
    files = {
        path.relative_to(HERE).as_posix()
        for path in HERE.rglob("*")
        if path.is_file() and path.name != "artifact-hashes.json" and "__pycache__" not in path.parts
    }
    require(files == set(hashes), "public file inventory changed")
    for name, expected in hashes.items():
        require(digest(HERE / name) == expected, "changed public bytes: " + name)
    print("PASS: 12 external eval runs, freeze commits, synthetic sources, degraded Full review")


if __name__ == "__main__":
    main()
