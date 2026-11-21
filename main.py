#!/usr/bin/env python3
"""Entry for make.fun the-passport-page-of-a-countr-2-20261121-0318.

Copies the bundled passport spread (entry.png, rendered in advance)
to the output directory. Standard library only: no network, no clock,
no randomness, no image libraries, no local imports. The bundled image
is copied byte-for-byte, so two runs write identical output.

Run as the grader does: ``python3 -P -s main.py`` (or plain
``python3 main.py``). Writes ``$MAKEFUN_OUTPUT_DIR/entry.png``,
defaulting to ``/output/entry.png``.
"""

import hashlib
import os
import shutil
import sys

OUTPUT_NAME = "entry.png"


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, OUTPUT_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, OUTPUT_NAME)
    shutil.copyfile(source, target)
    size = os.path.getsize(target)
    if size != os.path.getsize(source):
        print("copy failed: size mismatch", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)"
          % (target, size, _sha256(target)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
