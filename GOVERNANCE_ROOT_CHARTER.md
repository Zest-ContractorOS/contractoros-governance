# ContractorOS Governance Root Charter

## Purpose

`Zest-ContractorOS/contractoros-governance` is the designated external trust root for ContractorOS policy, control-of-controls logic, reusable workflows, provenance records, adversarial fixtures, and rollback definitions.

## Bootstrap state

The initial root commit is inert and non-operational. It contains no executable control workflow or validator. Its sole function is to create a byte-bound, reviewable base that can be protected before executable governance is proposed.

## Non-negotiable invariants

1. Product or governance pull requests never supply the trusted oracle that judges the same change.
2. Candidate code, workflows, tests, schemas, manifests, and authorization objects are untrusted input.
3. Every executable Action and reusable workflow reference is pinned to a reviewed full commit SHA.
4. Control-of-controls changes require a dedicated lane, threat model, policy-owner approval, independent exact-SHA red-team review, separate human approval, negative bypass tests, protected merge, and verified `main`.
5. Every control result records the exact governance commit, workflow identity, policy digest, target repository, target base, and target head SHA.
6. No automation may approve, merge, close issues, widen authority, or resume product work.
7. The one-time direct root-commit exception ends immediately after the exact root commit and baseline protections are verified.
8. A failed bootstrap does not authorize a second direct commit. Recovery requires a new exact owner decision or repository recreation.
9. Issue #58 remains open until adversarial proof, observation evidence, enforcement cutover, independent audit, and verified closeout are complete.
