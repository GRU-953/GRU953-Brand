#!/bin/sh
# GRU953 — remove the fonts installed by install-fonts.command.
#
# Double-click this file in Finder. Removes ~/Library/Fonts/GRU953/ and
# nothing else — no other font on your Mac is touched.
set -e
DEST="$HOME/Library/Fonts/GRU953"
if [ ! -d "$DEST" ]; then
  echo "Nothing installed at $DEST — nothing to remove."
  exit 0
fi
COUNT=$(find "$DEST" -type f | wc -l | tr -d ' ')
rm -rf "$DEST"
echo "Removed $DEST ($COUNT file(s))."
