"""Check every skills/*/SKILL.md has valid frontmatter matching its directory name."""
import re
import sys
from pathlib import Path

errors = []
skills = sorted(Path(__file__).parent.parent.glob("skills/*/SKILL.md"))
if not skills:
    errors.append("no skills found under skills/")
for p in skills:
    m = re.match(r"---\n(.*?)\n---\n", p.read_text(), re.S)
    if not m:
        errors.append(f"{p}: missing frontmatter")
        continue
    fm = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M))
    if fm.get("name") != p.parent.name:
        errors.append(f"{p}: name {fm.get('name')!r} != directory {p.parent.name!r}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fm.get("name", "")):
        errors.append(f"{p}: name must be lowercase-hyphenated")
    if len(fm.get("description", "")) < 50:
        errors.append(f"{p}: description missing or too short")
    if len(p.read_text().splitlines()) > 500:
        errors.append(f"{p}: over 500 lines")
for e in errors:
    print("ERROR", e)
sys.exit(1 if errors else 0)
