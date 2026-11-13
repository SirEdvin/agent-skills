"""Signal-free synthetic checks; never discover or terminate host processes."""
import dataclasses
import re
import unittest

from recovery_decisions import Identity, assess


class RecoveryDecisions(unittest.TestCase):
    def setUp(self):
        self.original = Identity(101, "fixture-boot", 500, "fixture-task-a")
        self.flags = dict(authorized=True, exclusive=True, protected=False,
                          progress=False, wait_only=False)

    def decide(self, observed=None, **overrides):
        flags = self.flags | overrides
        return assess(self.original, observed or self.original, **flags)

    def test_verified_scope_only_recommends_review(self):
        self.assertEqual(self.decide(), "review-stop")

    def test_permission_is_not_inferred(self):
        self.assertEqual(self.decide(authorized=False), "checkpoint-permission-required")

    def test_pid_reuse(self):
        changed = dataclasses.replace(self.original, started=501)
        self.assertEqual(self.decide(changed), "checkpoint-identity-changed")

    def test_boot_change(self):
        changed = dataclasses.replace(self.original, boot="another-boot")
        self.assertEqual(self.decide(changed), "checkpoint-identity-changed")

    def test_same_user_executable_is_not_task_identity(self):
        changed = dataclasses.replace(self.original, owner="fixture-task-b")
        self.assertEqual(self.decide(changed), "checkpoint-identity-changed")

    def test_unknown_fields(self):
        for field in ("pid", "boot", "started", "owner"):
            with self.subTest(field=field):
                changed = dataclasses.replace(self.original, **{field: None})
                self.assertEqual(self.decide(changed), "checkpoint-unknown-identity")

    def test_invalid_identity_types(self):
        for field, value in (("pid", True), ("pid", 0), ("started", -1),
                             ("boot", " "), ("owner", "")):
            with self.subTest(field=field, value=value):
                changed = dataclasses.replace(self.original, **{field: value})
                self.assertEqual(self.decide(changed), "checkpoint-unknown-identity")

    def test_protected_ancestor(self):
        self.assertEqual(self.decide(protected=True), "checkpoint-shared-or-protected")

    def test_shared_group(self):
        self.assertEqual(self.decide(exclusive=False), "checkpoint-shared-or-protected")

    def test_unknown_flags_fail_closed(self):
        self.assertEqual(self.decide(exclusive=None), "checkpoint-shared-or-protected")
        self.assertEqual(self.decide(protected=None), "checkpoint-shared-or-protected")
        self.assertEqual(self.decide(authorized="yes"), "checkpoint-permission-required")
        self.assertEqual(self.decide(progress=None), "observe-existing-job")

    def test_wait_window_is_not_build_failure(self):
        self.assertEqual(self.decide(wait_only=True), "observe-existing-job")

    def test_progress_is_not_a_stall(self):
        self.assertEqual(self.decide(progress=True), "observe-existing-job")

    def test_missing_process_requires_exit_inspection(self):
        self.assertEqual(assess(self.original, None, **self.flags),
                         "inspect-exit-and-outputs")

    def test_broad_match_includes_synthetic_supervisor(self):
        # No shell command is executed: this models full-command-line matching.
        pattern = "worker-build"
        lines = ["worker-build --task a", "worker-build --task b",
                 "sh -c 'pkill -f worker-build; print-recovery-status'"]
        self.assertEqual([bool(re.search(pattern, line)) for line in lines],
                         [True, True, True])


if __name__ == "__main__":
    unittest.main()
