# Sablonok — letölthető, üres minták

Minden olyan dokumentumhoz, amely egy másik projektben is újrahasznosítható, itt van egy
**üres minta kitöltési útmutatóval**. A kitöltött változatukat a [Xyo-példa](../04-xyo-pelda.md) és
a [mérési rendszer](../02-meresi-rendszer.md) mutatja.

Minden minta három részből áll:

1. **Használat** — mikor, melyik kapuhoz, ki tölti ki;
2. **a minta** — a kitöltendő mezők `[szögletes zárójelben]`;
3. **kitöltési útmutató** — mezőnként: mit írj bele · példa a Xyo-ból · tipikus hiba.

A szakszavak magyarázata: [tudasbazis.md](../../kutatas/tudasbazis.md).

## A minták

| Minta | Mire való | Mikor | Melyik kapuhoz | Ki tölti ki |
|---|---|---|---|---|
| [Mérőszámkártya](meroszamkartya.md) | egy mutató teljes leírása: mit mér, hogyan, mi a jó, mikor avatkozunk be | a keretben, a G1-küszöbök rögzítésekor; élesítés előtt az üzemeltetési mutatókra | G0 (G0-9), G1, G2 | a mutató gazdája, a PM koordinálja |
| [Célkártya](celkartya.md) | egy sikerkritérium: cél, mutató, baseline, célérték, határidő | az üzleti esetben | G0 (G0-1) | szponzor, PM |
| [Kapudöntés](kapudontes.md) | egy kapu döntési lapja: bemenetek, feltételek, eredmények, döntés, indoklás | minden kapunál | G0, G1, G2 | PM készíti elő, a döntéshozó írja alá |
| [Adatleltár](adatleltar.md) | a rendszerbe kerülő adatforrások, gazdáik, jogosultságaik és kizárási szabályaik | a keretben, a kísérleti szakasz előtt; minden új tár előtt | G0 (G0-5), G2 (G2-1) | PM az adatgazdákkal |
| [AI Act-besorolási lap](ai-act-besorolasi-lap.md) | a rendszer AI Act szerinti besorolásának és a GDPR-kérdéseknek az előkészítése | a keretben; minden célváltozásnál | G0 (G0-3, G0-4), változáskérés | DPO és jogász, a PM előkészíti |

A kitöltött változatok: [célkártyák](../xyo-mintak/celkartyak.md), [adatleltár](../xyo-mintak/adatleltar.md),
[AI Act-besorolási lap](../xyo-mintak/ai-act-besorolasi-lap.md), [kapudöntések](../xyo-mintak/kapudontesek.md);
a mérőszámkártyáké a [mérési rendszerben](../02-meresi-rendszer.md).

## Hogyan töltsd le

A GitHubon a fájl megnyitása után a **Raw** gomb mutatja a nyers Markdown-szöveget; ezt
mentheted (`Ctrl+S`), vagy bemásolhatod egy szerkesztőbe. A felület **Mintatár** oldalán minden
minta mellett letöltőgomb van, és egy zip az összessel.

## Hogyan használd jól

- **Ne töltsd ki mindet egyszerre.** A minták a kapukhoz tartoznak: a célkártya és az adatleltár a
  keret elején kell, a mérőszámkártyák a G0 előtt, a kapudöntés a kapunál.
- **Ami nem dönthető el, az nem kész.** Ha egy mezőbe csak azt tudod írni, hogy „majd kiderül”,
  az a mező a kapu nyitott kérdése — írd a kapudöntés „nyitott kérdések” sorába.
- **A küszöböket a mérés előtt rögzítsd.** A mérőszámkártya „Mi számít jónak” mezője a G0-n
  lezárul; a kapunál már nem módosítható ([kapuk](../01-kapuk-es-kill-criteria.md)).
