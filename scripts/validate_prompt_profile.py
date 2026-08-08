#!/usr/bin/env python3
"""H1-B2 prompt-profile validator (VALIDATOR instantiation, DEFECT_4 control).

Validates that a prompt text begins with the exact ordered ten-field profile
defined by the ContractorOS prompt convention. Fails closed on a missing,
reordered, duplicated, malformed, misplaced, empty-valued, or stale-version
profile (read-only scope; regression surface for
DEFECT_4=CODEX_EXECUTION_PROMPT_OMITTED_MANDATORY_ORDERED_TEN_FIELD_PROFILE).

Usage: validate_prompt_profile.py FILE   (or: --stdin)
Exit 0 = PASS, exit 1 = profile invalid, exit 2 = environment failure.
"""
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "Recommended Codex model:",
    "Recommended reasoning effort:",
    "Why this model/effort:",
    "Do not change model/effort unless:",
    "Recommended speed mode:",
    "Agent strategy:",
    "Plan/quota mode:",
    "Context-window strategy:",
    "Checkpoint cadence:",
    "Maximum scope:",
]


def validate(text):
    failures = []
    lines = [line.rstrip() for line in text.splitlines()]

    # Locate the first profile field anywhere in the text.
    first_idx = None
    for i, line in enumerate(lines):
        if any(line.startswith(f) for f in REQUIRED_FIELDS):
            first_idx = i
            break
    if first_idx is None:
        return ["PROFILE_MISSING: no ten-field profile found"]

    # Misplaced: substantive content precedes the profile.
    for line in lines[:first_idx]:
        if line.strip() and not line.strip().startswith("#"):
            failures.append("PROFILE_MISPLACED: substantive text precedes the profile")
            break

    # Collect the profile block: consecutive field lines from first_idx.
    seen = []
    for line in lines[first_idx:first_idx + len(REQUIRED_FIELDS) * 2]:
        matched = None
        for f in REQUIRED_FIELDS:
            if line.startswith(f):
                matched = f
                break
        if matched is None:
            if line.strip() and ":" in line and seen and len(seen) < len(REQUIRED_FIELDS):
                failures.append(f"FIELD_MALFORMED_OR_UNKNOWN: {line.strip()[:60]!r}")
            if len(seen) >= len(REQUIRED_FIELDS):
                break
            continue
        if matched in seen:
            failures.append(f"FIELD_DUPLICATED: {matched}")
            continue
        expected = REQUIRED_FIELDS[len(seen)]
        if matched != expected:
            failures.append(f"FIELD_OUT_OF_ORDER: got {matched!r} expected {expected!r}")
            seen.append(matched)
            continue
        value = line[len(matched):].strip()
        if not value:
            failures.append(f"FIELD_EMPTY_VALUE: {matched}")
        seen.append(matched)

    missing = [f for f in REQUIRED_FIELDS if f not in seen]
    if missing:
        failures.append(f"FIELDS_MISSING_OR_STALE_VERSION: {missing}")

    return failures


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--stdin":
        text = sys.stdin.read()
    elif len(sys.argv) == 2:
        path = Path(sys.argv[1])
        if not path.exists():
            print(json.dumps({"result": "ENVIRONMENT_FAILURE", "error": f"file not found: {path}"}))
            return 2
        text = path.read_text(encoding="utf-8", errors="replace")
    else:
        print(json.dumps({"result": "ENVIRONMENT_FAILURE", "error": "usage: validate_prompt_profile.py FILE|--stdin"}))
        return 2

    failures = validate(text)
    print(json.dumps({"result": "FAIL" if failures else "PASS", "failures": failures}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
