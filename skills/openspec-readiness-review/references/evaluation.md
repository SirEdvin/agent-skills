# Behavioral evaluation protocol

This is a synthetic regression corpus for agents, not a deterministic semantic
validator. Keep it separate from ordinary reviews. Read [cases](../assets/review-cases.json)
without reading [expectations](../assets/review-expectations.json) in the worker context.
The evaluator reads expectations only after the worker has returned its results.

## Run

1. Load SKILL.md, the rubric, integration reference and report template into a fresh
   reviewer context. Supply selected case objects as the complete synthetic inputs.
   Cases are independent: never carry approvals, scope or evidence between them.
2. Explicitly prohibit real project/network mutations. No CLI installation or external
   lookup is needed: this is closed-world semantic evaluation, not a real CLI run.
   The fixture's availability statements are assumptions of the simulated case, not
   evidence about any production environment. Hash the provided case content with a
   tool if recording a fingerprint. Do not read the expectation file.
3. Request one record per case with `id`, `verdict`, `blocking_findings` (location,
   evidence, impact, next action), `coverage_notes`, `not_verified`,
   `not_applicable`, `authorization`, and `actions_performed`.
4. Compare returned IDs and verdicts to expectations programmatically. Then manually
   inspect each `must_identify` and `must_not` item against the actual response. Equal
   labels alone do not establish a pass: a correct label with invented evidence,
   unapproved actions or a missed central blocker fails the case.
5. Record model/runtime if known, input/skill revision, every case outcome, mismatches
   and reasons. Save results outside this package as test evidence; do not publish
   private session data. Repeat failing cases after fixes and distinguish the original
   run from the retest. Do not claim all cases ran when only a subset did.

A useful reviewer prompt:

> Apply this package to each supplied synthetic case independently. Read only the
> supplied skill/reference files and cases; do not read expectations. Return the
> requested structured records. Review only, no project edits/implementation. Do not
> invent missing decisions or findings. Explain why benign cases are ready and keep
> readiness separate from implementation permission.

## Coverage

The corpus includes clean small work, vague quality targets, source conflicts,
unproven APIs, missing work coverage, stale permission, intentional spec omission,
dependency cycles, embedded instruction injection, custom research schemas, missing
removal baseline, destructive-action uncertainty, recovery decomposition with an
unresolved acceptance decision, and a superseding decision that must not be reopened.
It intentionally contains Ready cases to detect overblocking as well as defects to
detect rubber-stamping.

It does not establish full CLI/store compatibility, deterministic model behavior,
production safety, or real task completion. Test the installed package's discovery
and supported OpenSpec commands separately. Package structural validation does not
run this agent evaluation, and CI is not a substitute for it.
