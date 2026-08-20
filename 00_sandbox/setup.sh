#!/bin/sh
# GRU953 — build the project-local sandbox.
#
# Installs NOTHING outside this repository. No Homebrew, no system fonts, no
# settings changed anywhere on the machine. Deleting .venv, 00_sandbox/node_modules
# and 00_sandbox/browsers removes the whole build environment — nothing else on
# this computer knows this project exists.
#
#   sh 00_sandbox/setup.sh
#
set -e
cd "$(dirname "$0")/.."
ROOT=$(pwd)
[ -f requirements.txt ] || { echo "Not the repository root — requirements.txt is missing."; exit 2; }

echo "== 1. checking the host interpreters =="
# Checked, not assumed. A version too old fails here with one sentence, not
# four hundred lines later with a stack trace nobody can place.
python3 -c 'import sys; raise SystemExit(0 if sys.version_info[:2] >= (3,11) else 1)' \
  || { echo "Python 3.11 or newer is needed. Found: $(python3 -V)"; exit 2; }
node -e 'process.exit(+process.versions.node.split(".")[0] >= 20 ? 0 : 1)' \
  || { echo "Node 20 or newer is needed. Found: $(node -v)"; exit 2; }
echo "   python3: $(python3 -V)    node: $(node -v)"

echo "== 2. python, pinned exactly (requirements.txt) =="
[ -d .venv ] || python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip --quiet
./.venv/bin/python -m pip install -r requirements.txt --quiet

echo "== 3. node, from the lock file, not the registry =="
# npm ci at the repository root — package.json and package-lock.json live here, not
# inside 00_sandbox/ itself. (An earlier version of this line ran `cd 00_sandbox && npm
# ci`, which happened to work only because modern npm walks up to find the nearest
# package.json — correct by accident, and unreadable to anyone checking where the
# dependencies actually come from.)
npm ci --silent
# The kit's own build helpers (render.mjs, pdf.mjs, check.mjs) have a second,
# separate package.json — they need css-tree and svgo, which nothing else in the
# repository uses.
( cd brand-kit/00_sandbox && npm ci --silent )

echo "== 4. chromium, pinned INSIDE this project =="
# Without this env var Playwright uses a cache shared with every other project on
# the machine, and this sandbox stops being something a clone of this repo alone
# can reproduce.
PLAYWRIGHT_BROWSERS_PATH="$ROOT/00_sandbox/browsers" \
  ./.venv/bin/python -m playwright install chromium

echo "== 5. smoke test — a real job through every tool, not just an import =="
PLAYWRIGHT_BROWSERS_PATH="$ROOT/00_sandbox/browsers" ./.venv/bin/python 00_sandbox/smoke.py

echo
echo "Sandbox ready."
echo "  Next:    sh scripts/verify-all.sh    (once it exists)"
echo "  Optional, for Pages / Keynote / Figma:   open 00_sandbox/install-fonts.command"
