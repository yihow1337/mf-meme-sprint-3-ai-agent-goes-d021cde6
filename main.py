#!/usr/bin/env python3
"""Entry point: emit the meme PNG to the output directory.

Writes the repository's prebuilt entry.png (drawn by tools/render.py with
Pillow, shapes and text only) to $MAKEFUN_OUTPUT_DIR or /output as entry.png,
byte-for-byte identical on every run. Standard library only.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def output_dir():
    d = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(d, exist_ok=True)
        return d
    except OSError:
        d = HERE
        return d


def main():
    with open(SRC, "rb") as f:
        data = f.read()
    dest = os.path.join(output_dir(), "entry.png")
    with open(dest, "wb") as f:
        f.write(data)
    print("wrote {} ({} bytes)".format(dest, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
