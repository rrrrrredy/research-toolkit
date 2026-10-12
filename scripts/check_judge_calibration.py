#!/usr/bin/env python3
"""Read-only checks for public judge controls; no model calls or quality verdicts."""
import argparse
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
import unittest


DEFAULT_PACK = Path(__file__).resolve().parents[1] / "evals/tasksets/judge-calibration-v3"
HASH_METHOD = ("SHA-256 of parsed packet JSON serialized with sorted keys, UTF-8, "
               "ensure_ascii=false, compact separators. File whitespace/newline changes "
               "do not alter packet identity.")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text_value(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label}: nonempty text required")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON field: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"Non-JSON constant: {value}")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def packet_hash(packet):
    return hashlib.sha256(json.dumps(packet, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def length(value, unit):
    if unit == "whitespace_words":
        return len(value.split())
    require(unit == "nonwhitespace_characters", "Unknown length measurement")
    return sum(not char.isspace() for char in value)


def packet_path(base, name):
    text_value(name, "Packet path")
    relative = PurePosixPath(name)
    require(not relative.is_absolute() and ".." not in relative.parts and
            "\\" not in name and ":" not in name, "Packet path must stay inside tasksets")
    target = (base / relative).resolve()
    require(target.is_relative_to(base.resolve()) and target.is_file(),
            "Packet path must name a file inside tasksets")
    return target


def check_packet(packet):
    require(isinstance(packet, dict) and set(packet) == {"brief", "sources", "rubric", "reports"},
            "Judge packet must contain only brief, sources, rubric and reports")
    text_value(packet["brief"], "Brief")
    require(isinstance(packet["rubric"], dict) and bool(packet["rubric"]), "Missing rubric")
    sources = packet["sources"]
    require(isinstance(sources, list) and bool(sources), "Missing sources")
    ids = set()
    for source in sources:
        require(isinstance(source, dict) and set(source) == {"id", "text"},
                "Source must contain only id and text")
        text_value(source["id"], "Source ID")
        text_value(source["text"], "Source text")
        require(source["id"] not in ids, "Duplicate source ID")
        ids.add(source["id"])
    reports = packet["reports"]
    require(isinstance(reports, dict) and set(reports) == {"A", "B"}, "Expected A/B reports")
    for value in reports.values():
        text_value(value, "Report")


def verify_pack(pack=DEFAULT_PACK):
    pack = Path(pack)
    manifest = read(pack / "coordinator-manifest.json")
    require(isinstance(manifest, dict), "Manifest must be an object")
    require(type(manifest.get("schema_version")) is int and manifest["schema_version"] == 1,
            "Unsupported manifest schema")
    require(manifest.get("role") == "judge_calibration" and
            manifest.get("cohort_status") == "exposed_development", "Expected exposed calibration controls")
    require(manifest.get("hash_method") == HASH_METHOD, "Unknown packet hash method")
    for key in ("acceptance", "limitations"):
        text_value(manifest.get(key), key)
    families = manifest.get("families")
    require(isinstance(families, list) and bool(families), "Missing families")
    require(type(manifest.get("independent_families")) is int and
            manifest["independent_families"] == len(families), "Family count mismatch")
    require(type(manifest.get("judge_requests_per_model")) is int and
            manifest["judge_requests_per_model"] == 3 * len(families), "Request count mismatch")
    seen_ids, seen_paths = set(), set()
    for family in families:
        require(isinstance(family, dict), "Family must be an object")
        identifier = family.get("family_id")
        text_value(identifier, "Family ID")
        require(identifier not in seen_ids, "Duplicate family ID")
        seen_ids.add(identifier)
        for key in ("origin", "validity_basis"):
            text_value(family.get(key), f"{identifier}: {key}")
        exposure = family.get("exposure")
        require(isinstance(exposure, list) and bool(exposure), "Missing exposure history")
        for item in exposure:
            text_value(item, "Exposure history")
        language, unit = family.get("language"), family.get("measurement")
        require(language in ("en", "zh-CN") and unit == {
            "en": "whitespace_words", "zh-CN": "nonwhitespace_characters"
        }[language], "Language/measurement mismatch")
        refs = family.get("packets")
        require(isinstance(refs, dict) and set(refs) == {"primary", "swapped", "valid_tie"},
                "Expected primary, swapped and valid_tie packets")
        packets = {}
        for role, ref in refs.items():
            require(isinstance(ref, dict) and set(ref) == {"path", "sha256", "expected_preference"},
                    "Invalid packet reference")
            path = packet_path(pack.parent, ref["path"])
            require(path not in seen_paths, "Packet reused across manifest entries")
            seen_paths.add(path)
            packet = read(path)
            check_packet(packet)
            require(isinstance(ref["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", ref["sha256"])
                    and packet_hash(packet) == ref["sha256"], f"Packet hash mismatch: {ref['path']}")
            packets[role] = packet
        primary, swapped, tie = (packets[role] for role in ("primary", "swapped", "valid_tie"))
        for role in ("swapped", "valid_tie"):
            require(all(packets[role][key] == primary[key] for key in ("brief", "sources", "rubric")),
                    f"{identifier}: shared brief/sources/rubric changed")
        label = refs["primary"]["expected_preference"]
        require(label in ("A", "B"), "Primary preference must be A or B")
        other = "B" if label == "A" else "A"
        require(refs["swapped"]["expected_preference"] == other and
                refs["valid_tie"]["expected_preference"] == "tie", "Expected preference mismatch")
        valid, defect = primary["reports"][label], primary["reports"][other]
        require(valid != defect, "Primary reports must differ")
        require(swapped["reports"] == {"A": primary["reports"]["B"], "B": primary["reports"]["A"]},
                f"{identifier}: reports not swapped exactly")
        require(tie["reports"] == {"A": valid, "B": valid}, f"{identifier}: tie must duplicate valid report")
        counts = family.get("length_counts")
        actual = {"valid": length(valid, unit), "defect": length(defect, unit)}
        require(isinstance(counts, dict) and set(counts) == set(actual) and
                all(type(n) is int for n in counts.values()) and counts == actual,
                f"{identifier}: length counts mismatch")
        require(actual["valid"] == actual["defect"], f"{identifier}: reports are not length matched")
        known = family.get("known_defect")
        require(isinstance(known, dict), "Missing known defect")
        for key in ("report_excerpt", "source_id", "source_excerpt", "explanation"):
            text_value(known.get(key), f"Known defect: {key}")
        require(known["report_excerpt"] in defect and known["report_excerpt"] not in valid,
                f"{identifier}: defect excerpt does not distinguish the reports")
        sources = {source["id"]: source["text"] for source in primary["sources"]}
        require(known["source_id"] in sources and known["source_excerpt"] in sources[known["source_id"]],
                f"{identifier}: source excerpt not located")
    return {"structural_check": "passed", "families": len(families), "packets": len(seen_paths),
            "model_calls": 0, "judge_reliability": "not_evaluated"}


class CalibrationControlsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        for name in ("judge-calibration-v2", "judge-calibration-v3"):
            shutil.copytree(DEFAULT_PACK.parent / name, self.base / name)
        self.pack = self.base / "judge-calibration-v3"
        self.manifest = read(self.pack / "coordinator-manifest.json")
        self.family = self.manifest["families"][1]

    def save(self, path, value):
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")

    def verify(self):
        self.save(self.pack / "coordinator-manifest.json", self.manifest)
        return verify_pack(self.pack)

    def change_packet(self, role, change, reseal=True):
        ref = self.family["packets"][role]
        path = self.base / ref["path"]
        packet = read(path)
        change(packet)
        self.save(path, packet)
        if reseal:
            ref["sha256"] = packet_hash(packet)

    def test_read_only_valid_pack(self):
        before = {p: p.read_bytes() for p in self.base.rglob("*") if p.is_file()}
        result = verify_pack(self.pack)
        self.assertEqual((result["families"], result["packets"], result["model_calls"]), (4, 12, 0))
        self.assertEqual(result["judge_reliability"], "not_evaluated")
        self.assertEqual(before, {p: p.read_bytes() for p in self.base.rglob("*") if p.is_file()})

    def test_hash_and_checkout_line_endings(self):
        path = self.base / self.family["packets"]["primary"]["path"]
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        verify_pack(self.pack)
        self.change_packet("primary", lambda p: p.update(brief=p["brief"] + " changed"), reseal=False)
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            self.verify()

    def test_bad_swap_with_resealed_hash(self):
        primary = read(self.base / self.family["packets"]["primary"]["path"])
        self.change_packet("swapped", lambda p: p.update(reports=primary["reports"]))
        with self.assertRaisesRegex(ValueError, "not swapped"):
            self.verify()

    def test_false_tie_with_resealed_hash(self):
        self.change_packet("valid_tie", lambda p: p["reports"].update(B="Different report"))
        with self.assertRaisesRegex(ValueError, "tie must duplicate"):
            self.verify()

    def test_coordinator_metadata_is_not_packet_content(self):
        self.change_packet("primary", lambda p: p.update(expected_preference="B"))
        with self.assertRaisesRegex(ValueError, "must contain only"):
            self.verify()

    def test_shared_inputs_cannot_drift(self):
        for key, value in (("brief", "Changed brief"), ("rubric", {"changed": True}),
                           ("sources", [{"id": "S1", "text": "Changed evidence"}])):
            with self.subTest(key=key):
                original = copy.deepcopy(self.manifest)
                path = self.base / self.family["packets"]["swapped"]["path"]
                raw = path.read_bytes()
                self.change_packet("swapped", lambda p: p.update({key: value}))
                with self.assertRaisesRegex(ValueError, "shared brief/sources/rubric"):
                    self.verify()
                path.write_bytes(raw)
                self.manifest = original
                self.family = self.manifest["families"][1]

    def test_chinese_counts_and_unit(self):
        self.family["length_counts"] = {"valid": 3, "defect": 3}
        with self.assertRaisesRegex(ValueError, "length counts mismatch"):
            self.verify()
        self.family["measurement"] = "whitespace_words"
        with self.assertRaisesRegex(ValueError, "Language/measurement"):
            self.verify()

    def test_answer_and_source_locations(self):
        original = copy.deepcopy(self.family["known_defect"])
        for key, message in (("report_excerpt", "defect excerpt"), ("source_excerpt", "source excerpt")):
            self.family["known_defect"] = {**original, key: "MISSING_EXCERPT"}
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, message):
                self.verify()

    def test_path_escape(self):
        for name in ("../outside.json", "/outside.json", "C:/outside.json", "..\\outside.json"):
            self.family["packets"]["primary"]["path"] = name
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "inside tasksets"):
                self.verify()

    def test_counts_and_duplicate_family(self):
        self.manifest["judge_requests_per_model"] = 4
        with self.assertRaisesRegex(ValueError, "Request count"):
            self.verify()
        self.manifest["judge_requests_per_model"] = 12
        self.family["family_id"] = self.manifest["families"][0]["family_id"]
        with self.assertRaisesRegex(ValueError, "Duplicate family"):
            self.verify()

    def test_duplicate_json_fields(self):
        path = self.base / self.family["packets"]["primary"]["path"]
        path.write_text('{"brief":"one","brief":"two"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate JSON"):
            self.verify()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack", type=Path, default=DEFAULT_PACK)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify_pack(args.pack), ensure_ascii=False))
    if args.self_test:
        result = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(CalibrationControlsTests))
        if not result.wasSuccessful():
            raise SystemExit(1)


if __name__ == "__main__":
    main()
