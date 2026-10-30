# Readiness review rubric

Apply these checks to the selected change and its authoritative context, not to an
imagined ideal product. Read the whole relevant requirement/scenario block before
claiming coverage or omission. A search match is a navigation aid, not evidence of
semantic equivalence. This is a pre-implementation review: planned tests are not
executed evidence, but their not-yet-executed status is expected here.

## Check states and blocking policy

- **Pass**: applicable check completed with concrete evidence; explain why it passes.
- **Finding**: a supported problem; attach finding IDs and blocking disposition.
- **Not verified**: applicable check lacks usable evidence or was not performed.
  Record what is missing and the next step. This prevents an overall Ready claim.
- **Not applicable**: outside the actual change/schema/risk; give a specific reason.
  Do not use this for a difficult check or inaccessible evidence.

Critical/Major findings normally block. A bounded, genuinely nonblocking limitation
may remain visible with rationale and any required risk-owner acceptance. Do not
self-accept security, legal, destructive-action or material scope uncertainty. A
human risk decision must identify what was accepted and for which revision; it does
not make a false statement true or an unperformed check Pass. Report disagreement
with unsafe decisions, not an unqualified Ready. No aggregate quality score.

## 1. Intent and business context

Check the source request, not just the proposal's summary of itself:

- What problem/outcome is wanted, for whom or for which operational process?
- Are scope, exclusions, priority constraints and success evidence consistent?
- Do proposed behavior changes have a source, or are they silently added preferences?
- Are existing behavior, identifiers, APIs, data and compatibility that must remain
  unchanged explicitly preserved where relevant?
- Are business/domain rules supported by an authoritative decision/source? Separate
  fact, hypothesis, assumption and actual decision. When authoritative decisions
  conflict and precedence is unresolved, cite both and ask who can decide. If a
  derived draft contradicts a clear source request without an authorized superseding
  decision, identify a revision instead of asking the user to repeat their decision.

A technical chore may be justified by maintenance value and invariants without a
fictional end-user story. A research task may deliver an evidence-backed decision
rather than production code. Do not demand stakeholder interviews for an adequately
specified small request. For a product experiment, label its value hypothesis and
planned validation; readiness to run the experiment is not proof of market value.

## 2. Requirements and baseline integrity

- Identify each affected capability using its native path/heading. Read relevant
  baseline requirements and scenarios alongside the change, not delta files alone.
- Check ambiguous terms, undefined actors/data/states, inconsistent rules, missing
  preconditions and contradictions between proposal, specs, design and tasks.
- Verify MODIFIED blocks retain unchanged obligations; do not lose scenarios when
  replacing a whole requirement. Confirm exact removal/rename targets exist and
  inspect downstream references. Review reason/migration for removal and preserved
  behavior for a name-only rename. Flag an apparent rename hiding a behavior change.
- Check scope boundaries, permissions, external integrations and transition states
  affected by this change. Do not insist on unrelated enterprise requirements.
- Honor optional artifacts and active schemas. If a pure refactor intentionally
  skips specs, check its observable invariants and verification route. If the same
  proposal changes output or policy, skipping specs is not justified.

## 3. Acceptance scenarios

Can a reviewer distinguish a correct implementation from an incorrect one?

- Scenarios specify relevant initial state, actor/input/action and observable result.
- Assertions verify the actual outcome, not “works”, “handles correctly”, “test exists”,
  or a restatement of the implementation step.
- Where relevant, cover boundaries, invalid input, permissions, empty/duplicate data,
  retries/idempotency, partial failures, timeout/recovery and compatibility.
- For non-functional behavior, use approved workload, metric, target, measurement
  method and environment. Ask for missing values; do not invent a latency number,
  retention policy, legal obligation or availability promise.
- Match planned verification to the risk: unit tests can check transformations;
  integrations may need a contract test or controlled real-service check. State
  fixtures/environment needs and what evidence will establish acceptance.

Not every task needs Given/When/Then, every feature needs every edge case, or every
small change needs an NFR section. A docs task can be accepted by a runnable example
and link/content checks; a spike by a bounded experiment, evidence and recommendation.

## 4. Feasibility and operations

Read code, configuration, supported APIs/version docs or prior verified evidence for
material assumptions. Record uncertainty when access is unavailable; do not infer a
capability just because a library has a promising name. Inspect the proposed approach
at the level needed to find blockers, not to prewrite the implementation.

Consider only applicable constraints: security/privacy, data integrity, performance,
accessibility, resource limits, observability, deployments, backup/migration/rollback,
permissions/licensing and external availability. Identify migration compatibility and
failure containment before irreversible changes. A rollback may legitimately be
impossible; then the approved recovery/forward-fix/containment strategy must address
the risk rather than inventing reversibility.

An unresolved factual dependency needs research with a question, bounded experiment,
expected evidence and decision point. An unresolved policy needs clarification.
Missing credentials are not a request to obtain secrets or probe production.

## 5. Bidirectional coverage

Build a compact table using native references:

| Outcome / requirement / invariant | Delivering task(s) or schema-equivalent work | Acceptance / verification route | Status / finding |
| --- | --- | --- | --- |

Include changed, removed and renamed behavior plus applicable preserved invariants.
Use exact headings/paths and task IDs where available; no new canonical REQ namespace.
For non-task schemas, use their actual execution/handoff artifact or identify where
the requested outcome is delivered. The lack of tasks.md itself is not a defect.

Check both directions:

- Every in-scope obligation has meaningful delivering work and a way to verify it.
- Every task is necessary to an obligation, accepted enabling work or justified
  research. Extra features hidden in tasks are scope creep.
- Each acceptance scenario has an appropriate verification route. One task may
  cover several requirements, and one requirement may need several tasks; explain
  that relationship rather than requiring a one-to-one map.
- Do not mistake shared keywords, IDs, or “run all tests” for coverage. Identify the
  specific test/assertion/observable evidence that will cover the behavior.

## 6. Decomposition and dependency safety

Look for bounded, independently verifiable work, not arbitrary time estimates or
forced fragmentation. Each executable task needs outcome, sufficient relevant
context, prerequisites and a completion check. Flag tasks that conceal an unresolved
design decision or combine unrelated deliverables that cannot be assessed together.

Check dependency cycles, missing prerequisites, migrations before consumers, contracts
before integrations, test-data availability and shared-file/interface conflicts.
Parallel work is safe only when its dependency and edit boundaries support it; a
list with no dependencies is not proof of independence. Deliver local tests and docs
with the relevant work; later integration checks may deliberately span groups.

When reviewing a recovery plan after implementation exposed an acceptance conflict,
carry the unresolved decision into every affected successor's readiness assessment.
Renaming a task, restoring its original text, creating a research child or splitting
implementation from verification does not resolve a behavior or authorization choice.
Record the conflicting assertions, the decision needed, its owner and the evidence
that would resolve it. Do not call the affected implementation Ready merely because
its new dependencies are complete; unrelated work may still be independently ready.

Check for a later, explicit scoped decision before carrying the blocker forward.
An earlier approval for a different defect does not cover the new conflict, but a
verified superseding decision must not trigger the same clarification again. Map
superseded assertions to their authorized current replacements, retain applicable
safety and historical-compatibility obligations, and recheck the affected coverage.
Readiness to implement that repair is not evidence its replacement tests passed.
This review reports the recovery decision; it does not requeue or alter task state.

## 7. Decisions, freshness and handoff

Resolve questions that change what gets built before declaring it ready. A documented
nonblocking implementation choice can remain open with its boundary and responsible
party; do not elevate every local variable name into a user decision.

Separate:

1. What was reviewed: exact artifacts, baseline/config, source decisions and revisions.
2. What the review establishes: specification verification and limits of business evidence.
3. What was authorized: who permitted which action at which revision, if known.

If relevant evidence changes during review, withhold Ready for the new state. On
re-review, compare changed content, carry finding IDs forward, verify resolution and
recheck affected dependencies/coverage. A clean re-review can be Ready while older
implementation approval is stale; implementation still needs appropriate authorization.
