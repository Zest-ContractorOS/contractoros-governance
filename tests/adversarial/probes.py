#!/usr/bin/env python3
"""H1-B2 adversarial probe runner (TEST instantiation).

Runs every probe in the immutable expected oracle against a disposable copy
of the repository: applies the named mutation, executes the targeted
validator, and compares exit code and output token to the oracle. Fails
closed on ANY deviation — including probes that unexpectedly pass — so a
weakened validator cannot slip through (read-only scope for the real tree;
mutations touch disposable copies only).

Exit 0 = all probes match the oracle; exit 1 = any deviation;
exit 2 = environment failure.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORACLE = ROOT / "tests/adversarial/expected-oracle.json"
FIXTURES = ROOT / "tests/adversarial/fixtures.json"


def fresh_copy(tmp):
    dest = Path(tmp) / "repo"
    subprocess.run(["git", "checkout-index", "-a", f"--prefix={dest}/"], cwd=ROOT, check=True)
    subprocess.run(["git", "init", "-q", "."], cwd=dest, check=True)
    subprocess.run(["git", "add", "-A"], cwd=dest, check=True)
    return dest


def apply_mutation(dest, name, fixtures):
    if name in ("none", "none_blocked_import"):
        return
    spec = fixtures["corpus_mutations"][name]
    target = dest / spec["target_file"]
    op = spec["operation"]
    if op == "copy_first_rule_id_onto_second_rule":
        d = json.loads(target.read_text())
        d["rules"][1]["rule_id"] = d["rules"][0]["rule_id"]
        target.write_text(json.dumps(d))
    elif op == "set_first_rule_classification_to_MUTABLE":
        d = json.loads(target.read_text())
        d["rules"][0]["classification"] = "MUTABLE"
        target.write_text(json.dumps(d))
    elif op == "increment_expected_entry_count":
        d = json.loads(target.read_text())
        d["expected_entry_count"] = d["expected_entry_count"] + 1
        target.write_text(json.dumps(d))
    elif op == "create_untracked_then_add":
        target.write_text("adversarial probe file\n")
        subprocess.run(["git", "add", spec["target_file"]], cwd=dest, check=True)
    elif op == "git_rm_cached":
        subprocess.run(["git", "rm", "-q", "--cached", spec["target_file"]], cwd=dest, check=True)
    else:
        raise ValueError(f"unknown mutation operation: {op}")


def run_probe(probe, fixtures, python_bin):
    with tempfile.TemporaryDirectory() as tmp:
        dest = fresh_copy(tmp)
        env = dict(os.environ)
        if probe.get("fixture"):
            prompt_file = Path(tmp) / "prompt.txt"
            prompt_file.write_text(fixtures["prompt_profiles"][probe["fixture"]])
            cmd = [python_bin, str(dest / probe["target"]), str(prompt_file)]
        else:
            apply_mutation(dest, probe.get("mutation", "none"), fixtures)
            if probe.get("mutation") == "none_blocked_import":
                # Deterministically block the jsonschema import in any
                # interpreter: a stub module that raises ImportError wins
                # the path search via PYTHONPATH.
                stub_dir = Path(tmp) / "import-block"
                stub_dir.mkdir()
                (stub_dir / "jsonschema.py").write_text(
                    'raise ImportError("blocked by H1-B2 adversarial probe")\n'
                )
                env["PYTHONPATH"] = str(stub_dir)
            cmd = [python_bin, str(dest / probe["target"])]
        proc = subprocess.run(cmd, cwd=dest, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
        exit_ok = proc.returncode == probe["expected_exit"]
        token_ok = probe["expected_token"] in proc.stdout
        return exit_ok and token_ok, proc.returncode, proc.stdout[-200:]


def main():
    python_bin = os.environ.get("PROBE_PYTHON", sys.executable)
    try:
        oracle = json.loads(ORACLE.read_text())
        fixtures = json.loads(FIXTURES.read_text())
    except Exception as exc:
        print(f"ENVIRONMENT_FAILURE: cannot load oracle/fixtures: {exc}")
        return 2

    deviations = []
    for probe in oracle["probes"]:
        ok, code, tail = run_probe(probe, fixtures, python_bin)
        status = "MATCH" if ok else "DEVIATION"
        print(f"{status}: {probe['probe_id']} (exit={code}, expected={probe['expected_exit']})")
        if not ok:
            deviations.append({"probe": probe["probe_id"], "exit": code, "tail": tail})

    print(json.dumps({
        "result": "FAIL" if deviations else "PASS",
        "probe_count": len(oracle["probes"]),
        "deviation_count": len(deviations),
    }))
    return 1 if deviations else 0


if __name__ == "__main__":
    sys.exit(main())
