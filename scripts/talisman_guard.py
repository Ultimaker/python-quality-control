#!/usr/bin/env python3
"""Talisman pre-commit guard + `.talismanrc` maintenance helper.

Two problems this solves:

1. When Talisman blocks a commit, the raw output is terse and it is easy (for a
   human or an AI agent) to "fix" it the wrong way — by hand-appending a
   `fileignoreconfig` entry. Talisman honours the FIRST entry for a filename, so
   a second entry with a fresh checksum is silently ignored and the commit keeps
   failing (this exact trap cost two failed commits in issue #129).

2. Editing an already-whitelisted file changes its checksum, so the old entry
   goes stale and must be *replaced*, not duplicated.

Usage
-----
    # run the scan (this is what the pre-commit hook calls)
    ci/scripts/talisman_guard.py check

    # whitelist a false-positive: add OR replace the checksum, never duplicate
    ci/scripts/talisman_guard.py allow .env.example scripts/comfy_host.py

    # collapse any pre-existing duplicate filename entries (keep the last)
    ci/scripts/talisman_guard.py dedupe

`allow` and `dedupe` are idempotent and preserve the comments in `.talismanrc`.

Set SKIP_PRE_COMMIT=1 to make `check` a no-op (matches the other repo hooks).
"""
import os
import re
import shutil
import subprocess
import sys

REPO_ROOT = os.environ.get("REPO_ROOT", os.getcwd())
TALISMANRC = os.path.join(REPO_ROOT, ".talismanrc")
SELF = "ci/scripts/talisman_guard.py"

ANSI = re.compile(r"\x1b\[[0-9;]*m")


# --------------------------------------------------------------------- talisman
def _talisman_bin():
    """Locate the talisman binary (PATH, $TALISMAN_HOME, ~/.talisman)."""
    for cand in (
        os.environ.get("TALISMAN_BIN"),
        shutil.which("talisman"),
        os.path.expanduser("~/.talisman/bin/talisman_linux_amd64"),
        os.path.expanduser("~/.talisman/bin/talisman"),
    ):
        if cand and os.path.exists(cand):
            return cand
    return None


def _require_talisman():
    binp = _talisman_bin()
    if not binp:
        sys.stderr.write(
            "talisman_guard: could not find the talisman binary.\n"
            "  Install it (https://github.com/thoughtworks/talisman) or set "
            "TALISMAN_BIN=/path/to/talisman.\n"
        )
        sys.exit(2)
    return binp


def _checksums_for(files):
    """Ask talisman for the canonical checksum of each file. Returns an ordered
    list of (filename, checksum). Talisman is the source of truth here so we
    never guess the hashing scheme."""
    binp = _require_talisman()
    out = subprocess.run(
        [binp, f"--checksum={' '.join(files)}"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    ).stdout
    pairs, fname = [], None
    for line in ANSI.sub("", out).splitlines():
        m = re.match(r"- filename:\s*(.+?)\s*$", line)
        if m:
            fname = m.group(1)
            continue
        m = re.match(r"\s*checksum:\s*([0-9a-f]+)\s*$", line)
        if m and fname is not None:
            pairs.append((fname, m.group(1)))
            fname = None
    return pairs


# ------------------------------------------------------------------ .talismanrc
def _read_rc():
    if not os.path.exists(TALISMANRC):
        return "fileignoreconfig:\nversion: \"\"\n"
    with open(TALISMANRC) as fh:
        return fh.read()


def _write_rc(text):
    if not text.endswith("\n"):
        text += "\n"
    with open(TALISMANRC, "w") as fh:
        fh.write(text)


def _parse_blocks(text):
    """Split `.talismanrc` into a list of segments, preserving order/comments.

    Each segment is either:
      ("plain", "<line>")                         — comments, version:, headers…
      ("block", filename, ["<line>", ...])        — a `- filename:` entry + body
    A block's body is the set of following space-indented lines.
    """
    lines = text.splitlines()
    segs, i = [], 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"- filename:\s*(.+?)\s*$", line)
        if m:
            body = [line]
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or lines[i].startswith("\t")):
                body.append(lines[i])
                i += 1
            segs.append(("block", m.group(1), body))
        else:
            segs.append(("plain", line))
            i += 1
    return segs


def _render(segs):
    out = []
    for seg in segs:
        if seg[0] == "plain":
            out.append(seg[1])
        else:
            out.extend(seg[2])
    return "\n".join(out) + "\n"


def _set_checksum(body, checksum):
    """Return a block body with its `checksum:` line set (replaced or inserted),
    dropping any `ignore_detectors` lines so the entry is a clean checksum entry."""
    head = body[0]
    new = [head, f"  checksum: {checksum}"]
    return new


def _checksum_in(body):
    """Extract the checksum from a block body, or None (e.g. ignore_detectors entry)."""
    for line in body[1:]:
        m = re.match(r"\s*checksum:\s*([0-9a-f]+)\s*$", line)
        if m:
            return m.group(1)
    return None


def allow(files):
    if not files:
        sys.stderr.write("talisman_guard allow: no files given\n")
        return 1
    # normalise to repo-relative paths
    rels = []
    for f in files:
        ap = os.path.abspath(f)
        rels.append(os.path.relpath(ap, REPO_ROOT) if ap.startswith(REPO_ROOT) else f)

    pairs = _checksums_for(rels)
    if not pairs:
        sys.stderr.write("talisman_guard allow: talisman returned no checksums "
                         "(do the files exist / are they tracked?)\n")
        return 1
    checksum_of = dict(pairs)

    segs = _parse_blocks(_read_rc())
    handled = set()
    changed = []

    # Pass 1: replace the checksum of the first existing block per filename,
    #         and mark any later duplicates of that filename for removal.
    new_segs = []
    for seg in segs:
        if seg[0] == "block" and seg[1] in checksum_of:
            fn = seg[1]
            if fn in handled:
                changed.append(f"  - dropped duplicate entry for {fn}")
                continue  # remove duplicate
            handled.add(fn)
            old = seg[2]
            new_body = _set_checksum(old, checksum_of[fn])
            if new_body != old:
                changed.append(f"  - updated checksum for {fn}")
            new_segs.append(("block", fn, new_body))
        else:
            new_segs.append(seg)

    # Pass 2: insert brand-new entries just before the `version:` line.
    missing = [(fn, cs) for fn, cs in pairs if fn not in handled]
    if missing:
        insert_at = next((idx for idx, s in enumerate(new_segs)
                          if s[0] == "plain" and s[1].startswith("version:")), len(new_segs))
        block_segs = []
        for fn, cs in missing:
            block_segs.append(("block", fn, [f"- filename: {fn}", f"  checksum: {cs}"]))
            changed.append(f"  - added entry for {fn}")
        new_segs = new_segs[:insert_at] + block_segs + new_segs[insert_at:]

    _write_rc(_render(new_segs))
    print(f"talisman_guard: updated {TALISMANRC}")
    print("\n".join(changed) if changed else "  (no changes needed)")
    print("\nNext: git add .talismanrc && re-run your commit.")
    return 0


def dedupe():
    """Collapse duplicate `- filename:` blocks. For each filename that appears
    more than once, keep the entry whose checksum matches the CURRENT file
    (asked from talisman); if none matches (file changed/removed, or the entry
    is an ignore_detectors entry), keep the last occurrence and warn."""
    segs = _parse_blocks(_read_rc())
    counts = {}
    for seg in segs:
        if seg[0] == "block":
            counts[seg[1]] = counts.get(seg[1], 0) + 1
    dups = {fn for fn, c in counts.items() if c > 1}
    if not dups:
        print("talisman_guard: no duplicate .talismanrc entries found")
        return 0

    existing = [fn for fn in dups if os.path.exists(os.path.join(REPO_ROOT, fn))]
    current = dict(_checksums_for(existing)) if existing else {}

    idxs = {}
    for i, seg in enumerate(segs):
        if seg[0] == "block" and seg[1] in dups:
            idxs.setdefault(seg[1], []).append(i)

    keep, warns = {}, []
    for fn, ilist in idxs.items():
        want = current.get(fn)
        chosen = None
        if want:
            chosen = next((i for i in ilist if _checksum_in(segs[i][2]) == want), None)
        if chosen is None:
            chosen = ilist[-1]
            if want:
                warns.append(f"  ! {fn}: no entry matched the current file — kept "
                             f"the last one; run `{SELF} allow {fn}` to refresh it")
        keep[fn] = chosen

    out, removed = [], []
    for i, seg in enumerate(segs):
        if seg[0] == "block" and seg[1] in dups and i != keep[seg[1]]:
            removed.append(seg[1])
            continue
        out.append(seg)
    _write_rc(_render(out))
    print(f"talisman_guard: removed {len(removed)} duplicate entr"
          f"{'y' if len(removed) == 1 else 'ies'}: {', '.join(sorted(set(removed)))}")
    for w in warns:
        print(w)
    return 0


# -------------------------------------------------------------------- the hook
FAIL_HELP = """\
──────────────────────────────────────────────────────────────────────────────
Talisman blocked this commit — a staged change looks like a secret.

If it IS a real secret (API key, password, private key, token):
  → DO NOT whitelist it. Remove it from the diff, rotate it if it was ever
    pushed, and keep secrets in the gitignored .env.

If it is a FALSE POSITIVE (a placeholder/example value, a hex colour, an LFS
pointer oid, an env-var *name*), whitelist it the safe way — DO NOT hand-edit
.talismanrc (that creates duplicate stale entries; talisman honours only the
first, so the commit keeps failing):

    python3 {self} allow <file> [<file> ...]
    git add .talismanrc
    # then re-run your commit

`allow` adds a new entry OR replaces the existing (now-stale) checksum in place,
and removes duplicates — it is safe to run repeatedly.
──────────────────────────────────────────────────────────────────────────────
""".format(self=SELF)


def check():
    if os.environ.get("SKIP_PRE_COMMIT") == "1":
        return 0
    binp = _require_talisman()
    proc = subprocess.run([binp, "--githook", "pre-commit"], cwd=REPO_ROOT)
    if proc.returncode != 0:
        sys.stderr.write(FAIL_HELP)
    return proc.returncode


def main(argv):
    cmd = argv[0] if argv else "check"
    if cmd == "check":
        return check()
    if cmd == "allow":
        return allow(argv[1:])
    if cmd == "dedupe":
        return dedupe()
    sys.stderr.write(f"usage: {SELF} [check|allow <files...>|dedupe]\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
