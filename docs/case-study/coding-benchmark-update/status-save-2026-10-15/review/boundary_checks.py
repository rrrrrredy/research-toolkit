"""Independent review probes. Writes only disposable tasks and reviewer output."""
from pathlib import Path
import hashlib
import json
import sys
import tempfile
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / 'research-toolkit/scripts'))
import research_workflow as w
import research_records as rr
from check_research_workflow import BRIEF
from check_delivery import inspect_reading_evidence

results = []

def record(name, passed, evidence):
    results.append({'name': name, 'passed': passed, 'evidence': evidence})

with tempfile.TemporaryDirectory(prefix='ar-', dir=BASE / 'a14tmp') as d:
    workspace = Path(d)
    for task, locator in [('plain', 'source.md'), ('anchor', 'source.md#L1'),
                          ('markdown', '[reading](source.md#L1)'), ('page', 'source.md:1')]:
        w.start(workspace, task, BRIEF, profile='lite')
        root = workspace / task
        (root / 'source.md').write_text('Twelve shipments.', encoding='utf-8')
        seed = w.save_records(workspace, task,
            sources=[{'source_id': 'S1', 'title': 'Source', 'url': 'https://example.org/source',
                      'source_type': 'primary', 'read_scope': 'full_text', 'read_evidence': locator}],
            claims=[{'claim_id': 'C1', 'claim': 'Twelve shipments', 'claim_type': 'fact', 'supporting_sources': ['S1']}],
            draft={'path': 'final.md', 'content': '# Result\nTwelve shipments [source](https://example.org/source).', 'complete': True})
        assert seed['ok'], seed
        (root / 'source.md').write_text('Thirteen shipments.', encoding='utf-8')
        changed = w.save_records(workspace, task, sources=[{'source_id': 'S1'}])
        changes = changed['changes']
        record('source_locator_' + task,
               changes['source_files']['S1']['status'] == 'changed' and bool(changes['affected_claims']),
               {'locator': locator, 'existing_reading_validator_errors': inspect_reading_evidence(root, locator),
                'save_ok': changed['ok'], 'changes': changes})

    root = workspace / 'plain'
    # Per-source observations survive intervening batches for other collections.
    w.save_records(workspace, 'plain', requirements=[{'summary': 'Explain shipments', 'status': 'pending'}])
    again = w.save_records(workspace, 'plain', sources=[{'source_id': 'S1'}])
    record('per_source_history_after_other_batch', again['changes']['source_files']['S1']['status'] == 'unchanged', again['changes']['source_files'])

    # New optimization must not corrupt rollback when first planned file is skipped.
    before = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}
    real_replace = rr.os.replace
    calls = []
    def fail_second(src, dst):
        calls.append(str(dst))
        if len(calls) == 2:
            raise OSError('reviewer controlled write failure')
        return real_replace(src, dst)
    with patch.object(rr.os, 'replace', side_effect=fail_second):
        mixed = w.save_records(workspace, 'plain', sources=[{'source_id': 'S1'}],
            claims=[{'claim_id': 'C1', 'claim': 'Revised'}], draft={'path': 'final.md', 'content': 'Changed report.'})
    payloads = ['data/source_registry.csv', 'data/claims_registry.csv', 'final.md']
    record('rollback_with_skipped_identical_first_plan', not mixed['ok'] and all((root / p).read_bytes() == before[p] for p in payloads),
           {'result': mixed, 'replace_targets': calls})

    # Read-only status must not alter bytes or mtimes.
    before = {p.relative_to(root).as_posix(): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
              for p in root.rglob('*') if p.is_file()}
    w.status(workspace, 'plain')
    after = {p.relative_to(root).as_posix(): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
             for p in root.rglob('*') if p.is_file()}
    record('status_bytes_and_mtime_read_only', before == after, {'files_checked': len(before)})

    # Invalid source path must remain unobserved rather than read outside task.
    from record_changes import source_files
    record('source_file_boundary', source_files(root, {'read_evidence': '../outside.md'}) == {}, {'path': '../outside.md'})

out = {'checks': results, 'passed': sum(r['passed'] for r in results), 'failed': sum(not r['passed'] for r in results)}
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(1 if out['failed'] else 0)
