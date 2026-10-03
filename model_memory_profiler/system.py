from __future__ import annotations

import re
import subprocess


def _vm_stat() -> dict[str, int]:
    text = subprocess.check_output(["vm_stat"], text=True)
    page_match = re.search(r"page size of (\d+) bytes", text)
    page_size = int(page_match.group(1)) if page_match else 4096
    out = {"page_size": page_size}
    for line in text.splitlines()[1:]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        digits = re.sub(r"[^0-9]", "", value)
        if digits:
            out[key.strip().lower().replace(" ", "_")] = int(digits)
    return out


def _swap() -> dict[str, str]:
    try:
        text = subprocess.check_output(["sysctl", "-n", "vm.swapusage"], text=True).strip()
    except subprocess.CalledProcessError:
        return {}
    return {"swapusage": text}


def snapshot() -> dict:
    out = {}
    try:
        out["vm_stat"] = _vm_stat()
    except (FileNotFoundError, subprocess.CalledProcessError):
        out["vm_stat"] = {}
    out.update(_swap())
    return out
