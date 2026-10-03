from __future__ import annotations

from threading import Thread
from time import monotonic, sleep
import subprocess

from .process import snapshot as process_snapshot
from .system import snapshot as system_snapshot


def profile_command(command: list[str], interval: float = .1, include_system: bool = True) -> tuple[list[dict], int]:
    if not command:
        raise ValueError("command is empty")
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    started = monotonic()
    rows = []

    while proc.poll() is None:
        try:
            memory = process_snapshot(proc.pid)
            row = {
                "type":"sample",
                "t_seconds": monotonic() - started,
                "pid": proc.pid,
                "rss_kb": memory.rss_kb,
                "vsz_kb": memory.vsz_kb,
                "child_rss_kb": memory.child_rss_kb,
                "state": memory.state,
            }
            if include_system:
                row["system"] = system_snapshot()
            rows.append(row)
        except Exception:
            pass
        sleep(interval)

    stdout, stderr = proc.communicate()
    rows.append({
        "type":"process_end",
        "t_seconds": monotonic() - started,
        "pid": proc.pid,
        "returncode": proc.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "command": command,
    })
    return rows, int(proc.returncode or 0)
