---
name: lifecycle-safe-verification
description: Use when completion, handoff or cleanup may remove a workspace. Preserve evidence before the transition and verify exact state afterward from a surviving directory.
license: MIT
compatibility: The disposable regression fixture requires Python 3.12 or newer and Git.
metadata:
  version: "1.0.0"
---

# Lifecycle-safe verification

## Trigger and boundaries

Use before a task completion, review handoff, workspace teardown or other authorized
transition that may delete or relocate the current working directory. This skill does
not authorize cleanup, lifecycle transitions, status changes, process termination or
retries. Follow the platform's actual lifecycle contract; not every transition removes
a worktree, and a successful transition need not stop a worker process.

## Before the transition

1. Establish exact identity: task/record ID, board or namespace, profile/account,
   repository and expected state. Do not rely on a tool's implicit current task after
   changing directories. Use explicit selectors supported by the platform.
2. Inspect cleanup semantics and identify task-owned versus persistent locations.
   Choose an existing stable directory outside every workspace that the transition
   can remove. A parent path is safe only if it too survives cleanup; a symlink into
   the disposable workspace is not a durable location. Resolve real paths.
3. Finish acceptance checks first. Preserve required reports, checksums, commits and
   attachments through the platform's supported durable-artifact mechanism, or another
   user-approved persistent location. Read back exact artifact identity and content.
   A path string in a comment does not preserve the file it names.
4. Record a compact pre-transition receipt outside the disposable directory: exact
   identity, expected transition, evidence locations, verification commands, and any
   unresolved limitations. Never mark unfinished acceptance complete merely to preserve
   evidence; use the appropriate authorized checkpoint/handoff state instead.
5. Plan post-transition verification so it does not require the old checkout, its
   virtualenv, relative files, environment-dependent board discovery or helper scripts.
   Resolve required executables and durable paths before the transition.

## Transition and exact readback

1. Perform the already-authorized transition once. Capture its receipt without treating
   success as proof of the desired durable state.
2. Launch the readback with the execution tool's **explicit stable working-directory
   parameter**. A `cd` inside the command may never run if the tool fails while entering
   its remembered deleted cwd. If the tool lacks a working-directory override, use an
   independent session rooted in a surviving location. Do not repeat the lifecycle
   mutation to repair a failed readback.
3. Read the exact task/record and transition event using a supported read-only interface.
   Verify expected status, relevant run/event identity and durable artifact contents.
   If removal itself was requested, separately verify filesystem absence and Git worktree
   deregistration. Do not assume directory absence means a branch or attachment was removed.
4. If the platform transformed the requested state (for example, routed it for review),
   report the actual state. If a worker remains active, report that separately; do not
   stop it without authorization.
5. On error, inspect stderr and which stage failed. A wrapper returning 126 with
   `cd: ... No such file or directory` is not evidence that the target executable needs
   `chmod`. Retry only the read-only verification from a stable directory. If the record
   cannot be read, report transition acknowledged but verification incomplete.

## Disposable regression fixture

[The fixture](scripts/test_lifecycle.py) creates its own temporary Git repository and
linked worktree, preserves a synthetic receipt in a sibling durable directory, removes
only that fixture worktree, then proves launch from the removed cwd fails while launch
from the durable directory succeeds. It also checks Git's worktree list and receipt
content. It never touches a real task, remote, user workspace or platform API.

Run from the installed package directory:

```sh
python -m unittest discover -s scripts -p 'test_*.py' -v
```

This tests filesystem/subprocess/Git behavior, not a universal platform cleanup promise.
Real completion semantics and remote artifact readback still require platform-specific
verification. Do not run removal commands against a user's workspace as a demonstration.

## Sources and provenance

Independently authored from recurring removed-cwd verification failures; no private
logs, paths or task identifiers are included. Python's
[subprocess documentation](https://docs.python.org/3/library/subprocess.html) documents
`cwd`, return codes and child startup failures. The
[Git worktree manual](https://git-scm.com/docs/git-worktree) documents linked-worktree
creation, removal and listing. These primitives support the fixture, not an inference
about any particular task scheduler's implementation.
