from __future__ import annotations

from time import monotonic, sleep

from .process import snapshot as process_snapshot
from .system import snapshot as system_snapshot


def sample_pid(
    pid: int,
    *,
    interval: float = .1,
    seconds: float | None = None,
    include_system: bool = True,
) -> list[dict]:
    if interval <= 0:
        raise ValueError("interval must be positive")
    started = monotonic()
    rows = []
    while True:
        elapsed = monotonic() - started
        if seconds is not None and elapsed > seconds:
            break
        try:
            process = process_snapshot(pid)
        except Exception:
            break
        row = {
            "type": "sample",
            "t_seconds": elapsed,
            "pid": pid,
            "rss_kb": process.rss_kb,
            "vsz_kb": process.vsz_kb,
            "child_rss_kb": process.child_rss_kb,
            "state": process.state,
        }
        if include_system:
            row["system"] = system_snapshot()
        rows.append(row)
        sleep(interval)
    return rows
