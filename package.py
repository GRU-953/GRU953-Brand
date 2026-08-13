#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""Package the GRU953 plugin, the three standalone skills and the design system.

Nothing is packaged until everything it depends on has been proved:

    1. the tokens in all three trees match the brand kit          (sync-tokens.py --check)
    2. every card on disk matches its source                      (build.py --check)
    3. both delivery trees pass the brand review with no blockers (check.py)
    4. every .skill archive has SKILL.md at its ROOT, and frontmatter that uses only the
       six fields the Agent Skills specification defines
    5. plugin.json passes the installer's own limits, including the 500-character cap on
       `description` — which is NOT in the published reference, and which this build
       learned about from a failed install

A packaging step that runs before its checks is a packaging step that ships a failure,
so the order here is the point.

    python3 package.py            # check, then build 09_delivery/
    python3 package.py --check    # run the checks only
"""
from __future__ import annotations
import argparse
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "delivery"
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
problems: list[str] = []


def run(cmd: list[str], cwd: pathlib.Path, label: str) -> str:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        problems.append(f"{label} failed:\n      "
                        + "\n      ".join((r.stdout + r.stderr).strip().splitlines()[-6:]))
    return r.stdout


# The installer rejects a plugin whose description is longer than this, with
# "Plugin description must be at most 500 characters."
#
# HOW THIS NUMBER GOT HERE, stated plainly: not from the documentation. The plugins
# reference describes the field only as "Brief plugin description" and gives no limit, so
# a build that read the reference carefully still shipped a 641-character description and
# failed at install. The figure comes from the installer's own error message. If it ever
# changes, this constant is where to change it — and the check below is why the next
# person finds out at package time instead.
PLUGIN_DESCRIPTION_MAX = 500


def check_manifest() -> None:
    import json as _json
    f = HERE / "plugin/gru953/.claude-plugin/plugin.json"
    try:
        m = _json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        problems.append(f"{f} could not be read as JSON: {e}")
        return
    if "name" not in m:
        problems.append(f"{f}: `name` is the one required field and it is missing")
    elif not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(m["name"])):
        problems.append(f"{f}: `name` must be kebab-case; claude.ai rejects other forms")
    d = m.get("description", "")
    if len(d) > PLUGIN_DESCRIPTION_MAX:
        problems.append(f"{f}: `description` is {len(d)} characters; the installer "
                        f"refuses more than {PLUGIN_DESCRIPTION_MAX} "
                        f"(\"Plugin description must be at most 500 characters.\")")
    if not d:
        problems.append(f"{f}: `description` is empty; it is what the picker shows")


def check_frontmatter() -> None:
    """The six-field rule, measured rather than assumed.

    Claude Code accepts extra fields; claude.ai uploads, the Skills API and
    `package_skill.py` reject them with "Unexpected key(s) in SKILL.md frontmatter".
    A skill that loads in one place and not the other is not a portable skill.
    """
    for d in sorted((HERE / "plugin" / "gru953" / "skills").iterdir()):
        f = d / "SKILL.md"
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            problems.append(f"{f} has no frontmatter")
            continue
        fm = text.split("---\n", 2)[1]
        keys = set(re.findall(r"^([a-z][\w-]*):", fm, re.M))
        extra = keys - SPEC_FIELDS
        if extra:
            problems.append(f"{f}: frontmatter keys outside the spec: {sorted(extra)}")
        name = re.search(r"^name:\s*(\S+)", fm, re.M)
        if not name or name.group(1) != d.name:
            problems.append(f"{f}: `name` must equal the directory name ({d.name})")
        elif not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name.group(1)) or len(name.group(1)) > 64:
            problems.append(f"{f}: `name` is not a valid Agent Skills name")
        desc = re.search(r"description: >\n((?:  .*\n)+)", fm)
        if not desc:
            problems.append(f"{f}: no `description`")
        else:
            flat = " ".join(x.strip() for x in desc.group(1).splitlines())
            if len(flat) > 1024:
                problems.append(f"{f}: description is {len(flat)} characters; the "
                                f"specification caps it at 1024")


def zip_dir(src: pathlib.Path, target: pathlib.Path, root_is_src: bool) -> None:
    """A deterministic archive: sorted, and with a fixed timestamp.

    Two runs over the same files must produce the same bytes, or nobody can tell a
    rebuild from a change.
    """
    if target.exists():
        target.unlink()
    files = sorted(f for f in src.rglob("*")
                   if f.is_file() and "__pycache__" not in f.parts
                   and f.suffix != ".pyc" and "node_modules" not in f.parts)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            arc = f.relative_to(src if root_is_src else src.parent).as_posix()
            info = zipfile.ZipInfo(arc, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (f.stat().st_mode & 0o7777) << 16
            z.writestr(info, f.read_bytes())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="run the checks only")
    a = ap.parse_args()

    print("Checking, before anything is packaged.\n")
    run([sys.executable, "sync-tokens.py", "--check"], HERE, "the token sync")
    run([sys.executable, "build.py", "--check"], HERE / "design-system", "the card build")
    checker = HERE / "plugin/gru953/skills/gru953-review/scripts/check.py"
    for tree in ("plugin", "design-system"):
        out = run([sys.executable, str(checker), tree, "--quiet"], HERE,
                  f"the brand review of {tree}")
        if out.strip():
            problems.append(f"the brand review of {tree} reported findings:\n      "
                            + "\n      ".join(out.strip().splitlines()[:8]))
    check_manifest()
    check_frontmatter()

    if problems:
        print("NOT PACKAGED — these must be fixed first:")
        for p in problems:
            print(f"  ✗ {p}")
        return 1
    print("  ✓ tokens in step across all three trees")
    print("  ✓ every card matches its source")
    print("  ✓ both trees pass the brand review with no findings")
    print("  ✓ every SKILL.md uses only the six specification fields")
    import json as _json
    _d = _json.loads((HERE / "plugin/gru953/.claude-plugin/plugin.json").read_text())["description"]
    print(f"  ✓ plugin.json is within the installer's limits "
          f"(description {len(_d)}/{PLUGIN_DESCRIPTION_MAX} characters)")
    if a.check:
        return 0

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "skills").mkdir()

    zip_dir(HERE / "plugin" / "gru953", OUT / "gru953-plugin.zip", root_is_src=False)
    zip_dir(HERE / "design-system", OUT / "gru953-design-system.zip", root_is_src=False)
    for d in sorted((HERE / "plugin" / "gru953" / "skills").iterdir()):
        if (d / "SKILL.md").exists():
            zip_dir(d, OUT / "skills" / f"{d.name}.skill", root_is_src=True)

    # every archive is opened again and checked, because a zip that cannot be read is a
    # zip nobody finds out about until they try to install it
    print("\nPackaged:")
    for f in sorted(OUT.rglob("*")):
        if f.suffix not in (".zip", ".skill"):
            continue
        with zipfile.ZipFile(f) as z:
            bad = z.testzip()
            names = z.namelist()
        if bad:
            problems.append(f"{f.name} is corrupt at {bad}")
        if f.suffix == ".skill" and "SKILL.md" not in names:
            problems.append(f"{f.name} has no SKILL.md at its root")
        sha = hashlib.sha256(f.read_bytes()).hexdigest()[:12]
        print(f"  {f.relative_to(OUT).as_posix():40s} {f.stat().st_size/1024:8.0f} kB  "
              f"{len(names):3d} files  sha256:{sha}")
    if problems:
        print("\nBROKEN:")
        for p in problems:
            print(f"  ✗ {p}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
