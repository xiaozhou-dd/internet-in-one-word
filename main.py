#!/usr/bin/env python3
"""Write the one-word entry to /output/entry.txt.

Reads entry.txt next to this file, strips exactly one trailing newline,
checks the result is a single lowercase word, and writes it byte-for-byte
to /output/entry.txt with no trailing newline.

Usage: python3 main.py
On success it exits 0 and prints nothing; on failure it prints an error
to stderr and exits 1.
"""

import os
import re
import sys
from pathlib import Path

WORD = re.compile(r"[a-z]+")


def read_entry(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        print(f"error: cannot read {path}: {exc}", file=sys.stderr)
        raise SystemExit(1)


def strip_one_newline(data: bytes) -> bytes:
    if data.endswith(b"\r\n"):
        return data[:-2]
    if data.endswith(b"\n"):
        return data[:-1]
    return data


def main() -> int:
    entry_path = Path(__file__).resolve().parent / "entry.txt"
    data = strip_one_newline(read_entry(entry_path))
    if not data:
        print("error: entry is empty", file=sys.stderr)
        return 1
    try:
        word = data.decode("utf-8")
    except UnicodeDecodeError:
        print("error: entry is not valid UTF-8", file=sys.stderr)
        return 1
    if not WORD.fullmatch(word):
        print("error: entry must be one lowercase word", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.txt").write_bytes(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
