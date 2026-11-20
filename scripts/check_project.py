"""Run the repository checks locally or in CI (Python 3.11+, Node and requirements-mcp.txt)."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = (
    'scripts/check_agent_matrix.py',
    'scripts/check_claim_consistency.py',
    'scripts/check_published_evidence.py',
    'scripts/check_version.py --self-test',
    'scripts/check_docs_sync.py',
    'scripts/check_docs_sync.py --skill SKILL.zh-CN.md --html docs/framework.zh-CN.html',
    'scripts/run_dsh_evals.py validate',
    'scripts/check_eval_source_integrity.py',
    'scripts/check_source_policy_contract.py',
    'scripts/check_source_extraction.py',
    'scripts/check_regression_fixtures.py',
    'scripts/check_conformance_fixtures.py',
    'scripts/check_delivery_contract.py',
    'scripts/check_review_completion_contract.py',
    'scripts/check_evaluator_contract.py',
    'scripts/check_semantic_diagnostics.py',
    'scripts/check_installation_contract.py',
    'scripts/check_diagnostic_bundle.py --self-test',
    'scripts/check_semantic_review_bundle.py --self-test',
    'scripts/check_research_workflow.py',
    'scripts/check_draft_contract.py',
    'scripts/check_record_workflow.py',
    'scripts/check_task_continuity.py',
    'scripts/check_release_updates.py',
    'scripts/check_task_lock.py',
    'scripts/check_profiles_reviewers.py',
    'scripts/check_usage_sharing.py',
    'scripts/check_host_execution.py',
    'scripts/build_plugin.py --check',
    'scripts/check_plugin_build.py',
    'scripts/check_mcp_contract.py',
    'scripts/check_blinded_evals.py',
    'scripts/check_blinded_protocol_v2.py',
    'scripts/check_judge_calibration.py --self-test',
    'scripts/check_live_execution.py',
    'scripts/check_live_diagnostics.py',
    'scripts/check_development_evidence.py --self-test',
    'scripts/check_feedback_probes.py --self-test',
    'evals/diagnostics/2026-10-13-targeted-recheck/verify.py',
    'evals/diagnostics/2026-10-13-dedicated-seven/verify.py',
    'evals/repairs/2026-10-13-pipeline-complete/verify.py',
    'evals/studies/2026-10-13-before-after/verify.py',
    'evals/studies/2026-10-14-native-agent/verify.py',
    'evals/studies/2026-10-16-external-batches/verify.py',
    'evals/studies/2026-10-19-external-batches/verify.py',
    'evals/studies/2026-10-21-external-batches/verify.py',
    'scripts/check_study_verification.py',
)
SITE = (
    'scripts/build_site.py --check',
    'scripts/check_site.py --self-test',
    'node --check docs/assets/reading-preferences.js',
    'node --check docs/assets/showcase.js',
)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", choices=["all", "runtime", "site"], default="all")
    group = parser.parse_args().group
    commands = (SITE if group in ("all", "site") else ()) + (RUNTIME if group in ("all", "runtime") else ())
    env = {**os.environ, "PYTHONUTF8": "1", "RESEARCH_TOOLKIT_TELEMETRY": "off"}
    for command in commands:
        args = command.split()
        if args[0] != "node":
            args.insert(0, sys.executable)
        print("+ " + command, flush=True)
        result = subprocess.run(args, cwd=ROOT, env=env)
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
