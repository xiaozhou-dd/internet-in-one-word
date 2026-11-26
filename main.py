#!/usr/bin/env python3
"""Read entry.txt and write its contents byte-for-byte to /output/entry.txt."""

import os
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    entry_path = os.path.join(here, "entry.txt")
    try:
        with open(entry_path, "rb") as f:
            data = f.read()
    except OSError as exc:
        print(f"error: cannot read entry.txt: {exc}", file=sys.stderr)
        return 1

    # Strip only one trailing newline (LF or CRLF).
    if data.endswith(b"\r\n"):
        data = data[:-2]
    elif data.endswith(b"\n"):
        data = data[:-1]

    if not data:
        print("error: entry is empty", file=sys.stderr)
        return 1

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "wb") as f:
        f.write(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
