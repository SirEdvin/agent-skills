"""Pure advisory decisions over synthetic/already-collected process evidence.

No process discovery, shell execution, signals or authorization is performed.
Even 'review-stop' requires fresh platform-specific checks before an authorized act.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Identity:
    pid: int | None
    boot: str | None
    started: int | None
    owner: str | None

    def known(self) -> bool:
        return (
            type(self.pid) is int and self.pid > 0
            and type(self.started) is int and self.started >= 0
            and isinstance(self.boot, str) and bool(self.boot.strip())
            and isinstance(self.owner, str) and bool(self.owner.strip())
        )


def assess(
    expected: Identity,
    observed: Identity | None,
    *,
    authorized: bool,
    exclusive: bool,
    protected: bool,
    progress: bool,
    wait_only: bool,
) -> str:
    """Return a checkpoint recommendation, never a signal target."""
    if observed is None:
        return "inspect-exit-and-outputs"
    if not expected.known() or not observed.known():
        return "checkpoint-unknown-identity"
    if expected != observed:
        return "checkpoint-identity-changed"
    if protected is not False or exclusive is not True:
        return "checkpoint-shared-or-protected"
    if progress is not False or wait_only is not False:
        return "observe-existing-job"
    if authorized is not True:
        return "checkpoint-permission-required"
    return "review-stop"
