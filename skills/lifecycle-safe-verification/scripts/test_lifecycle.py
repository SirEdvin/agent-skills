"""Exercise removed-cwd recovery only inside a disposable Git fixture."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class LifecycleTests(unittest.TestCase):
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
