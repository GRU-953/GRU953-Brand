#!/bin/sh
# GRU953 — install the brand's own typefaces for your own use.
#
# Double-click this file in Finder. No terminal needed.
#
# Copies the five shipping families into ~/Library/Fonts/GRU953/ — USER LEVEL
# ONLY, so no administrator password and nothing system-wide changes. This is
# entirely optional: it exists so you can use Sora, Noto Sans, Noto Sans
# Bengali, Anek Bangla and JetBrains Mono in Pages, Keynote or Figma. The build
# itself never depends on this having been run — every generator loads these
# same files by their repo-relative path, never by asking macOS for a font by
# name.
set -e
cd "$(dirname "$0")/.."
SRC="brand-kit/05_type/source-fonts"
DEST="$HOME/Library/Fonts/GRU953"

if [ -d "$DEST" ] && [ "$1" != "--force" ]; then
  echo "Already installed at $DEST."
  echo "Run with --force to overwrite, or run 00_sandbox/uninstall-fonts.command first."
  exit 0
fi

mkdir -p "$DEST"
COUNT=0
for family_dir in "$SRC"/*/; do
  family=$(basename "$family_dir")
  for f in "$family_dir"*.ttf; do
    [ -e "$f" ] || continue
    cp "$f" "$DEST/"
    echo "  copied  $(basename "$f")"
    COUNT=$((COUNT + 1))
  done
  cp "$family_dir/OFL.txt" "$DEST/OFL-$family.txt" 2>/dev/null || true
done

echo
echo "$COUNT font file(s) installed to $DEST"
echo
echo "Licence: every one of these is SIL Open Font Licence 1.1. The licence text"
echo "travelled with each family as OFL-<name>.txt beside it. OFL 1.1 permits"
echo "using, copying and embedding these fonts freely, including commercially;"
echo "the one thing it restricts is redistributing a MODIFIED copy under the"
echo "same family name if that name is Reserved."
echo
echo "To remove everything this installed:"
echo "  sh 00_sandbox/uninstall-fonts.command"
echo
echo "You may need to log out and back in, or restart the app you want to use"
echo "them in, before macOS's Font Book picks up the new files."
