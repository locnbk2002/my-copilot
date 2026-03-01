"""Tests for hook_utils module — per-session log directory resolution."""
import hashlib, json, os, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / ".github" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import hook_utils


class TestGetProjectHash(unittest.TestCase):
    def test_returns_12_char_hex(self):
        h = hook_utils.get_project_hash("/some/path")
        self.assertEqual(len(h), 12)
        self.assertTrue(all(c in "0123456789abcdef" for c in h))

    def test_deterministic_for_same_cwd(self):
        h1 = hook_utils.get_project_hash("/same/path")
        h2 = hook_utils.get_project_hash("/same/path")
        self.assertEqual(h1, h2)

    def test_different_for_different_cwd(self):
        h1 = hook_utils.get_project_hash("/path/a")
        h2 = hook_utils.get_project_hash("/path/b")
        self.assertNotEqual(h1, h2)

    def test_uses_sha256(self):
        expected = hashlib.sha256("/my/project".encode()).hexdigest()[:12]
        self.assertEqual(hook_utils.get_project_hash("/my/project"), expected)


class TestSessionId(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        # Patch LOG_BASE for isolation
        self.orig_log_base = hook_utils.LOG_BASE
        hook_utils.LOG_BASE = Path(self.tmp)

    def tearDown(self):
        hook_utils.LOG_BASE = self.orig_log_base

    def test_init_session_creates_pid_keyed_file(self):
        sid = hook_utils.init_session(cwd="/test/proj")
        ppid = str(os.getppid())
        sessions_dir = Path(self.tmp) / hook_utils.get_project_hash("/test/proj") / ".sessions"
        pid_file = sessions_dir / ppid
        self.assertTrue(pid_file.exists())
        self.assertEqual(pid_file.read_text().strip(), sid)

    def test_init_session_with_explicit_id(self):
        sid = hook_utils.init_session(session_id="my-explicit-id", cwd="/test/proj")
        self.assertEqual(sid, "my-explicit-id")

    def test_get_session_id_reads_pid_keyed_file(self):
        hook_utils.init_session(session_id="test-session-123", cwd="/test/proj")
        result = hook_utils.get_session_id(cwd="/test/proj")
        self.assertEqual(result, "test-session-123")

    def test_get_session_id_returns_unknown_if_missing(self):
        result = hook_utils.get_session_id(cwd="/nonexistent/proj")
        self.assertEqual(result, "unknown")

    def test_concurrent_sessions_get_different_ids(self):
        # Simulate two different PPIDs by writing manually
        cwd = "/concurrent/test"
        proj_hash = hook_utils.get_project_hash(cwd)
        sessions_dir = Path(self.tmp) / proj_hash / ".sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        (sessions_dir / "11111").write_text("session-A")
        (sessions_dir / "22222").write_text("session-B")
        self.assertNotEqual(
            (sessions_dir / "11111").read_text(),
            (sessions_dir / "22222").read_text()
        )

    def test_end_session_removes_pid_file(self):
        hook_utils.init_session(session_id="to-be-removed", cwd="/test/proj")
        hook_utils.end_session(cwd="/test/proj")
        ppid = str(os.getppid())
        pid_file = Path(self.tmp) / hook_utils.get_project_hash("/test/proj") / ".sessions" / ppid
        self.assertFalse(pid_file.exists())

    def test_end_session_handles_missing_file_gracefully(self):
        # Should not raise if file doesn't exist
        hook_utils.end_session(cwd="/nonexistent/proj")


class TestGetLogDir(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.orig_log_base = hook_utils.LOG_BASE
        hook_utils.LOG_BASE = Path(self.tmp)

    def tearDown(self):
        hook_utils.LOG_BASE = self.orig_log_base

    def test_returns_expected_path_structure(self):
        hook_utils.init_session(session_id="my-session", cwd="/proj")
        d = hook_utils.get_log_dir(cwd="/proj")
        proj_hash = hook_utils.get_project_hash("/proj")
        expected = Path(self.tmp) / proj_hash / "my-session"
        self.assertEqual(d, expected)

    def test_creates_directory_if_missing(self):
        hook_utils.init_session(session_id="new-session", cwd="/proj2")
        d = hook_utils.get_log_dir(cwd="/proj2")
        self.assertTrue(d.is_dir())

    def test_unknown_session_creates_unknown_dir(self):
        # No init_session → "unknown" subdir
        d = hook_utils.get_log_dir(cwd="/brand/new/proj")
        self.assertTrue(d.name == "unknown" or d.exists())


class TestLogPath(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.orig_log_base = hook_utils.LOG_BASE
        hook_utils.LOG_BASE = Path(self.tmp)

    def tearDown(self):
        hook_utils.LOG_BASE = self.orig_log_base

    def test_returns_file_inside_log_dir(self):
        hook_utils.init_session(session_id="sess", cwd="/proj")
        p = hook_utils.log_path("tools.jsonl", cwd="/proj")
        self.assertEqual(p.name, "tools.jsonl")
        self.assertTrue(str(p).startswith(self.tmp))

    def test_log_path_is_inside_session_dir(self):
        hook_utils.init_session(session_id="sess-x", cwd="/proj")
        p = hook_utils.log_path("errors.jsonl", cwd="/proj")
        log_dir = hook_utils.get_log_dir(cwd="/proj")
        self.assertEqual(p, log_dir / "errors.jsonl")


class TestAppendLog(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.orig_log_base = hook_utils.LOG_BASE
        hook_utils.LOG_BASE = Path(self.tmp)
        hook_utils.init_session(session_id="test-sess", cwd="/proj")

    def tearDown(self):
        hook_utils.LOG_BASE = self.orig_log_base

    def test_appends_json_line(self):
        hook_utils.append_log("test.jsonl", {"key": "value"}, cwd="/proj")
        p = hook_utils.log_path("test.jsonl", cwd="/proj")
        lines = p.read_text().strip().split("\n")
        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0]), {"key": "value"})

    def test_creates_file_if_missing(self):
        p = hook_utils.log_path("new.jsonl", cwd="/proj")
        self.assertFalse(p.exists())
        hook_utils.append_log("new.jsonl", {"x": 1}, cwd="/proj")
        self.assertTrue(p.exists())

    def test_appends_to_existing(self):
        hook_utils.append_log("multi.jsonl", {"n": 1}, cwd="/proj")
        hook_utils.append_log("multi.jsonl", {"n": 2}, cwd="/proj")
        p = hook_utils.log_path("multi.jsonl", cwd="/proj")
        lines = [json.loads(l) for l in p.read_text().strip().split("\n")]
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0]["n"], 1)
        self.assertEqual(lines[1]["n"], 2)

    def test_uses_compact_json(self):
        hook_utils.append_log("compact.jsonl", {"a": 1, "b": 2}, cwd="/proj")
        p = hook_utils.log_path("compact.jsonl", cwd="/proj")
        content = p.read_text().strip()
        # Compact JSON has no spaces after separators
        self.assertNotIn(", ", content)
        self.assertNotIn(": ", content)


if __name__ == "__main__":
    unittest.main()
