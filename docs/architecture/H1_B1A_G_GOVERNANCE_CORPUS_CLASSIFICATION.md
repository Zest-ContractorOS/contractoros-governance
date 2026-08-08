# H1-B1A-G Governance Corpus Classification

```text
NORMATIVE_STATUS=NON_NORMATIVE_GUIDANCE
CANONICAL_SOURCES=policy/corpus/*.json
H1_B1A_G_MODEL=CONTRACT_COMPLETE_EXECUTION_EMPTY
LOCAL_PACKET_LINTER_AUTHORITY=NONE
TRUSTED_RUNTIME_VALIDATOR=NO
FUTURE_TRUSTED_VALIDATOR_GATE=H1_B1C
```

This document is non-normative guidance. It explains, diagrams, and navigates the H1-B1A-G corpus.
It must not be treated as a second maintainable authority.

Canonical normative sources are the five policy JSON files under `policy/corpus/`.
Structural constraints are the five Draft 2020-12 schemas under `schemas/governance/`.
The local packet linter validates candidate packages only and creates no H1 operational authority.

## Phase model

H1-B1A-G is contract-complete and execution-empty.

It completely defines governance language, authority hierarchy, classifications, artifact inventory,
rule identity, ownership, schemas, supersession, dependency and impact relationships, future component
classes, future gate assignments, authority and publication contracts, failure semantics, and the
H1-B4/H4 handoff boundary.

It does not implement scanners, compilers, trusted runtime validators, workflows, rulesets,
branch protection, observation mode, enforcement, product integration, product sanitation,
AI output contracts, or product runtime capabilities.

See:

- `COS-H1-AUTH-011` in `policy/corpus/governance-hierarchy.json`
- `/gate_contracts` in `policy/corpus/governance-hierarchy.json`

## Authority hierarchy

Exact ordered layers (rank equals array position):

1. `APPLICABLE_LAW_AND_BINDING_OBLIGATIONS` — rule `COS-H1-AUTH-001`
2. `DURABLE_EXPLICIT_OWNER_AUTHORITY`
3. `PROGRAM_CONSTITUTION_AND_OWNER_DECISION_REGISTER`
4. `TRUSTED_H1_GOVERNANCE_POLICY_ROOT`
5. `PRODUCT_REPOSITORY_CONTROLS_AND_WORKFLOWS`
6. `DEVELOPER_RED_TEAM_AND_AUTOMATION_OUTPUTS`

Structured data and rule text must agree (`COS-H1-AUTH-015`).

Mutable-state resolution (`/mutable_state_resolution`):

- `CURRENT_LIFECYCLE=LIVE_GITHUB_REQUIRED`
- `CURRENT_MAIN_SHA=LIVE_GITHUB_REQUIRED`
- `ACTIVE_AUTHORITY=AUTHORITY_INDEX_AND_LIVE_ISSUE_REQUIRED`
- `CANONICAL_STATE=LAST_VERIFIED_OBSERVATION`

## Classifications

Closed set of six primary classifications in `policy/corpus/classifications.json`:

| Classification | May control current action |
|---|---|
| STABLE_POLICY | yes when ACTIVE |
| MUTABLE_LIVE_STATE | no |
| DERIVED_POINT_IN_TIME_STATE | no |
| HISTORICAL_AUDIT_EVIDENCE | no |
| GENERATED_PRESENTATION | no |
| NON_NORMATIVE_GUIDANCE | no |

Historical-example contract: rule `COS-H1-CLASS-004` and `/historical_example_template`.

## Hybrid governing-artifact manifest

Model: `HYBRID` (`COS-H1-TREE-008`).

- Existing artifacts: exact repository paths
- Proposed H1-B1A-G files: exact paths with `PROPOSED_FOR_H1_B1A_G`
- Future components: closed class records with `NOT_YET_EXISTS` and `exact_path=UNRESOLVED_BY_CURRENT_GATE`

No unapproved future filenames are invented. `H1_TO_H4_ENFORCEMENT_HANDOFF` is a required future class.

## Ownership and posting contract

Identities (`policy/corpus/ownership.json`):

- `OWNER=Zest-LeadGen`
- `POLICY_OWNER=Zest-LeadGen`
- `MANIFEST_OWNER=Zest-LeadGen`
- `IMPLEMENTATION_MACHINE_ACCOUNT=danidon-wq`
- machine approval authority: `NONE`

Posting-ready contract (`COS-H1-OWNER-009`): child issue `IMPLEMENTATION_AUTHORITY=NONE`.

Two-checkpoint publication and event-bounded single-use authority: `COS-H1-OWNER-011`.

```text
authorization_reuse=NO
stage_b.requires_separate_owner_activation=true
automatic_cleanup=PROHIBITED
mutation_window_type=EVENT_BOUNDED_TWO_CHECKPOINT
```

## H1-B4 / H4 boundary

| Concern | Rule |
|---|---|
| One canonical H1 policy check at H1-B4 | `COS-H1-AUTH-012` |
| No H1-B4 program-wide CI / general ruleset redesign | `COS-H1-AUTH-012` |
| H4 may supersede H1-B4 mechanics only via handoff | `COS-H1-AUTH-013` |
| H4 must not weaken H1 effective control | `COS-H1-AUTH-013` |
| MAKE_BEFORE_BREAK required | `COS-H1-AUTH-014` |
| H1_TO_H4_ENFORCEMENT_HANDOFF future class only | `/h1_to_h4_enforcement_handoff_contract` |

```text
h1_b4_program_wide_ci_hardening=PROHIBITED
h4_may_weaken_h1_effective_control=NO
make_before_break=REQUIRED
break_before_make=PROHIBITED
```

## Gate contracts

See `/gate_contracts` in `policy/corpus/governance-hierarchy.json` for machine-readable assignments of
H1_B1A_G through H1_B5 and H4.

## Mapping the eleven proposed files

| Path | Role |
|---|---|
| `policy/corpus/governance-hierarchy.json` | Precedence, gate contracts, H1-B4/H4 boundary |
| `policy/corpus/classifications.json` | Closed classifications and historical exemption |
| `policy/corpus/governing-files.json` | Hybrid manifest + dependency/impact inventory |
| `policy/corpus/supersession.json` | Lineage and versioning |
| `policy/corpus/ownership.json` | Ownership, lifecycle, posting, two-checkpoint model |
| `schemas/governance/*.schema.json` | Draft 2020-12 structural constraints |
| `docs/architecture/H1_B1A_G_GOVERNANCE_CORPUS_CLASSIFICATION.md` | This non-normative guidance |

## Gate-specific threat model

Each threat references normative rule IDs. This section is guidance only.

### TM-001 MALFORMED_OR_JSON_STRING_ENCODED_MARKDOWN

- affected_asset: architecture markdown
- failure_or_attack: wrap markdown as a JSON string or use literal `\n` line structure
- normative_prevention_rule_ids: `COS-H1-CLASS-008`, `COS-H1-TREE-001`
- detection: first byte `#`; physical LF lines; not JSON-parseable as a string
- stop_condition: packet rejected
- assigned_test: `json_string_encoded_markdown`, `literal_backslash_n_markdown_structure`
- residual_risk: low if linter + review enforced
- future_gate: H1_B1C for repository-tree enforcement

### TM-002 HIERARCHY_STRUCTURE_AND_RULE_TEXT_DIVERGENCE

- affected_asset: `precedence_layers` vs `COS-H1-AUTH-001`
- failure_or_attack: reorder or substitute layers while leaving prose unchanged
- normative_prevention_rule_ids: `COS-H1-AUTH-001`, `COS-H1-AUTH-015`
- detection: prefixItems/const schema + linter rank/order checks
- stop_condition: reject missing/added/substituted/duplicate/wrong-order layers
- assigned_test: `wrong_hierarchy_order`, `substituted_hierarchy_layer`, `hierarchy_rule_structured_data_divergence`
- residual_risk: medium without H1_B1C
- future_gate: H1_B1C

### TM-003 SCHEMA_WEAKENING_OR_UNKNOWN_FIELD_ACCEPTANCE

- affected_asset: Draft 2020-12 schemas
- failure_or_attack: allow unknown properties or remote refs
- normative_prevention_rule_ids: `COS-H1-GATE-003`, `COS-H1-TREE-001`
- detection: `additionalProperties:false`, independent Draft202012Validator, no remote loading
- stop_condition: independent schema validation fails
- assigned_test: `unknown_schema_version`, `unknown_rule_property`
- residual_risk: medium
- future_gate: H1_B1C

### TM-004 UNKNOWN_OR_UNCLASSIFIED_GOVERNING_ARTIFACT

- affected_asset: governing-file inventory
- failure_or_attack: introduce controlling file outside hybrid manifest
- normative_prevention_rule_ids: `COS-H1-TREE-001`, `COS-H1-TREE-008`, `COS-H1-CLASS-002`
- detection: sole-manifest checks; future classes closed
- stop_condition: reject unclassified controlling artifact claims
- assigned_test: `extra_proposed_tree_file`, `missing_required_future_component_class`
- residual_risk: high until full-tree scanner (H1_B1C)
- future_gate: H1_B1C

### TM-005 INCOMPLETE_DEPENDENCY_OR_IMPACT_GRAPH

- affected_asset: `/dependency_impact_entries`
- failure_or_attack: orphan rules/schemas or unknown dependency targets
- normative_prevention_rule_ids: `COS-H1-TREE-008`
- detection: one dep record per artifact/rule/schema/future class; resolvable edges only from known IDs
- stop_condition: unknown/duplicate/orphan dependency graph
- assigned_test: `unknown_dependency_target`, `unknown_valid_format_rule_dependency`
- residual_risk: medium
- future_gate: H1_B2

### TM-006 UNKNOWN_CIRCULAR_OR_NONRECIPROCAL_SUPERSESSION

- affected_asset: supersession lineage
- failure_or_attack: self, circular, or nonreciprocal supersession of any length
- normative_prevention_rule_ids: `COS-H1-SUPER-001` through `COS-H1-SUPER-007`
- detection: reciprocal supersedes/superseded_by validation and full graph cycle detection
- stop_condition: listed rejection codes in supersession.json
- assigned_test: `self_supersession`, `three_node_supersession_cycle`, `four_node_supersession_cycle`
- residual_risk: low
- future_gate: H1_B2

### TM-007 MUTABLE_STATE_EMBEDDED_IN_STABLE_POLICY

- affected_asset: stable policy JSON
- failure_or_attack: embed live comment IDs as self-sufficient authority
- normative_prevention_rule_ids: `COS-H1-AUTH-003`, `COS-H1-CLASS-003`
- detection: provenance uses durable decision IDs + LIVE_GITHUB_REQUIRED
- stop_condition: reject active comment-ID authority inside stable policy
- assigned_test: authority provenance checks in linter
- residual_risk: medium
- future_gate: H1_B1C

### TM-008 DRAFT_GENERATED_OR_NAVIGATION_ARTIFACT_TREATED_AS_AUTHORITY

- affected_asset: publication drafts and unposted planning artifacts
- failure_or_attack: treat drafts as live authority, or weaken unposted classification via aliases, synonyms, `LOCAL_PUBLICATION_TEMPLATE`, or `AUTHORITY=NONE` alone
- controlling_requirement: `H1B1-POST-001`
- normative_prevention_rule_ids: `COS-H1-CLASS-007`, `COS-H1-OWNER-009`
- structured_contract: `unposted_draft_classification_contract` requiring exact `DRAFT_STATUS=NOT_POSTED`, `DRAFT_POSTING_AUTHORITY=NOT_YET_GRANTED`, and `IMPLEMENTATION_AUTHORITY=NONE` with `aliases_allowed=false` and `equivalent_values_allowed=false`
- detection: exact field parsing of the three required classifications; reject missing, duplicate, conflicting, alias, and `LOCAL_PUBLICATION_TEMPLATE` values; `AUTHORITY=NONE` alone is insufficient
- stop_condition: `INVALID_UNPOSTED_DRAFT_STATUS`, `MISSING_DRAFT_POSTING_AUTHORITY`, `MISSING_EXACT_UNPOSTED_DRAFT_FIELDS`, `DUPLICATE_OR_CONFLICTING_DRAFT_CLASSIFICATION`, `UNPOSTED_DRAFT_EQUIVALENCE_ESCAPE`, `DRAFT_FALSELY_CLAIMS_AUTHORITY`
- assigned_test: `alternate_draft_status_local_publication_template`, `missing_draft_posting_authority`, `authority_none_used_as_alias_only`, `conflicting_duplicate_draft_status`, `equivalent_language_reintroduced_in_normative_rule`, `coordinated_rule_schema_coverage_and_draft_mutation_to_alternate_values`, `draft_falsely_claims_authority`
- residual_risk: medium without independent Red-Team semantic review
- future_gate: Stage A/B process controls; trusted runtime validator remains H1_B1C

### TM-009 MACHINE_ACCOUNT_ROLE_ESCALATION

- affected_asset: role separation
- failure_or_attack: danidon-wq provides owner/approval/merge authority
- normative_prevention_rule_ids: `COS-H1-OWNER-004`, `COS-H1-OWNER-010`
- detection: identity constants and prohibited acts list
- stop_condition: reject machine-account approval claims
- assigned_test: ownership completeness checks
- residual_risk: medium without H2/H4
- future_gate: H2 / H4

### TM-010 PREPUBLICATION_AND_POSTPUBLICATION_BYTE_DRIFT

- affected_asset: implementation package digest and review bundle
- failure_or_attack: mutate files after seal
- normative_prevention_rule_ids: `COS-H1-AUTH-005`
- detection: EXTERNAL_SHA256SUMS_AND_FINAL_REPORT binding; resealed self-tests
- stop_condition: digest mismatch
- assigned_test: `implementation_package_digest_mismatch`, `review_bundle_seal_mismatch`
- residual_risk: low if seals verified
- future_gate: Stage A/B readback

### TM-011 UNRESOLVED_CHILD_ISSUE_VALUE_IN_FINAL_PR_BODY

- affected_asset: PR template
- failure_or_attack: leave sentinel placeholders in final PR
- normative_prevention_rule_ids: `COS-H1-OWNER-007`, `COS-H1-OWNER-011`
- detection: Stage B substitution and seal after live child-issue readback
- stop_condition: reject unresolved sentinels in final PR body
- assigned_test: `unresolved_child_issue_sentinel_in_final_pr`
- residual_risk: low with Stage B gates
- future_gate: Stage B

### TM-012 PARTIAL_GITHUB_MUTATION_OR_UNAUTHORIZED_CLEANUP

- affected_asset: publication mutation windows
- failure_or_attack: auto-delete/close after partial failure
- normative_prevention_rule_ids: `COS-H1-OWNER-011` and `/partial_failure_behavior`
- detection: STOP_AND_REPORT_EXACT_CREATED_OBJECTS
- stop_condition: no automatic cleanup
- assigned_test: process review (publication drafts)
- residual_risk: medium
- future_gate: Stage A/B runbooks

### TM-013 H1_B4_SCOPE_ABSORBS_H4

- affected_asset: H1-B4 boundary
- failure_or_attack: program-wide CI/ruleset redesign under H1-B4
- normative_prevention_rule_ids: `COS-H1-AUTH-012`
- detection: gate contract and rule structured flags
- stop_condition: reject H1-B4 absorbing H4
- assigned_test: `h1_b4_absorbs_program_wide_h4_scope`
- residual_risk: medium
- future_gate: H1_B4 / H4

### TM-014 H4_WEAKENS_OR_REPLACES_H1_WITH_AN_ENFORCEMENT_GAP

- affected_asset: H1 effective control
- failure_or_attack: H4 replaces H1-B4 mechanics without handoff / with gap
- normative_prevention_rule_ids: `COS-H1-AUTH-013`, `COS-H1-AUTH-014`
- detection: required H1_TO_H4_ENFORCEMENT_HANDOFF; MAKE_BEFORE_BREAK
- stop_condition: reject break-before-make and weakening
- assigned_test: `h4_allowed_to_weaken_h1_control`, `break_before_make_allowed`
- residual_risk: medium until H4 handoff tooling
- future_gate: H4

## Explicit non-claims

```text
FULL_TREE_AUDIT_PERFORMED=NO
EXHAUSTIVE_FULL_TREE_ENUMERATION=NOT_PERFORMED
ABSENCE_OF_UNDISCOVERED_FILES=NOT_PROVEN
IMPLEMENTATION_AUTHORITY=NONE_UNTIL_EXTERNAL_OWNER_RECORD
H1_B1A_G_IMPLEMENTATION_STARTED=NO
H1_B1A_P_STARTED=NO
H1_B1C_STARTED=NO
H1_B2_STARTED=NO
H1_B3_STARTED=NO
H1_B4_STARTED=NO
H4_STARTED=NO
PRODUCT_WORK_STARTED=NO
AUTOMATIC_CONTINUATION=NO
combined_governance_and_product_blast_radius=PROHIBITED
```

This architecture document does not authorize implementation, issue creation, branch creation,
merge, Stage A, Stage B, or automatic continuation.
