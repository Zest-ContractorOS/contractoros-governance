#!/usr/bin/env python3
"""H1-B1C FULL_TREE_SCANNER (ART-FUTURE-FULL_TREE_SCANNER instantiation).

Compares the actual tracked repository tree against the governing-files
corpus entries. Fails closed on: unclassified tracked files, classified
EXISTS entries missing from the tree, duplicate path classifications, or
entry-count mismatch.

Read-only. Exit 0 = PASS, exit 1 = validation failure, exit 2 = environment
failure (fail closed; no fallback derivation).
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOVERNING_FILES = ROOT / "policy/corpus/governing-files.json"


def fail_env(message):
    print(json.dumps({"result": "ENVIRONMENT_FAILURE", "error": message}))
    return 2


def main():
    failures = []

    if not GOVERNING_FILES.exists():
        return fail_env("CORPUS_FILE_MISSING: policy/corpus/governing-files.json")
    try:
        doc = json.loads(GOVERNING_FILES.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return fail_env(f"CORPUS_PARSE_FAILURE: {exc}")

    proc = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        return fail_env("GIT_LS_FILES_FAILED: cannot enumerate the tracked tree.")
    tree = sorted(line.strip() for line in proc.stdout.splitlines() if line.strip())

    entries = doc.get("entries", [])
    expected_count = doc.get("expected_entry_count")
    if expected_count is not None and expected_count != len(entries):
        failures.append(
            f"ENTRY_COUNT_MISMATCH: expected_entry_count={expected_count} but entries={len(entries)}"
        )

    classified = {}
    for entry in entries:
        if entry.get("locator_type") != "REPOSITORY_PATH":
            continue
        path = entry.get("exact_path")
        if not path:
            failures.append(f"ENTRY_WITHOUT_EXACT_PATH: {entry.get('artifact_id', '?')}")
            continue
        if path in classified:
            failures.append(
                f"DUPLICATE_CLASSIFICATION: {path} ({classified[path]} and {entry.get('artifact_id', '?')})"
            )
        classified[path] = entry.get("artifact_id", "?")
        if entry.get("existence_status") == "EXISTS" and path not in tree:
            failures.append(
                f"CLASSIFIED_FILE_MISSING_FROM_TREE: {path} ({entry.get('artifact_id', '?')})"
            )

    exists_paths = {
        e.get("exact_path")
        for e in entries
        if e.get("locator_type") == "REPOSITORY_PATH" and e.get("existence_status") == "EXISTS"
    }
    for path in tree:
        if path not in exists_paths:
            failures.append(f"UNCLASSIFIED_TRACKED_FILE: {path}")

    report = {
        "result": "FAIL" if failures else "PASS",
        "tracked_file_count": len(tree),
        "classified_exists_count": len(exists_paths),
        "failures": failures,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
