"""Exercise artifact preservation and removed-cwd recovery in disposable fixtures."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class LifecycleTests(unittest.TestCase):
    def test_receipt_does_not_preserve_payload(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            work, durable = root / "work", root / "durable"
            work.mkdir()
            durable.mkdir()
            source = work / "evidence.bin"
            source.write_bytes(b"synthetic evidence\x00\xff")
            expected = hashlib.sha256(source.read_bytes()).hexdigest()
            saved = durable / source.name
            receipt = durable / "receipt.json"
            receipt.write_text(json.dumps({"required_payload": saved.name,
                                           "sha256": expected}), encoding="utf-8")

            def verify_payload():
                recorded = json.loads(receipt.read_text(encoding="utf-8"))
                payload = durable / recorded["required_payload"]
                self.assertTrue(payload.is_file(), "required payload missing")
                self.assertEqual(hashlib.sha256(payload.read_bytes()).hexdigest(),
                                 recorded["sha256"], "required payload differs")

            # A real receipt and declared digest cannot stand in for the payload.
            with self.assertRaisesRegex(AssertionError, "required payload missing"):
                verify_payload()
            # A symlink into disposable storage is not a preserved payload either.
            saved.symlink_to(source)
            self.assertTrue(saved.resolve().is_relative_to(work))
            saved.unlink()
            shutil.copy2(source, saved)
            self.assertFalse(saved.resolve().is_relative_to(work))
            verify_payload()
            shutil.rmtree(work)  # Only this test's own disposable directory.
            verify_payload()
            saved.write_bytes(b"corrupted")
            with self.assertRaisesRegex(AssertionError, "required payload differs"):
                verify_payload()

    def test_readback_survives_worktree_removal(self):
        self.assertIsNotNone(shutil.which("git"), "Git is required for this fixture")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            repo, work, durable = root / "repo", root / "work", root / "durable"
            repo.mkdir()
            durable.mkdir()

            def git(*args):
                return subprocess.run(["git", "-C", str(repo), *args],
                                      check=True, capture_output=True, text=True).stdout

            git("init")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-m", "fixture")
            git("worktree", "add", "--detach", str(work), "HEAD")
            receipt = {"record": "synthetic", "expected": "completed"}
            saved = durable / "receipt.json"
            saved.write_text(json.dumps(receipt), encoding="utf-8")
            self.assertEqual(json.loads(saved.read_text()), receipt)
            git("worktree", "remove", str(work))
            self.assertFalse(work.exists())
            self.assertNotIn("worktree " + str(work), git("worktree", "list", "--porcelain"))
            command = [sys.executable, "-c",
                       "import json,pathlib,sys; "
                       "r=json.loads(pathlib.Path(sys.argv[1]).read_text()); "
                       "assert r == {'record':'synthetic','expected':'completed'}; "
                       "print('durable receipt verified')", str(saved)]
            with self.assertRaises(FileNotFoundError):
                subprocess.run(command, cwd=work, capture_output=True, check=True)
            result = subprocess.run(command, cwd=durable, capture_output=True,
                                    text=True, check=True)
            self.assertEqual(result.stdout, "durable receipt verified\n")


if __name__ == "__main__":
    unittest.main()
