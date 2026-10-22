# Sources and provenance

This package is independently authored review guidance, not copied BMAD, Spec Kit,
OpenSpec or third-party BA skill text. It introduces a local review policy, not an
official OpenSpec workflow or a guarantee of IIBA certification. No private project
paths, stakeholder records or conversation transcripts are included.

Reviewed on **2026-10-22**. OpenSpec release **v1.14.3** resolves to commit
`c794978f4f8845ce59693373c9dd882ee776588c` (tag checked through GitHub). Commands were
smoke-tested using the published `@fission-ai/openspec@1.14.3` package in a disposable
project. These observations do not guarantee every older CLI or custom schema works.

## Upstream contracts

- [OpenSpec default schema](https://github.com/Fission-AI/OpenSpec/blob/c794978f4f8845ce59693373c9dd882ee776588c/schemas/spec-driven/schema.yaml): artifact roles, behavior specs, deltas, intentional spec omission, conditional design, task verification and dependency ordering.
- [OpenSpec verification skill](https://github.com/Fission-AI/OpenSpec/blob/c794978f4f8845ce59693373c9dd882ee776588c/skills/openspec-verify-change/SKILL.md): schema-aware discovery, resolved roots, task tracking and distinction between not applicable and not verified. Its purpose is post-implementation; this package does not copy its completion checks into pre-implementation review.
- [OpenSpec supported tools](https://github.com/Fission-AI/OpenSpec/blob/c794978f4f8845ce59693373c9dd882ee776588c/docs/supported-tools.md): Hermes skills-only delivery and workflow-dependent generated skill names. Its external_dirs setup advice must be checked against the installed Hermes version rather than repeated as universal.
- [Hermes skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills): on-demand loading, package installation, project-local trust/discovery and slash invocation. This is a living document.
- [Agent Skills specification](https://agentskills.io/specification): independently installable directories, progressive disclosure and portable string-valued metadata.

Upstream repositories retain their own licenses (OpenSpec is MIT). Links identify
technical evidence, not a claim that all linked documentation is covered by this
repository's MIT license. No third-party BA package is vendored or required.

## Policy defined here, not promised upstream

The four readiness verdicts, blocking policy, finding format, independent risk-scaled
review, requirement/work/verification coverage table, exact-revision review, and
separation of readiness from business validation and implementation authorization
are this package's recommendations. OpenSpec's structural validator is not a semantic
oracle. No script in this package enforces project transitions or grants approval.

## Verification boundaries

Structural package validation and CLI smoke tests can establish packaging and command
behavior. The synthetic behavioral cases exercise review decisions and false-positive
resistance. They are not a benchmark of real-project reliability, an end-to-end
production rollout, or proof of enforced read-only tool access. Record actual model,
case outcomes and limitations in PR evidence; do not turn a single run into a success-rate
claim. Repeat the cases when changing verdict rules or schema handling.
