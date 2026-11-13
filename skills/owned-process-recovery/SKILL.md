---
name: owned-process-recovery
description: Use when a build or tool process appears stuck. Verify ownership and process identity before any authorized stop or retry.
license: MIT
compatibility: POSIX process concepts; Linux-specific inspection notes are labelled. Synthetic tests require Python 3.12 or newer and send no signals.
metadata:
  version: "1.0.0"
---

# Owned process recovery

## Trigger and authority

Use when an agent considers stopping or relaunching a build, test, server fixture,
or tool subprocess on a shared machine. Diagnose first: this skill grants no
permission to terminate processes, restart tasks, change budgets, or delete caches.
A read-only audit must remain read-only even when it finds an unsafe command.

## Establish what actually timed out

1. Distinguish a tool's **wait window** from the child process's deadline and the
   enclosing worker's runtime budget. A wait response with `process_running=true`
   is not a failed build. Poll the existing job rather than launching a duplicate.
2. Keep the original job/session handle, launch receipt, command, working directory,
   log path and exit status. Prefer the platform's supported job-specific inspection
   and cancellation interface; inspect its actual semantics before using it.
3. Compare log growth, progress markers, descendants and recent errors. Quiet output,
   cache contention or long dependency resolution alone does not establish a stall.
   Read bounded failure excerpts from a durable log, not an entire build transcript.

## Prove ownership before an authorized stop

- Treat a process-name or command-line match as a **discovery hint**, never a kill
  target. Broad `pkill -f` and `killall` can select another task's build. Matching
  the command line can also match an ancestor shell containing the pattern itself;
  exclusion of the matching utility's own PID does not protect that shell.
- Narrowing a regex, adding an ancestor-ignore flag or selecting the same OS user
  does not establish task ownership. Concurrent agents often share a user, build
  executable and cache. Do not try progressively broader kill patterns after failure.
- Correlate a candidate with the original launch receipt, job handle, repository,
  real working directory and task-specific descendants. On Linux, inspect PID,
  parent PID, process group/session, boot identity and process start time. Parentage
  and cwd are corroborating clues, not standalone authorization; descendants may
  reparent and processes may change directories.
- Revalidate identity immediately before acting: a PID can be reused. Prefer a
  platform-owned process handle or supported stable kernel handle where available.
  A separate inspect-then-signal sequence still has a race; do not describe a PID
  plus start-time comparison as an atomic guarantee.
- Never target the agent, tool supervisor, ancestor shell, shared gateway, another
  worker, or a shared daemon. Signal a process group only if its creation and every
  member's ownership are established and group termination is authorized. Do not
  infer an exclusive process group from a common executable name.

## Stop, verify, then retry

1. If permission or identity is uncertain, preserve the log and request the specific
   recovery decision through the allowed checkpoint/escalation mechanism. Do not
   turn a timeout into permission for machine-wide cleanup.
2. If stopping is authorized, use the smallest verified job scope and graceful
   termination first. Do not silently escalate to a stronger signal. Keep stop and
   subsequent mutation/restart in separate calls so a failed stop cannot masquerade
   as successful recovery.
3. Read back that exact job and its known descendants. A stop acknowledgement is not
   proof all descendants exited; a failed shell command is not proof which process
   received a signal. Do not infer collateral damage without evidence.
4. Inspect any partial output or edits before retrying. State the changed hypothesis,
   source revision or environment correction. Reuse logs with distinct attempt names
   and preserve the real command exit status, including nonzero statuses.

## Signal-free verification fixture

The [synthetic tests](scripts/test_recovery_decisions.py) exercise a pure advisory
[identity gate](scripts/recovery_decisions.py). They reject missing authority,
reused PIDs, unknown identity, shared/protected targets and mismatched ownership.
They also demonstrate regex matching of a synthetic ancestor command line without
calling `pkill`, spawning a build or sending signals.

```sh
python -m unittest discover -s scripts -p 'test_*.py' -v
```

The gate consumes already-collected evidence; it does not authenticate that evidence,
inspect live processes or make inspect-and-act atomic. A `review-stop` decision is
not permission or an instruction to signal a process. These tests do not verify any
particular agent platform's cancellation, descendant cleanup or timeout semantics.

## Sources and provenance

Independently authored guidance; no private transcripts or project identifiers are
included. Reviewed sources:

- [procps pgrep/pkill manual](https://man7.org/linux/man-pages/man1/pgrep.1.html): full-command-line matching, default SIGTERM, ancestor filtering and matching-utility exclusion.
- [Linux proc PID stat](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html): parent, group, session and start-time fields; Linux-specific, not a portable process API.
- [Python subprocess documentation](https://docs.python.org/3/library/subprocess.html): wait timeouts, child return codes and process lifecycle. A tool wrapper can add different timeout semantics; inspect its actual response.

The procedure complements evidence-preservation workflows; it does not replace
application-specific shutdown requirements or a human's recovery authorization.
