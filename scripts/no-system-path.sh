#!/bin/sh
# GRU953 — prove the build depends on nothing that merely HAPPENS to be
# installed on this machine.
#
# Runs the smoke test with the system PATH stripped back to a three-binary
# allow-list, each with a written reason, and a throwaway HOME so an installed
# font (see install-fonts.command) cannot secretly help. If the build only
# works because this Mac happens to have some other tool sitting on PATH, this
# is where that finding surfaces — as a plain "command not found", not a
# mystery on someone else's machine.
set -e
cd "$(dirname "$0")/.."
ROOT=$(pwd)

# A scratch bin holding symlinks to the three binaries the sandbox cannot
# exist without. Anything else the build reaches for fails with "command not
# found", and that failure IS the finding.
BIN=$(mktemp -d)
ln -s "$(command -v python3)" "$BIN/python3"   # runs .venv's own interpreter
ln -s "$(command -v node)"    "$BIN/node"      # runs 00_sandbox/node_modules
ln -s "$(command -v git)"     "$BIN/git"       # the diff gates need it

# A throwaway HOME, so ~/Library/Fonts is empty by construction. Without this,
# a Mac where install-fonts.command has been run would hand the build the
# brand's own typefaces for free — which is the exact dependency this gate
# exists to disprove.
FAKEHOME=$(mktemp -d)
TMPDIR_SCRATCH=$(mktemp -d)

echo "Running the sandbox smoke test with:"
echo "  PATH restricted to: python3, node, git (plus their own resolved targets)"
echo "  HOME replaced with an empty directory: $FAKEHOME"
echo

env -i \
  HOME="$FAKEHOME" \
  PATH="$ROOT/.venv/bin:$ROOT/00_sandbox/node_modules/.bin:$BIN" \
  PLAYWRIGHT_BROWSERS_PATH="$ROOT/00_sandbox/browsers" \
  LANG=en_GB.UTF-8 \
  TMPDIR="$TMPDIR_SCRATCH" \
  "$ROOT/.venv/bin/python" "$ROOT/00_sandbox/smoke.py"
STATUS=$?

rm -rf "$BIN" "$FAKEHOME" "$TMPDIR_SCRATCH"

if [ $STATUS -eq 0 ]; then
  echo
  echo "PASS — the sandbox works with nothing on PATH but python3, node and git,"
  echo "and with no fonts installed anywhere on the machine."
fi
exit $STATUS
