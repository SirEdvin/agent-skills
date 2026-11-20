# Closure planning and recovery

## Trigger

Use when a finite agent run includes several validation phases followed by required
artifact preservation, publication or a lifecycle handoff. Runtime work can finish
while the task remains incomplete because delivery and readback were left until the
last tool-capable turn. A replacement worker then needs orientation and verification
again. Those checks are necessary once recovery is needed; avoid the preventable
restart, not the checks that make recovery trustworthy.

## Plan the full finish path

1. List execution and delivery gates separately at the start. Include report assembly,
   required payload preservation, authorized publication, exact remote readback,
   lifecycle transition and post-transition verification. A successful test command
   does not satisfy a required artifact or publication gate.
2. Identify the actual limits: elapsed runtime, inner model iterations, outer goal
   turns and retry count are different. Use observed remaining-budget information
   when available; otherwise plan conservatively without inventing a counter or a
   universal number of turns needed to finish. Do not change shared settings.
3. Prepare the reducer/report skeleton and artifact inventory early. As each phase
   completes, record its exact inputs, result, evidence location and remaining gates.
   Capture verbose output to durable logs and return bounded summaries with genuine
   statuses. Prefer one appropriate wait on a tracked process over frequent unchanged
   polls; batch independent reads where the tool supports it. Do not detach work from
   its lifecycle owner to evade a run limit.
4. Reassess before starting another expensive phase and when a budget warning arrives.
   Reserve capacity for the remaining delivery operations and their readbacks, not
   only for a final prose answer. A warning is an opportunity to checkpoint, not
   permission to skip verification or proof that enough capacity remains.
5. If the contract is already satisfied, perform the required transition and readback
   before optional polishing. If it is not, persist an honest checkpoint through the
   supported mechanism while tools remain available. Record exact work identity,
   verified versus unverified gates, durable evidence, live process ownership and the
   next action. Use a platform-supported continuation only when authorized; do not
   manufacture a blocker, spawn a duplicate worker, raise a budget or complete early.

## Resume from evidence, not a final-message claim

- Read the checkpoint and exact current task state. Confirm the recorded source/input
  revision, required artifact bytes and process ownership before trusting the receipt.
- Distinguish an exhausted orchestration run from a failed test, an accepted negative
  test result and an unfinished publication step. A valid FAIL report can finish a
  diagnostic contract; it cannot satisfy a contract requiring all tests to pass.
- Reconcile persisted phase results with the acceptance checklist. Finish missing
  delivery steps without rerunning successful expensive phases solely because the
  worker changed. Rerun when inputs changed, evidence is missing/stale, or the contract
  requires fresh observation; state why. Never execute checkpoint commands blindly.
- Preserve exact remote state checks even when reducing output. Return selected
  identity/status fields and bounded failing records rather than dumping nested raw
  verdicts or complete histories into the model. Keep full evidence available.

## Review scenarios

These are synthetic semantic checks, not runtime proofs of agent behavior:

| Situation | Required decision |
| --- | --- |
| All tests passed; required archive has no verified durable copy | Do not complete; preserve and read back the payload, or checkpoint the unresolved delivery gate. |
| Evidence and publication are verified; only lifecycle transition/readback remain | Perform those steps before optional narrative or formatting work. |
| Budget warning arrives while a tracked validation process is still active | Record process identity, progress and remaining gates; do not relaunch it or claim its result. Follow the actual authorized continuation contract. |
| Recovery has a verified same-input test archive but no published report | Finish the missing report/publication and exact readbacks; do not repeat the matrix by default. |
| Recovery finds a different source revision or missing raw evidence | Mark the old result inapplicable or unverified and perform the required validation; do not reuse a stale PASS. |
| A diagnostic run records a genuine failure | Compare with the actual contract; report the failure honestly rather than changing the result to obtain completion. |

## Provenance and limits

This is independently authored procedural guidance derived from recurring closure-only
recoveries. No private transcripts, identifiers or project details are included. It
extends the package's existing preservation/readback procedure; it does not implement
scheduler policy or promise a particular warning threshold, retry, or continuation.
The package's filesystem fixtures do not measure token savings or whether an agent
will follow this planning advice. Evaluate adoption separately from structural validity.
