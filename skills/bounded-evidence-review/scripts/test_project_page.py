import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from project_page import project


class PageTests(unittest.TestCase):
    def test_all_pages_bounded_and_complete(self):
        data = {"runs": [{"id": i, "summary": '🌒\n"\\' * 1000,
                          "nested": [{"large": "x" * 1000}] * 100}
                         for i in range(37)]}
        offset, ids = 0, []
        while True:
            raw = project(data, "runs", ["id", "summary", "nested"],
                          offset=offset, limit=8, max_bytes=1400, chars=40)
            self.assertLessEqual(len(raw), 1400)
            page = json.loads(raw)
            self.assertEqual(page["total"], 37)
            self.assertEqual(page["returned"], len(page["rows"]))
            self.assertLessEqual(page["returned"], 8)
            for row in page["rows"]:
                self.assertTrue(row["summary"]["truncated"])
                self.assertEqual(row["nested"], {"type": "list", "count": 100})
                ids.append(row["id"])
            if not page["has_more"]:
                self.assertIsNone(page["next_offset"])
                break
            self.assertGreater(page["next_offset"], offset)
            offset = page["next_offset"]
        self.assertEqual(ids, list(range(37)))

    def test_empty_and_end(self):
        for data, offset in [({"runs": []}, 0), ({"runs": [{"id": 1}]}, 1)]:
            page = json.loads(project(data, "runs", ["id"], offset=offset))
            self.assertEqual(page["rows"], [])
            self.assertFalse(page["has_more"])

    def test_exact_byte_boundary(self):
        data = {"runs": [{"id": 1}]}
        raw = project(data, "runs", ["id"])
        self.assertEqual(project(data, "runs", ["id"], max_bytes=len(raw)), raw)
        with self.assertRaises(ValueError):
            project(data, "runs", ["id"], max_bytes=len(raw) - 1)

    def test_bad_schema_and_limits(self):
        for data in [[], {}, {"runs": None}, {"runs": [1]}]:
            with self.assertRaises(ValueError):
                project(data, "runs", ["id"])
        for kw in [{"offset": -1}, {"offset": 2}, {"limit": 0},
                   {"max_bytes": 0}, {"chars": 0}]:
            with self.assertRaises(ValueError):
                project({"runs": []}, "runs", ["id"], **kw)

    def test_cli_fixture_and_error(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "snapshot.json"
            source.write_text(json.dumps({"runs": [{"id": 1, "status": "ok"}]}))
            cmd = [sys.executable, str(Path(__file__).with_name("project_page.py")),
                   str(source), "--collection", "runs", "--fields", "id,status",
                   "--offset", "0", "--limit", "8", "--max-bytes", "4096"]
            result = subprocess.run(cmd, capture_output=True, check=True)
            self.assertEqual(json.loads(result.stdout)["returned"], 1)
            self.assertLessEqual(len(result.stdout), 4096)
            source.write_text("invalid json")
            result = subprocess.run(cmd, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b"")
            self.assertLess(len(result.stderr), 200)


if __name__ == "__main__":
    unittest.main()
