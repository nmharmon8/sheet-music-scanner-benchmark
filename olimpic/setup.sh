#!/bin/bash
# Fetches what the OLiMPiC benchmark needs into olimpic/ (all gitignored): the scanned test set, the authors'
# code at a pinned commit (their linearizer and TEDn scorer), and a Python venv with its two dependencies.
# Safe to run again: it skips what is already there.
set -euo pipefail
cd "$(dirname "$0")"
REPO=https://github.com/ufal/olimpic-icdar24
COMMIT=f4f45ac523ebe09832342270a68b1b4368f63da2   # 2026-09-29
DATA=$REPO/releases/download/datasets/olimpic-1.0-scanned.2024-02-12.tar.gz

if [ ! -d data/olimpic-1.0-scanned ]; then
  mkdir -p data
  curl -fL --progress-bar -o data/scanned.tgz "$DATA"
  tar xzf data/scanned.tgz -C data && rm data/scanned.tgz
fi
if [ ! -d vendor/olimpic-icdar24 ]; then
  git clone -q "$REPO" vendor/olimpic-icdar24
  git -C vendor/olimpic-icdar24 checkout -q "$COMMIT"
fi
if [ ! -x .venv/bin/python ]; then
  if command -v uv >/dev/null; then
    uv venv -q .venv && VIRTUAL_ENV=$PWD/.venv uv pip install -q 'zss==1.2.0' 'Levenshtein==0.27.1'
  else
    python3 -m venv .venv && .venv/bin/pip install -q 'zss==1.2.0' 'Levenshtein==0.27.1'
  fi
fi
echo "ready: $(wc -l < data/olimpic-1.0-scanned/samples.test.txt) test systems, $(wc -l < sample.txt) in the standard sample"
