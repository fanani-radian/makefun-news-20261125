#!/usr/bin/env python3
"""make.fun news-image-20261125 entry: 'World News — 25 November 2026'.

Writes the bundled front-page image to the output directory. Runs with no
network and is fully deterministic: both runs write identical bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

SRC = os.path.join(HERE, "entry.png")
DST = os.path.join(OUT, "entry.png")

if not os.path.isfile(SRC):
    raise FileNotFoundError(f"source entry image missing: {SRC}")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, DST)

if not os.path.isfile(DST):
    raise FileNotFoundError(f"output entry image missing after copy: {DST}")
src_size = os.path.getsize(SRC)
dst_size = os.path.getsize(DST)
if dst_size != src_size:
    raise IOError(
        f"output size mismatch: {DST} is {dst_size} bytes, expected {src_size} bytes"
    )

print(f"wrote {DST} ({dst_size} bytes)")
