# Readiness review: <change>

Use as an output structure, not a requirement to create a file. Replace placeholders;
compress rows for a small change, but retain scope, verdict, evidence limitations and
authorization. Never copy a placeholder into a claim of completed verification.

## Summary

- Verdict: Ready | Needs clarification | Needs research | Needs revision
- Scope: project/store, exact change, intended outcome and exclusions
- Reviewed revision: commit(s) plus dirty/untracked content fingerprints or immutable
  document revisions; include relevant baseline/config/source decision identities
- Review depth: lightweight | expanded; risk rationale, actual reviewers/perspectives
- Blocking findings: IDs (or none)
- Next action: precise decision/research/revision request, or handoff for user decision

## Evidence and checks

| Input | Location / exact revision | Read / unavailable / intentionally omitted | Relevance |
| --- | --- | --- | --- |

Structural validation: command, tool version, actual result/errors or Not run + reason.
Treat structural validation and semantic review separately.

| Dimension | Pass / Finding / Not verified / Not applicable | Evidence / finding IDs / reason |
| --- | --- | --- |
| Intent and scope | | |
| Requirement and baseline integrity | | |
| Acceptance quality | | |
| Feasibility and applicable operational constraints | | |
| Bidirectional coverage | | |
| Decomposition and dependencies | | |
| Decisions, freshness and provenance | | |

## Coverage

| Native requirement / outcome / invariant | Delivering work | Scenario and verification route | Disposition |
| --- | --- | --- | --- |

List justified enabling work and any orphan tasks. Reconcile declared counts with
actual rows programmatically if reporting totals. Do not call omitted rows covered.

## Findings

### RR-001 — <specific problem>

- Severity: Critical | Major | Minor | Suggestion
- Blocking: yes/no, with impact rationale
- Location: exact artifact/heading/task and line range when available
- Evidence: source quote or observed fact; distinguish absence from contradiction
- Consequence: why this matters to implementation or acceptance
- Resolution: concrete edit, decision or research result required
- Owner / question: known responsible party, or owner unassigned; focused question
- Re-review status: open | resolved | superseded; resolution evidence if applicable

Zero findings is a legitimate result. Do not invent suggestions to fill this section.

## Decisions, limits and authorization

- Specification verification: what was established and what remains unverified
- Business validation: evidence of need/fit, or explicitly unvalidated hypothesis
- Nonblocking limitations: rationale and risk acceptance source where required
- Implementation authorization: current | absent | stale | unknown; evidence, actor,
  permitted action and revision if actually available; this review grants none
- Freshness: inputs unchanged at completion, or exact changes that invalidate review
- Writes/actions performed: report only, or explicitly authorized report path
- Re-review triggers: material changes to scope, rules, scenarios, design, dependencies,
  relevant baseline/evidence or required approval; name affected checks
