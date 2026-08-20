#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Aninda Sundar Howlader (GRU953)
"""Fetch the 28 typography candidates from Google's own font repository.

Every family in candidates_registry.json is SIL OFL 1.1, sourced from
github.com/google/fonts -- the primary distribution point Google itself
publishes these files from, not a mirror or a scrape. Each file's OFL.txt is
fetched alongside it, because the one condition OFL 1.1 actually asks is that
the licence travels with the font.

Every download is verified three ways before being trusted: the HTTP status
was 200, the bytes actually parse as a font (fontTools opens it and finds a
name table), and a SHA-256 is recorded so a future re-fetch can prove whether
upstream changed. A candidate that fails any of these is reported as not
fetched -- never silently dropped from the count.

Run:  python3 brand-kit/05_type/fetch_candidates.py
"""
import hashlib
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REGISTRY_PATH = HERE / "candidates_registry.json"
CANDIDATES_DIR = HERE / "candidates"
MANIFEST_PATH = HERE / "candidates_manifest.json"
BASE_URL = "https://raw.githubusercontent.com/google/fonts/main"


def curl_to_file(url: str, dest: pathlib.Path) -> tuple:
    """Download via curl (the system's own TLS trust store, not Python's --
    which on this Mac cannot verify GitHub's certificate at all). Returns
    (http_status, byte_count)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    # --globoff: curl's URL-globbing treats a literal [wght] in a variable-font
    # filename as a glob pattern (its brace/bracket range syntax), not literal
    # characters, and fails the request outright with no HTTP attempt at all --
    # which is why the first run here fetched every -Regular.ttf file fine and
    # failed every [axis] one with an empty status and zero bytes.
    result = subprocess.run(
        ["curl", "-s", "-g", "--globoff", "-w", "%{http_code}", "-o", str(dest), url],
        capture_output=True, text=True, timeout=60,
    )
    status = result.stdout.strip()
    size = dest.stat().st_size if dest.exists() else 0
    return status, size


def verify_is_font(path: pathlib.Path) -> bool:
    try:
        from fontTools.ttLib import TTFont
        f = TTFont(str(path), lazy=True)
        return "name" in f
    except Exception:
        return False


def sha256_of(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main():
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    fetched, failed = [], []

    for category, families in registry["candidates"].items():
        for key, spec in families.items():
            fam_dir = CANDIDATES_DIR / key
            font_url = f"{BASE_URL}/ofl/{spec['repo_dir']}/{spec['file']}"
            ofl_url = f"{BASE_URL}/ofl/{spec['repo_dir']}/OFL.txt"
            font_dest = fam_dir / spec["file"].replace("[", "_").replace(",", "-").replace("]", "")
            ofl_dest = fam_dir / "OFL.txt"

            status, size = curl_to_file(font_url, font_dest)
            if status != "200" or size < 1000:
                failed.append({"key": key, "family": spec["family"],
                                "reason": f"http {status}, {size} bytes", "url": font_url})
                if font_dest.exists():
                    font_dest.unlink()
                continue
            if not verify_is_font(font_dest):
                failed.append({"key": key, "family": spec["family"],
                                "reason": "downloaded bytes do not parse as a font",
                                "url": font_url})
                font_dest.unlink()
                continue

            ofl_status, ofl_size = curl_to_file(ofl_url, ofl_dest)
            ofl_ok = ofl_status == "200" and ofl_size > 100

            fetched.append({
                "key": key, "category": category, "family": spec["family"],
                "incumbent": spec.get("incumbent", False),
                "note": spec.get("note", ""),
                "font_file": str(font_dest.relative_to(HERE)),
                "font_bytes": size, "font_sha256": sha256_of(font_dest),
                "ofl_fetched": ofl_ok,
                "source_url": font_url,
            })
            print(f"  fetched {spec['family']} ({size} bytes){'  [OFL missing!]' if not ofl_ok else ''}")

    manifest = {
        "$note": "Every candidate actually fetched and verified as a real font file, "
                 "with its SHA-256 recorded. Regenerate: "
                 "python3 brand-kit/05_type/fetch_candidates.py",
        "total_in_registry": sum(len(v) for v in registry["candidates"].values()),
        "fetched_count": len(fetched),
        "failed_count": len(failed),
        "fetched": fetched,
        "failed": failed,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                              encoding="utf-8")

    print(f"\n{len(fetched)} fetched, {len(failed)} failed, of "
          f"{manifest['total_in_registry']} in the registry.")
    if failed:
        print("FAILED:")
        for f in failed:
            print(f"  {f['family']}: {f['reason']}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
