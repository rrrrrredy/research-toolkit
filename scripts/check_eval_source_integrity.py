#!/usr/bin/env python3
"""Fail closed when eval source packs or case references are internally inconsistent."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from check_delivery import resolve_inside, sha256_file


INSUFFICIENT_SOURCE_MARKERS = [
    "无法提供",
    "无法生成符合要求的摘要",
    "无法从中提取",
    "无法提取",
    "实质内容均已被遮蔽",
    "实质性单元格内容均为空白",
]


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_source_policy(path: Path, pack_ids: set[str] | None = None) -> dict[str, dict[str, Any]]:
    policy = read_json(path)
    if not isinstance(policy, dict) or policy.get("schema_version") != 1 or not isinstance(policy.get("packs"), dict):
        raise ValueError(f"{path}: expected source policy version 1 with a packs object")
    entries = policy["packs"]
    if pack_ids is not None:
        entries = {pack_id: entry for pack_id, entry in entries.items() if pack_id in pack_ids}
    for pack_id, entry in entries.items():
        if not isinstance(entry, dict):
            raise ValueError(f"{path}/{pack_id}: expected a pack-policy object")
        if entry.get("factual_authority") is not False:
            raise ValueError(f"{path}/{pack_id}/factual_authority: must be false, including for public_sources")
        expected_purposes = ["workflow", "factual"] if entry.get("kind") == "public_sources" else ["workflow"]
        if entry.get("allowed_purposes") != expected_purposes:
            raise ValueError(f"{path}/{pack_id}/allowed_purposes: use {json.dumps(expected_purposes)} for kind={entry.get('kind')!r}")
        for field in ("kind", "provenance_status", "rights_status"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise ValueError(f"{path}/{pack_id}: missing {field}")
        exclusions = entry.get("excluded_claims", [])
        if not isinstance(exclusions, list):
            raise ValueError(f"{path}/{pack_id}: excluded_claims must be a list")
        for item in exclusions:
            if not isinstance(item, dict) or item.get("field") not in {"summary", "key_points"}:
                raise ValueError(f"{path}/{pack_id}: invalid claim exclusion")
            if any(not isinstance(item.get(key), str) or not item[key].strip() for key in ("source_id", "text", "reason", "evidence")):
                raise ValueError(f"{path}/{pack_id}: claim exclusion lacks its original text or audit evidence")
    return entries


def apply_source_exclusions(rows: list[dict[str, Any]], policy: dict[str, Any]) -> list[dict[str, Any]]:
    """Remove reviewed exact excerpts, preserving caller inputs and the original text in the policy."""
    curated = copy.deepcopy(rows)
    for item in policy.get("excluded_claims", []):
        for row in curated:
            if row.get("source_id") != item["source_id"]:
                continue
            if item["field"] == "key_points":
                row["key_points"] = [value for value in row.get("key_points", []) if value != item["text"]]
            else:
                row["summary"] = str(row.get("summary", "")).replace(item["text"], "")
    return curated


def excluded_claim_findings(rows: list[dict[str, Any]], policy: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    for item in policy.get("excluded_claims", []):
        for row in rows:
            content = str(row.get("summary", "")) + "\n" + "\n".join(str(value) for value in row.get("key_points", []))
            if item["text"] in content:
                findings.append(f"{row.get('source_id')}: an audited excluded claim was reintroduced")
    return findings


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected a JSON object")
            rows.append(value)
    return rows


def contradictory_content(row: dict[str, Any]) -> bool:
    summary = str(row.get("summary", ""))
    key_points = row.get("key_points")
    return (
        isinstance(key_points, list)
        and bool(key_points)
        and any(marker in summary for marker in INSUFFICIENT_SOURCE_MARKERS)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evals-dir", default="evals")
    parser.add_argument("--purpose", choices=("workflow", "factual"), default="workflow")
    parser.add_argument("--case", help="Check one case by its filename stem in evals-dir/cases and only its referenced pack.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    evals_dir = (repo_root / args.evals_dir).resolve()
    failures: list[str] = []
    warnings: list[str] = []
    pack_sources: dict[str, set[str]] = {}
    source_owner: dict[str, str] = {}
    active_count = 0
    quarantined_count = 0
    public_count = 0
    originals_checked = 0
    unavailable_originals = 0

    try:
        packs_dir = evals_dir / "source_packs"
        pack_dirs = sorted(path for path in packs_dir.iterdir() if path.is_dir()) if packs_dir.is_dir() else []
        case_paths = sorted(path for path in (evals_dir / "cases").glob("*.json") if path.is_file())
    except OSError as exc:
        print(f"Eval source integrity failure: cannot enumerate source packs or cases: {exc}")
        return 1

    selected_packs = None
    if args.case is not None:
        case_paths = [path for path in case_paths if path.stem == args.case]
        if not case_paths:
            print(f"Eval source integrity failure: unknown --case {args.case!r}; use a filename stem from {evals_dir / 'cases'}.")
            return 1
        try:
            selected_case = read_json(case_paths[0])
            if not isinstance(selected_case, dict):
                raise ValueError(f"{case_paths[0].name}: case must be an object")
            selected_packs = {str(selected_case.get("source_pack", "")).strip()}
        except (OSError, ValueError) as exc:
            print(f"Eval source integrity failure: {exc}")
            return 1

    try:
        policies = read_source_policy(evals_dir / "source_policy.json", selected_packs)
    except (OSError, ValueError) as exc:
        print(f"Eval source policy failure: {exc}")
        return 1

    if not pack_dirs:
        failures.append("no source pack directories; an empty or missing collection cannot pass integrity checks")
    if not case_paths:
        failures.append("no case files; source-reference coverage was not checked")

    for pack_dir in pack_dirs:
        manifest_path = pack_dir / "manifest.json"
        sources_path = pack_dir / "sources.jsonl"
        if selected_packs is not None:
            try:
                candidate = read_json(manifest_path)
            except (OSError, ValueError):
                continue
            if not isinstance(candidate, dict) or str(candidate.get("source_pack_id", "")).strip() not in selected_packs:
                continue
        if not manifest_path.exists() or not sources_path.exists():
            failures.append(f"{pack_dir}: source pack requires manifest.json and sources.jsonl")
            continue

        try:
            manifest = read_json(manifest_path)
            sources = read_jsonl(sources_path)
            quarantined = read_jsonl(pack_dir / "quarantined_sources.jsonl")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            failures.append(str(exc))
            continue

        if not isinstance(manifest, dict):
            failures.append(f"{manifest_path}: manifest must be an object")
            continue

        pack_id = str(manifest.get("source_pack_id", "")).strip()
        if not pack_id:
            failures.append(f"{manifest_path}: missing source_pack_id")
            continue
        if pack_id in pack_sources:
            failures.append(f"Duplicate source_pack_id: {pack_id}")
            continue
        policy = policies.get(pack_id)
        if policy is None:
            failures.append(f"{pack_id}: no explicit source-use policy")
        else:
            if args.purpose not in policy["allowed_purposes"]:
                failures.append(
                    f"{pack_id}: not eligible for {args.purpose}; allowed_purposes={json.dumps(policy['allowed_purposes'])}. "
                    "Use --purpose workflow for legacy/synthetic packs; use a separate public_sources pack for factual."
                )
            failures.extend(f"{pack_id}/{finding}" for finding in excluded_claim_findings(sources, policy))

        source_ids = [str(row.get("source_id", "")).strip() for row in sources]
        quarantine_ids = [str(row.get("source_id", "")).strip() for row in quarantined]
        if any(not source_id for source_id in source_ids + quarantine_ids):
            failures.append(f"{pack_id}: every source and quarantine row requires source_id")
        if len(source_ids) != len(set(source_ids)):
            failures.append(f"{pack_id}: duplicate active source_id")
        if len(quarantine_ids) != len(set(quarantine_ids)):
            failures.append(f"{pack_id}: duplicate quarantined source_id")
        if set(source_ids) & set(quarantine_ids):
            failures.append(f"{pack_id}: a source_id appears in both active and quarantine files")

        if manifest.get("source_count") != len(sources):
            failures.append(
                f"{pack_id}: manifest source_count={manifest.get('source_count')} but found {len(sources)}"
            )
        if manifest.get("source_ids") != source_ids:
            failures.append(f"{pack_id}: manifest source_ids do not match sources.jsonl order")
        if quarantined or "quarantined_source_count" in manifest:
            if manifest.get("quarantined_source_count") != len(quarantined):
                failures.append(f"{pack_id}: quarantined source count does not match manifest")
            if manifest.get("quarantined_source_ids") != quarantine_ids:
                failures.append(f"{pack_id}: quarantined source ids do not match manifest")

        for row in sources:
            source_id = str(row.get("source_id", ""))
            if policy is not None and policy["kind"] == "public_sources":
                public_count += 1
                for field in ("url", "date", "summary", "retrieved_at", "read_evidence"):
                    if not isinstance(row.get(field), str) or not row[field].strip():
                        failures.append(f"{pack_id}/{source_id}/{field}: use a non-empty string from the source or research record")
                digest = row.get("sha256")
                if not isinstance(digest, str) or len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
                    failures.append(
                        f"{pack_id}/{source_id}/sha256: use the 64 lowercase hex digits returned by "
                        "check_delivery.sha256_file for the complete retrieved original at evidence_path"
                    )
                original = resolve_inside(repo_root, row.get("evidence_path"))
                if original is None:
                    failures.append(
                        f"{pack_id}/{source_id}/evidence_path: use a repository-relative path "
                        "to the complete retrieved original inside the repository"
                    )
                else:
                    try:
                        if not original.is_file():
                            if args.purpose == "factual":
                                failures.append(
                                    f"{pack_id}/{source_id}/evidence_path: complete retrieved original is missing or not a file: "
                                    f"{row['evidence_path']!r}; restore that original for --purpose factual"
                                )
                            else:
                                unavailable_originals += 1
                        elif args.purpose == "factual":
                            actual = sha256_file(original)
                            if actual != digest:
                                failures.append(
                                    f"{pack_id}/{source_id}/sha256: mismatch for evidence_path={row['evidence_path']!r}: "
                                    f"recorded {digest!r}, computed {actual}; restore the reviewed original or independently "
                                    "review the replacement and recompute sha256 with check_delivery.sha256_file"
                                )
                            else:
                                originals_checked += 1
                    except OSError as exc:
                        failures.append(f"{pack_id}/{source_id}/evidence_path: cannot read {row['evidence_path']!r}: {exc}")
            if contradictory_content(row):
                failures.append(
                    f"{pack_id}/{source_id}: summary denies usable content while key_points assert facts"
                )
            if not row.get("date"):
                warnings.append(f"{pack_id}/{source_id}: source date is unavailable")
            previous_owner = source_owner.get(source_id)
            if previous_owner:
                failures.append(
                    f"source_id {source_id} is reused by {previous_owner} and {pack_id}"
                )
            source_owner[source_id] = pack_id

        for row in quarantined:
            source_id = str(row.get("source_id", ""))
            if row.get("usable_for_fact_evaluation") is not False:
                failures.append(f"{pack_id}/{source_id}: quarantined source must be unusable")
            if not str(row.get("quarantine_reason", "")).strip():
                failures.append(f"{pack_id}/{source_id}: quarantined source lacks a reason")

        pack_sources[pack_id] = set(source_ids)
        active_count += len(sources)
        quarantined_count += len(quarantined)

    for pack_id in sorted(set(policies) - set(pack_sources)):
        failures.append(f"{pack_id}: policy references missing source pack")

    for case_path in case_paths:
        try:
            case = read_json(case_path)
        except (OSError, ValueError) as exc:
            failures.append(f"{case_path}: {exc}")
            continue
        if not isinstance(case, dict):
            failures.append(f"{case_path.name}: case must be an object")
            continue
        references = case.get("source_ids")
        if (
            not isinstance(references, list)
            or not references
            or not all(isinstance(value, str) and value.strip() for value in references)
            or len(references) != len(set(references))
        ):
            failures.append(f"{case_path.name}: source_ids must be a non-empty list of distinct non-empty strings")
            continue
        pack_id = str(case.get("source_pack", "")).strip()
        available = pack_sources.get(pack_id)
        if available is None:
            failures.append(f"{case_path.name}: unknown source_pack {pack_id!r}")
            continue
        missing = [source_id for source_id in references if source_id not in available]
        if missing:
            failures.append(
                f"{case_path.name}: references missing or quarantined sources: {', '.join(missing)}"
            )

    if warnings:
        print(f"WARN: {len(warnings)} active source records lack dates.")
    if unavailable_originals:
        print(
            f"INFO: {unavailable_originals} declared local original files are absent; "
            "permitted for workflow, required for factual."
        )
    if failures:
        print("Eval source integrity failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        f"PASS: purpose={args.purpose}; {len(pack_sources)} source packs, {active_count} active sources, "
        f"{quarantined_count} quarantined sources, {len(case_paths)} cases: references checked; "
        f"{public_count} public records: metadata checked; {originals_checked} local originals: hashes checked."
    )
    if public_count:
        print("Content and read_evidence accuracy were not reviewed here; independent research review is required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
