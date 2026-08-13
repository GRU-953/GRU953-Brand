#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""Package the kit, and write the verification report that ships beside it.

WHY THIS FILE EXISTS
--------------------
`09_delivery/` used to be assembled by hand. It went stale: the zip and the verification
report both still described a build with three separate bird drawings, a colour that had
been replaced, and a check count from a different day. Nobody noticed because the stale-
reference scan in `verify.py` skipped this folder — the one folder whose whole job is to
carry a snapshot of everything else.

So: the folder is emptied and rebuilt from the current tree, every time, by this script. And
the scan no longer skips it.

The zip does NOT contain the guidebook HTML or PDF. The guidebook already embeds every
other file in the kit individually, so putting it inside an archive of those same files
would carry a third copy of everything for no benefit.

Run:  python3 09_delivery/package.py
"""
import hashlib, os, pathlib, subprocess, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "09_delivery"
ZIP = OUT / "GRU953-Brand-Kit.zip"
REPORT = OUT / "VERIFICATION.txt"

# Not shipped: build caches, the node install, the exploration font library, and the
# guidebook itself (which embeds this zip).
SKIP_DIRS = {"node_modules", "__pycache__", ".git", "09_delivery", "candidates"}
SKIP_NAMES = {".DS_Store"}
SKIP_SUFFIX_IN_GUIDEBOOK = {".html", ".pdf"}


def wanted(p: pathlib.Path) -> bool:
    rel = p.relative_to(ROOT)
    if any(part in SKIP_DIRS for part in rel.parts) or p.name in SKIP_NAMES:
        return False
    if p.name.startswith("."):
        return False
    # the guidebook cannot be inside a zip that the guidebook embeds
    if rel.parts[0] == "08_guidebook" and p.suffix.lower() in SKIP_SUFFIX_IN_GUIDEBOOK:
        return False
    return True


def build_zip():
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(filenames):
            p = pathlib.Path(dirpath) / fn
            if p.is_file() and wanted(p):
                files.append(p)
    staging = OUT / "GRU953-Brand-Kit.zip.building"
    with zipfile.ZipFile(staging, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in files:
            # A fixed timestamp, so the same tree always produces the same bytes. Without it
            # the zip's hash changes on every run and "did anything actually change?" becomes
            # unanswerable.
            info = zipfile.ZipInfo(str(pathlib.Path("GRU953_Branding") / p.relative_to(ROOT)),
                                   date_time=(2026, 8, 13, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, p.read_bytes())
    if ZIP.exists():
        ZIP.unlink()
    staging.rename(ZIP)
    return files


def main():
    # clear out anything left from an earlier build, so nothing stale can survive
    for old in sorted(OUT.iterdir()):
        if old.name != "package.py":
            if old.is_dir():
                import shutil
                shutil.rmtree(old)
            else:
                old.unlink()

    files = build_zip()
    total = sum(p.stat().st_size for p in files)
    sha = hashlib.sha256(ZIP.read_bytes()).hexdigest()

    # The report is the verifier's OWN output, captured, not a summary written by hand.
    r = subprocess.run([sys.executable, str(ROOT / "00_sandbox/verify.py")],
                       capture_output=True, text=True, cwd=ROOT)
    passed = r.returncode == 0

    REPORT.write_text(
        "GRU953 BRAND KIT — VERIFICATION REPORT\n"
        "সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.\n"
        "Copyright 2026 Aninda Sundar Howlader (GRU953)\n"
        f"{'=' * 78}\n\n"
        f"Packaged     13 August 2026\n"
        f"Archive      {ZIP.name}\n"
        f"             {ZIP.stat().st_size:,} bytes\n"
        f"             SHA-256 {sha}\n"
        f"Contents     {len(files):,} files, {total:,} bytes uncompressed\n"
        f"Excluded     the guidebook HTML and PDF \u2014 the guidebook already embeds every\n"
        f"             other file in the kit individually, so archiving it alongside them\n"
        f"             would carry a third copy of everything. Also excluded: the node\n"
        f"             install and the build caches.\n\n"
        "This report is the verifier's own output, captured by 09_delivery/package.py.\n"
        "It is not a summary written by hand, and it is regenerated every time the kit is\n"
        "packaged — so it cannot describe a build that no longer exists.\n\n"
        f"{'=' * 78}\n\n" + r.stdout + ("\n" + r.stderr if r.stderr.strip() else ""),
        encoding="utf-8")

    print(f"{ZIP.name}   {ZIP.stat().st_size / 1048576:.1f} MB   {len(files):,} files")
    print(f"VERIFICATION.txt written — verifier {'PASSED' if passed else 'FAILED'}")
    if not passed:
        sys.exit("FAIL — the kit does not pass its own checks. Not shipping this.")
    print("\nRebuild the guidebook afterwards if any source file changed:")
    print("  python3 08_guidebook/build.py && python3 08_guidebook/build.py --print")


if __name__ == "__main__":
    main()
