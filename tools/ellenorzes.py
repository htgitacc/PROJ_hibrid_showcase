"""A dokumentumok gyors ellenőrzése: F-nn források, tudásbázis-horgonyok, belső linkek.

Futtatás a repó gyökeréből: python3 tools/ellenorzes.py
Átnézi a kutatas/ és a koncepcio/ összes .md fájlját.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(".")
K = ROOT / "kutatas"
docs = sorted(list(K.glob("*.md")) + list((ROOT / "koncepcio").rglob("*.md")))
forrasok = (K / "forrasok.md").read_text()
tb = (K / "tudasbazis.md").read_text()


def anchor(h: str) -> str:
    return re.sub(r"[^\w -]", "", h.lower()).replace(" ", "-")


anchors = {anchor(h) for h in re.findall(r"^### (.+)$", tb, re.MULTILINE)}
listed = set(re.findall(r"^### (F-\d\d)", forrasok, re.MULTILINE))
used: set[str] = set()
hibak = []
figyelm = []
for p in docs:
    text = p.read_text()
    if p.name != "forrasok.md":
        used |= set(re.findall(r"F-\d\d", text))
    for target, frag in re.findall(r"\]\(([^)#\s]*)(?:#([\w-]+))?\)", text):
        if target.startswith(("http://", "https://")):
            continue
        dest = (p.parent / target).resolve() if target else p.resolve()
        if target and not dest.exists():
            figyelm.append(f"{p}: még nem létező fájl: {target}")
            continue
        if frag and dest.name == "tudasbazis.md" and frag not in anchors | {"kifejezes"}:
            hibak.append(f"{p}: törött tudásbázis-horgony: #{frag}")
if used - listed:
    hibak.append(f"hiányzó forrás: {sorted(used - listed)}")
if listed - used:
    hibak.append(f"nem hivatkozott forrás: {sorted(listed - used)}")
print("\n".join(hibak) or "rendben")
if figyelm:
    print("figyelmeztetés (a fázis zárásáig el kell tűnnie):\n  " + "\n  ".join(figyelm))
print(f"{len(docs)} dokumentum, {len(listed)} forrás, {len(anchors)} szócikk")
sys.exit(1 if hibak else 0)
