#!/usr/bin/env python3
"""Compare a Verus file against its original and flag common proof shortcuts."""
import difflib
import re
import sys

ADDED_PATTERNS = [
    (r"\bassume\s*\(", "assume(...)"),
    (r"\badmit\s*\(", "admit(...)"),
    (r"external_body", "external_body"),
    (r"verifier::external\b|\bexternal\b", "external"),
    (r"\baxiom\b", "axiom"),
    (r"verifier::\w+", "verifier attribute"),
]
SPEC_KEYWORDS = re.compile(r"\b(requires|ensures|decreases|invariant|recommends)\b")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: cheat_check.py ORIGINAL.rs MODIFIED.rs")
    old, new = read(sys.argv[1]), read(sys.argv[2])
    findings = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new).get_opcodes():
        if tag == "equal":
            continue
        for k in range(j1, j2):
            line = new[k].split("//")[0]
            for pat, name in ADDED_PATTERNS:
                if re.search(pat, line):
                    findings.append(f"added {name} at line {k + 1}: {new[k].strip()}")
        for k in range(i1, i2):
            text = old[k].strip()
            if not text or text.startswith("//"):
                continue
            kind = "spec" if SPEC_KEYWORDS.search(text) else "code"
            findings.append(f"original {kind} line {k + 1} removed/changed: {text}")
    if findings:
        print("Possible cheating or unintended changes:")
        for f in findings:
            print(" -", f)
        sys.exit(1)
    print("No suspicious changes found (text-based check; still review the diff).")


if __name__ == "__main__":
    main()
