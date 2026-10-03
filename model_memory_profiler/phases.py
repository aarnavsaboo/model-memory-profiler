from dataclasses import dataclass


@dataclass(frozen=True)
class Phase:
    name: str
    t_seconds: float


def parse_marker(line: str, prefix: str = "PROFILE_PHASE:") -> str | None:
    stripped = line.strip()
    if not stripped.startswith(prefix):
        return None
    name = stripped[len(prefix):].strip()
    return name or None
