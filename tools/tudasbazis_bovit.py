"""Tudásbázis-szócikkek hozzáadása kategóriánként, betűrendben. Használat: kb.py <json>"""
import json
import pathlib
import re
import sys

KB = pathlib.Path("kutatas/tudasbazis.md")
CATS = ["Rövidítések", "Folyamatfogalmak", "Mérési módszerek", "Mutatók"]

def fmt(e):
    fields = [("Mit jelent", e["mit"])]
    for k, lab in [("hol", "Hol fordul elő"), ("olvas", "Hogyan olvasd"), ("felre", "Tipikus félreolvasás"), ("lasd", "Lásd")]:
        if e.get(k): fields.append((lab, e[k]))
    lines = [f"**{lab}:** {txt}" for lab, txt in fields]
    return f"### {e['cim']}\n" + "\\\n".join(lines) + "\n"

text = KB.read_text()
head, rest = text.split("\n## Rövidítések\n", 1)
body = "## Rövidítések\n" + rest
sections = {}
parts = re.split(r"^## (.+)$", body, flags=re.MULTILINE)
for i in range(1, len(parts), 2):
    name, content = parts[i].strip(), parts[i + 1]
    entries = re.split(r"(?=^### )", content, flags=re.MULTILINE)
    sections[name] = {re.match(r"### (.+)", x).group(1).strip(): x.strip() + "\n" for x in entries if x.startswith("### ")}
for e in json.loads(pathlib.Path(sys.argv[1]).read_text()):
    sections[e["kat"]][e["cim"]] = fmt(e)
out = [head.rstrip() + "\n"]
for c in CATS:
    out.append(f"\n## {c}\n")
    items = sections.get(c, {})
    if not items:
        out.append("\n*(A kutatással együtt bővül.)*\n")
    for k in sorted(items, key=lambda s: s.lower()):
        out.append("\n" + items[k])
KB.write_text("".join(out))
print(sum(len(v) for v in sections.values()), "szócikk")
