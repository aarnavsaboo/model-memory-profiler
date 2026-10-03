from __future__ import annotations

from dataclasses import dataclass
import subprocess


@dataclass(frozen=True)
class ProcessMemory:
    pid: int
    rss_kb: int
    vsz_kb: int
    child_rss_kb: int
    state: str


def _ps(pid: int) -> tuple[int, int, str]:
    out = subprocess.check_output(
        ["ps", "-o", "rss=,vsz=,state=", "-p", str(pid)],
        text=True,
    ).strip()
    if not out:
        raise ProcessLookupError(pid)
    rss, vsz, state = out.split(maxsplit=2)
    return int(rss), int(vsz), state


def child_pids(pid: int) -> list[int]:
    try:
        out = subprocess.check_output(["pgrep", "-P", str(pid)], text=True).strip()
    except subprocess.CalledProcessError:
        return []
    return [int(x) for x in out.splitlines() if x.strip().isdigit()]


def snapshot(pid: int) -> ProcessMemory:
    rss, vsz, state = _ps(pid)
    children = 0
    for child in child_pids(pid):
        try:
            child_rss, _, _ = _ps(child)
            children += child_rss
        except (subprocess.CalledProcessError, ProcessLookupError, ValueError):
            pass
    return ProcessMemory(pid, rss, vsz, children, state)
