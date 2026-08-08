#!/usr/bin/env python3
"""H1-B1C VALIDATOR (ART-FUTURE-VALIDATOR instantiation).

Validates the governance corpus documents themselves: every instance against
its schema, rule-ID uniqueness across documents, and supersession-reference
resolution. Tree-vs-corpus comparison lives in scripts/scan_tree.py
(FULL_TREE_SCANNER); the two run together in CI.

Read-only. Exit 0 = PASS, exit 1 = validation failure, exit 2 = environment
failure (fail closed; no fallback derivation).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CORPUS = {
    "governance-hierarchy": "policy/corpus/governance-hierarchy.json",
    "classifications": "policy/corpus/classifications.json",
    "governing-files": "policy/corpus/governing-files.json",
    "supersession": "policy/corpus/supersession.json",
    "ownership": "policy/corpus/ownership.json",
}
SCHEMAS = {name: f"schemas/governance/{name}.schema.json" for name in CORPUS}


def fail_env(message):
    print(json.dumps({"result": "ENVIRONMENT_FAILURE", "error": message}))
    return 2


def main():
    failures = []

    try:
        import jsonschema
    except ImportError:
        return fail_env("INDEPENDENT_SCHEMA_ENVIRONMENT_UNAVAILABLE: jsonschema is not importable; install it (pinned) before validation. No fallback path exists.")

    docs = {}
    for name, rel in CORPUS.items():
        path = ROOT / rel
        if not path.exists():
            failures.append(f"CORPUS_FILE_MISSING: {rel}")
            continue
        try:
            docs[name] = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            failures.append(f"CORPUS_PARSE_FAILURE: {rel}: {exc}")

    for name, doc in docs.items():
        schema_path = ROOT / SCHEMAS[name]
        if not schema_path.exists():
            failures.append(f"SCHEMA_FILE_MISSING: {SCHEMAS[name]}")
            continue
        try:
            jsonschema.validate(doc, json.loads(schema_path.read_text(encoding="utf-8")))
        except jsonschema.ValidationError as exc:
            failures.append(f"SCHEMA_INVALID: {name}: {exc.message[:200]}")

    rule_ids = {}
    for name, doc in docs.items():
        for rule in doc.get("rules", []):
            rid = rule.get("rule_id", "")
            if rid in rule_ids:
                failures.append(f"DUPLICATE_RULE_ID: {rid} ({rule_ids[rid]} and {name})")
            rule_ids[rid] = name

    for name, doc in docs.items():
        for rule in doc.get("rules", []):
            for ref in rule.get("superseded_by") or []:
                if ref and ref not in rule_ids:
                    failures.append(f"UNRESOLVED_SUPERSESSION: {rule.get('rule_id', '?')} superseded_by {ref}")

    report = {
        "result": "FAIL" if failures else "PASS",
        "corpus_documents_loaded": len(docs),
        "rule_count": len(rule_ids),
        "failures": failures,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
