"""Shared utilities for hook scripts. Provides session-aware log directory resolution."""
import hashlib, json, os, uuid
from pathlib import Path

LOG_BASE = Path(os.environ.get("HOOK_LOG_BASE",
    str(Path.home() / ".local" / "share" / ".copilot" / "my-copilot" / "logs")))


def get_project_hash(cwd: str | None = None) -> str:
    """SHA256[:12] of CWD — deterministic project identifier."""
    cwd = cwd or os.getcwd()
    return hashlib.sha256(cwd.encode()).hexdigest()[:12]


def _sessions_dir(cwd: str | None = None) -> Path:
    return LOG_BASE / get_project_hash(cwd) / ".sessions"


def _ppid() -> str:
    return str(os.getppid())


def init_session(session_id: str | None = None, cwd: str | None = None) -> str:
    """Initialize session: generate/write session ID keyed by PPID. Returns session ID."""
    sid = session_id or str(uuid.uuid4())
    sdir = _sessions_dir(cwd)
    sdir.mkdir(parents=True, exist_ok=True)
    (sdir / _ppid()).write_text(sid)
    get_log_dir(cwd)
    return sid


def end_session(cwd: str | None = None) -> None:
    """Remove PID-keyed session file on session end."""
    path = _sessions_dir(cwd) / _ppid()
    try:
        path.unlink()
    except (FileNotFoundError, OSError):
        pass


def get_session_id(cwd: str | None = None) -> str:
    """Read session ID from PID-keyed file. Returns 'unknown' if missing."""
    path = _sessions_dir(cwd) / _ppid()
    try:
        return path.read_text().strip()
    except (FileNotFoundError, OSError):
        return "unknown"


def get_log_dir(cwd: str | None = None) -> Path:
    """Return per-session log directory, creating if needed."""
    d = LOG_BASE / get_project_hash(cwd) / get_session_id(cwd)
    d.mkdir(parents=True, exist_ok=True)
    return d


def log_path(filename: str, cwd: str | None = None) -> Path:
    """Return full path to a log file in the session log dir."""
    return get_log_dir(cwd) / filename


def append_log(filename: str, data: dict, cwd: str | None = None) -> None:
    """Append a compact JSON line to a log file."""
    p = log_path(filename, cwd)
    with open(p, "a") as f:
        f.write(json.dumps(data, separators=(",", ":")) + "\n")


def read_log_tail(filename: str, n: int = 10, cwd: str | None = None) -> list:
    """Read last N entries from a JSONL log file. Returns list of dicts."""
    from collections import deque
    p = log_path(filename, cwd)
    try:
        with open(p, "r") as f:
            lines = deque(f, maxlen=n)
        return [json.loads(line.strip()) for line in lines if line.strip()]
    except (FileNotFoundError, OSError):
        return []


def count_log_lines(filename: str, cwd: str | None = None) -> int:
    """Count lines in a JSONL log file. Returns 0 if missing."""
    p = log_path(filename, cwd)
    try:
        with open(p, "r") as f:
            return sum(1 for _ in f)
    except (FileNotFoundError, OSError):
        return 0
