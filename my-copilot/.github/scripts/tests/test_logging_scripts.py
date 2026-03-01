"""Tests for updated logging scripts — verify per-session log paths."""
import json, os, sys, tempfile, unittest
from pathlib import Path

# Add scripts dir to path
scripts_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))
import hook_utils


class ScriptTestBase(unittest.TestCase):
    def setUp(self):
        import subprocess
        self.subprocess = subprocess
        self.tmp = tempfile.mkdtemp()
        self.scripts_dir = scripts_dir
        self.orig_log_base = hook_utils.LOG_BASE
        hook_utils.LOG_BASE = Path(self.tmp)
        # Subprocess PPID = our PID — pre-populate session keyed by our PID
        self.real_cwd = os.getcwd()
        proj_hash = hook_utils.get_project_hash(self.real_cwd)
        sessions_dir = Path(self.tmp) / proj_hash / ".sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        self.session_id = "test-session-fixed"
        (sessions_dir / str(os.getpid())).write_text(self.session_id)
        self.log_dir = Path(self.tmp) / proj_hash / self.session_id
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        hook_utils.LOG_BASE = self.orig_log_base

    def run_script(self, script_name, stdin_data):
        env = os.environ.copy()
        env["HOOK_LOG_BASE"] = self.tmp
        proc = self.subprocess.run(
            [sys.executable, str(self.scripts_dir / script_name)],
            input=json.dumps(stdin_data),
            capture_output=True, text=True, env=env
        )
        return proc


class TestSessionLogger(ScriptTestBase):
    def test_session_start_writes_to_sessions_jsonl(self):
        payload = {
            "timestamp": "2026-01-01T00:00:00Z",
            "cwd": "/fake/cwd",
            "source": "user",
            "initialPrompt": "Hello"
        }
        proc = self.run_script("session-logger.py", payload)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        # Find sessions.jsonl anywhere in log base (session init creates new dir)
        found = list(Path(self.tmp).glob("**/sessions.jsonl"))
        self.assertTrue(len(found) > 0, "sessions.jsonl not found")
        content = found[0].read_text().strip()
        self.assertTrue(len(content) > 0)
        entry = json.loads(content.split("\n")[0])
        self.assertEqual(entry["event"], "sessionStart")

    def test_session_end_writes_to_sessions_jsonl(self):
        # First start a session
        self.run_script("session-logger.py", {
            "timestamp": "2026-01-01T00:00:00Z", "cwd": "/fake/cwd",
            "source": "user", "initialPrompt": "Hi"
        })
        # Then end it
        proc = self.run_script("session-logger.py", {
            "timestamp": "2026-01-01T01:00:00Z",
            "cwd": "/fake/cwd",
            "reason": "normal"
        })
        self.assertEqual(proc.returncode, 0, proc.stderr)
        found = list(Path(self.tmp).glob("**/sessions.jsonl"))
        self.assertTrue(len(found) > 0)
        lines = [json.loads(l) for l in found[0].read_text().strip().split("\n") if l.strip()]
        events = [l["event"] for l in lines]
        self.assertIn("sessionEnd", events)


class TestToolTracker(ScriptTestBase):
    def test_writes_to_per_session_tools_jsonl(self):
        payload = {
            "timestamp": "2026-01-01T00:00:00Z",
            "toolName": "bash",
            "toolResult": {"resultType": "success"}
        }
        proc = self.run_script("tool-tracker.py", payload)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        found = list(Path(self.tmp).glob("**/tools.jsonl"))
        self.assertTrue(len(found) > 0, f"tools.jsonl not found in {self.tmp}")
        entry = json.loads(found[0].read_text().strip())
        self.assertEqual(entry["toolName"], "bash")

    def test_ignores_malformed_input(self):
        import subprocess
        env = os.environ.copy()
        env["HOOK_LOG_BASE"] = self.tmp
        proc = subprocess.run(
            [sys.executable, str(self.scripts_dir / "tool-tracker.py")],
            input="not json", capture_output=True, text=True, env=env
        )
        self.assertEqual(proc.returncode, 0)


class TestErrorLogger(ScriptTestBase):
    def test_writes_to_per_session_errors_jsonl(self):
        payload = {
            "timestamp": "2026-01-01T00:00:00Z",
            "error": {"name": "TestError", "message": "Something went wrong"}
        }
        proc = self.run_script("error-logger.py", payload)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        found = list(Path(self.tmp).glob("**/errors.jsonl"))
        self.assertTrue(len(found) > 0, "errors.jsonl not found")
        entry = json.loads(found[0].read_text().strip())
        self.assertEqual(entry["errorName"], "TestError")


class TestSubagentLaunch(ScriptTestBase):
    def test_writes_launch_event(self):
        payload = {
            "toolName": "task",
            "toolArgs": {"agent_type": "explore", "model": "claude-haiku-4.5", "prompt": "Search for files"}
        }
        proc = self.run_script("log-subagent-launch.py", payload)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        found = list(Path(self.tmp).glob("**/subagents.jsonl"))
        self.assertTrue(len(found) > 0, "subagents.jsonl not found")
        entry = json.loads(found[0].read_text().strip())
        self.assertEqual(entry["event"], "launch")
        self.assertEqual(entry["agent_type"], "explore")

    def test_ignores_non_task_tools(self):
        payload = {"toolName": "bash", "toolArgs": {"command": "ls"}}
        proc = self.run_script("log-subagent-launch.py", payload)
        self.assertEqual(proc.returncode, 0)
        found = list(Path(self.tmp).glob("**/subagents.jsonl"))
        self.assertEqual(len(found), 0, "Should not have written anything")


class TestSubagentComplete(ScriptTestBase):
    def test_writes_complete_event(self):
        payload = {
            "toolName": "task",
            "toolArgs": {"agent_type": "explore"},
            "toolResult": {"resultType": "success", "textResultForLlm": "Done"}
        }
        proc = self.run_script("log-subagent-complete.py", payload)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        found = list(Path(self.tmp).glob("**/subagents.jsonl"))
        self.assertTrue(len(found) > 0, "subagents.jsonl not found")
        entry = json.loads(found[0].read_text().strip())
        self.assertEqual(entry["event"], "complete")


class TestEditValidator(ScriptTestBase):
    def test_writes_edit_health(self):
        payload = {
            "toolName": "edit",
            "toolArgs": {"path": "/some/file.py", "old_str": "old", "new_str": "new"},
            "toolResult": {"resultType": "success"}
        }
        proc = self.run_script("edit-validator.py", payload)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        found = list(Path(self.tmp).glob("**/edit-health.jsonl"))
        self.assertTrue(len(found) > 0, "edit-health.jsonl not found")

    def test_flags_oversized_create(self):
        long_content = "\n".join(f"line {i}" for i in range(250))
        payload = {
            "toolName": "create",
            "toolArgs": {"path": "/big/file.py", "file_text": long_content},
            "toolResult": {"resultType": "success"}
        }
        proc = self.run_script("edit-validator.py", payload)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        found = list(Path(self.tmp).glob("**/edit-health.jsonl"))
        self.assertTrue(len(found) > 0)
        entry = json.loads(found[0].read_text().strip())
        self.assertTrue(entry.get("oversized", False))


class TestModelFallback(ScriptTestBase):
    def test_writes_fallback_on_rate_limit(self):
        payload = {
            "error": {"name": "RateLimitError", "message": "429 rate limit exceeded"},
            "model": "claude-opus-4.6"
        }
        proc = self.run_script("model-fallback.py", payload)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        found = list(Path(self.tmp).glob("**/model-fallback.jsonl"))
        self.assertTrue(len(found) > 0, "model-fallback.jsonl not found")

    def test_ignores_non_rate_limit_errors(self):
        payload = {
            "error": {"name": "SomeOtherError", "message": "unrelated problem"}
        }
        proc = self.run_script("model-fallback.py", payload)
        self.assertEqual(proc.returncode, 0)
        found = list(Path(self.tmp).glob("**/model-fallback.jsonl"))
        self.assertEqual(len(found), 0, "Should not have written for non-rate-limit error")


if __name__ == "__main__":
    unittest.main()
