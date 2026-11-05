# Kapudöntés — [G0 / G1 / G2] [projekt neve]

> **Használat.** Minden kapunál egy lap. A PM készíti elő a kapu előtt, a döntéshozó a kapun
> tölti ki a döntést és az indoklást, majd aláírja. A lap akkor jó, ha egy kívülálló fél év múlva
> is megérti belőle, **mi alapján** született a döntés — nem csak azt, hogy mi lett.
>
> A kapuk szabályai: [kapuk és kill criteria](../01-kapuk-es-kill-criteria.md). Kitöltött
> példák: a [Xyo-példa](../04-xyo-pelda.md) 4.3. (G0), 4.5. (G1) és 4.6. (G2) pontja.

---

**Kapu:** [G0 — Indulhat-e a kísérleti szakasz? / G1 — PoC-kapu / G2 — élesítési kapu: [hullám]]\
**Dátum:** [éééé.hh.nn.]\
**Döntéshozó:** [név, szerep]\
**Előterjesztő:** [név, szerep]\
**Jelen vannak:** [nevek]\
**Ez a kapu hányadik alkalommal ülésezik:** [1. / 2. (hiánypótlás után) / G1' (pivot után)]

## 1. Bemenetek

| Bemenet | Verzió / dátum | Hol érhető el |
|---|---|---|
| [pl. mérési jelentés] | [golden set v1.0, 2027.02.26.] | [link] |
| [...] | | |

## 2. Feltételek

| # | Feltétel | Teljesült? | Bizonyíték | Megjegyzés |
|---|---|---|---|---|
| [G0-1] | [a feltétel szövege a kapuk dokumentumból] | [igen / nem] | [dokumentum, dátum] | |
| [...] | | | | |

## 3. Mutatók (G1, G2)

| Mutató | Típus | Küszöb (zöld) | Eredmény | Sáv |
|---|---|---|---|---|
| [MK-nn név] | [kizáró / kritikus / támogató] | [érték] | [érték] | [zöld / sárga / piros] |
| [...] | | | | |

**Esetszintű megjegyzések:** [mely esetek hibásak, mi az okuk — a mérési jelentés alapján]

## 4. Döntés

**A döntés:** [a kapu lehetséges kimenetei közül egy — G0: go / hiánypótlás / leállítás · G1: go /
pivot / no-go · G2: élesítés / halasztás]

**Indoklás:** [melyik szabály szerint — hivatkozással a kapuk dokumentumra; ha kill criterion
teljesült, melyik]

**Feltételek a következő szakaszra:** [pl. pivot: hipotézis, határidő, keret, és mi történik, ha nem
sikerül]

**Felszabaduló keret:** [összeg és megnevezés, vagy „nincs”]

**Nyitott kérdések:** [ami nem dőlt el, felelőssel és határidővel]

**Aláírás:** [döntéshozó neve, dátum]

---

## Kitöltési útmutató

| Mező | Mit írj bele | Példa (Xyo, G1) | Tipikus hiba |
|---|---|---|---|
| Hányadik alkalom | ha a kapu hiánypótlás vagy pivot után újra ülésezik, külön lap | G1' (pivot után), 2027.03.19. | felülírni az első lapot — elvész, miért kellett pivot |
| Bemenetek | minden dokumentum **verzióval** | mérési jelentés, golden set v1.0; költségbecslés 2027.03.01. | verzió nélkül — nem rekonstruálható, mi alapján döntöttek |
| Feltételek | a kapuk dokumentum feltételei szó szerint, egyenként | G0-4: DPIA-döntés — 1. G0-n **nem**, 2. G0-n igen | „lényegében teljesült” — igen vagy nem |
| Mutatók | a mérőszámkártyák küszöbei, változtatás nélkül | context recall 0,84, zöld ≥ 0,85 → sárga | a sávot a kapun átírni |
| Esetszintű megjegyzések | a hibás esetek oka | a 3 recall-hiba a Beszerzés tár szkennelt PDF-jei | csak az átlagot közölni |
| Döntés | a lehetséges kimenetek egyike | pivot | „feltételes go” — ilyen kimenet nincs; ez pivot vagy hiánypótlás |
| Indoklás | a szabály, amely alapján | egy kritikus mutató sárga, a hibahely azonosított → pivot (1.3.) | a demó benyomására hivatkozni |
| Feltételek a következő szakaszra | pivotnál: hipotézis, határidő, keret, és a no-go feltétele | OCR a 112 PDF-re, 2 hét, kb. 850 000 Ft a tartalékból; ha a recall nem zöld → no-go | a no-go feltételét nem kimondani — akkor a pivot végtelen lesz |
| Felszabaduló keret | szakaszos finanszírozás | G1': a bevezetési keret 9,8 M Ft és a futási keret | a teljes keretet a G0-n felszabadítani |
| Nyitott kérdések | felelős + határidő | a golden set elutasítandó csoportjának bővítése 20 elemre — Kiss Réka, a zárásig | nyitott kérdést döntésként rögzíteni |
