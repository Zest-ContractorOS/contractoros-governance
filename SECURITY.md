# Security and Reporting Boundary

This repository must not contain production secrets, private keys, long-lived credentials, deploy keys, self-hosted-runner credentials, customer data, or product runtime data.

Security-sensitive governance changes include workflows, validators, policy files, schemas, CODEOWNERS, ruleset specifications, provenance formats, authorization formats, and rollback logic. They require the control-of-controls lifecycle defined in `GOVERNANCE_ROOT_CHARTER.md`.

Report suspected control bypasses, provenance failures, policy self-modification, workflow replacement, check-name collision, stale pins, authorization forgery, or rollback ambiguity through the owner-controlled ContractorOS issue process. Do not disclose credentials or private evidence in a public issue.

The inert bootstrap commit provides no security certification and no claim that the trusted policy root is operational.
