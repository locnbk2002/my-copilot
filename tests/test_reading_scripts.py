"""Tests for log-reading scripts — verify they read from per-session log dirs."""
import json, os, sys, subprocess, tempfile, unittest
from pathlib import Path

scripts_dir = Path(__file__).resolve().parent.parent / "my-copilot" / ".github" / "scripts"
sys.path.insert(0, str(scripts_dir))
import hook_utils


class ReadingScriptTestBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.orig_log_base = hook_utils.LOG_BASE
        hook_utils.LOG_BASE = Path(self.tmp)
        self.real_cwd = os.getcwd()
        # Subprocess PPID = our PID — pre-populate session keyed by our PID
        proj_hash = hook_utils.get_project_hash(self.real_cwd)
        sessions_dir = Path(self.tmp) / proj_hash / ".sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        self.session_id = "reader-test-session"
        (sessions_dir / str(os.getpid())).write_text(self.session_id)
        self.log_dir = Path(self.tmp) / proj_hash / self.session_id
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        hook_utils.LOG_BASE = self.orig_log_base

    def run_script(self, script_name, stdin_data):
        env = os.environ.copy()
        env["HOOK_LOG_BASE"] = self.tmp
        proc = subprocess.run(
            [sys.executable, str(scripts_dir / script_name)],
            input=json.dumps(stdin_data),
            capture_output=True, text=True, env=env
        )
        return proc

    def write_log(self, filename, entries):
        """Pre-populate a log file in the session directory (matches subprocess's session lookup)."""
        p = self.log_dir / filename
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w") as f:
            for e in entries:
                f.write(json.dumps(e, separators=(",", ":")) + "\n")


class TestAgentBabysitter(ReadingScriptTestBase):
    def test_detects_loop_from_per_session_logs(self):
        # Pre-populate subagents.jsonl with 3 identical entries (loop condition)
        entries = [
            {"event": "launch", "agent_type": "explore", "prompt_preview": "find files", "timestamp": "2026-01-01T00:00:00Z"},
            {"event": "launch", "agent_type": "explore", "prompt_preview": "find files", "timestamp": "2026-01-01T00:01:00Z"},
            {"event": "launch", "agent_type": "explore", "prompt_preview": "find files", "timestamp": "2026-01-01T00:02:00Z"},
        ]
        self.write_log("subagents.jsonl", entries)

        payload = {
            "toolName": "task",
            "toolArgs": {"agent_type": "explore", "prompt": "find files"},
            "timestamp": "2026-01-01T00:03:00Z"
        }
        proc = self.run_script("agent-babysitter.py", payload)
        self.assertEqual(proc.returncode, 0, proc.stderr)

        # Should have written to agent-health.jsonl in session dir
        found = list(Path(self.tmp).glob("**/agent-health.jsonl"))
        self.assertTrue(len(found) > 0, f"agent-health.jsonl not found in {self.tmp}")
        entry = json.loads(found[0].read_text().strip())
        self.assertIn("warning", entry.get("severity", ""))

    def test_no_loop_exits_cleanly(self):
        # Different agents — no loop
        entries = [
            {"event": "launch", "agent_type": "explore", "prompt_preview": "find files"},
            {"event": "launch", "agent_type": "task", "prompt_preview": "run tests"},
            {"event": "launch", "agent_type": "general-purpose", "prompt_preview": "implement"},
        ]
        self.write_log("subagents.jsonl", entries)

        payload = {
            "toolName": "task",
            "toolArgs": {"agent_type": "explore", "prompt": "find files"},
        }
        proc = self.run_script("agent-babysitter.py", payload)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        found = list(Path(self.tmp).glob("**/agent-health.jsonl"))
        self.assertEqual(len(found), 0, "Should not detect loop with different agents")

    def test_ignores_non_task_tools(self):
        payload = {"toolName": "bash", "toolArgs": {"command": "ls"}}
        proc = self.run_script("agent-babysitter.py", payload)
        self.assertEqual(proc.returncode, 0)
        found = list(Path(self.tmp).glob("**/agent-health.jsonl"))
        self.assertEqual(len(found), 0)


class TestAutoCompactReminder(ReadingScriptTestBase):
    def test_counts_from_per_session_tools(self):
        # Write exactly 100 tool entries
        entries = [{"timestamp": f"2026-01-01T00:{i:02d}:00Z", "toolName": "bash"} for i in range(100)]
        self.write_log("tools.jsonl", entries)

        payload = {"timestamp": "2026-01-01T02:00:00Z"}
        proc = self.run_script("auto-compact-reminder.py", payload)
        self.assertEqual(proc.returncode, 0, proc.stderr)

        found = list(Path(self.tmp).glob("**/compact-reminders.jsonl"))
        self.assertTrue(len(found) > 0, "compact-reminders.jsonl not found — should trigger at 100 tool calls")
        entry = json.loads(found[0].read_text().strip())
        self.assertEqual(entry["toolCount"], 100)

    def test_no_reminder_at_non_threshold(self):
        # Write 50 entries — not at 100 threshold
        entries = [{"toolName": "bash"} for _ in range(50)]
        self.write_log("tools.jsonl", entries)

        payload = {"timestamp": "2026-01-01T01:00:00Z"}
        proc = self.run_script("auto-compact-reminder.py", payload)
        self.assertEqual(proc.returncode, 0)
        found = list(Path(self.tmp).glob("**/compact-reminders.jsonl"))
        self.assertEqual(len(found), 0, "Should not write reminder at non-threshold count")


class TestContextRecovery(ReadingScriptTestBase):
    def test_reads_from_per_session_logs(self):
        # Populate tools.jsonl and subagents.jsonl
        tools = [{"toolName": "bash", "timestamp": f"t{i}"} for i in range(10)]
        self.write_log("tools.jsonl", tools)
        self.write_log("subagents.jsonl", [{"event": "launch", "agent_type": "explore"}])

        payload = {
            "error": {"name": "ContextError", "message": "context window exceeded token limit"},
            "timestamp": "2026-01-01T00:00:00Z"
        }
        proc = self.run_script("context-recovery.py", payload)
        self.assertEqual(proc.returncode, 0, proc.stderr)

        found = list(Path(self.tmp).glob("**/context-recovery.jsonl"))
        self.assertTrue(len(found) > 0, "context-recovery.jsonl not found")
        entry = json.loads(found[0].read_text().strip())
        self.assertIn("recentTools", entry)
        self.assertIsNotNone(entry.get("activeAgent"))

    def test_ignores_non_context_errors(self):
        payload = {
            "error": {"name": "SomeError", "message": "something unrelated"},
        }
        proc = self.run_script("context-recovery.py", payload)
        self.assertEqual(proc.returncode, 0)
        found = list(Path(self.tmp).glob("**/context-recovery.jsonl"))
        self.assertEqual(len(found), 0, "Should not write for non-context errors")


if __name__ == "__main__":
    unittest.main()
