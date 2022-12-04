from __future__ import annotations

import subprocess


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["./check_zpool_scrub.py"] + args,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
