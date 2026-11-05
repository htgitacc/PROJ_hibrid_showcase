# Kitöltött kapudöntések — Xyo

> A [kapudöntés](../sablonok/kapudontes.md) minta kitöltve a Xyo-példa négy ülésére. Egy ülés egy
> lap: a hiánypótlás és a pivot utáni újraülés **külön lap**, hogy látszódjon, miért kellett.
> A forrás a [Xyo-példa](../04-xyo-pelda.md) 4.3. és 4.5. pontja; a feltételek és küszöbök a
> [kapuk dokumentumból](../01-kapuk-es-kill-criteria.md), a mutatók a
> [mérési rendszerből](../02-meresi-rendszer.md). A G1 döntését a `hibrid_app/kapu.py` is
> újraszámolta a példa mérései alapján (az első mérésre pivot, a pivot utánira go). Ami a forrásban
> nincs kimondva, **„nincs adat a példában”**. A szakszavak: [tudasbazis.md](../../kutatas/tudasbazis.md).

Közös adatok: **döntéshozó** Horváth Júlia (ügyvezető, az irányító bizottság elnöke) · **előterjesztő**
Tóth Gergő (projektmenedzser) · **jelen vannak** az irányító bizottság tagjai (a névsor nincs adat a
példában).

---

## 1. lap — G0, első ülés

**Kapu:** G0 — Indulhat-e a kísérleti szakasz?\
**Dátum:** 2026. december 18.\
**Ez a kapu hányadik alkalommal ülésezik:** 1.

### Bemenetek

| Bemenet | Verzió / dátum | Hol érhető el |
|---|---|---|
| Üzleti eset, célkártyák | C-01–C-03, 2026. december 18. | [célkártyák](celkartyak.md) |
| Adatleltár | 1.0 | [adatleltár](adatleltar.md) |
| AI Act-besorolási lap | 1.0 | [besorolási lap](ai-act-besorolasi-lap.md) |
| Baseline-mérés | T0, 2026. december 7–11. | [Xyo-példa](../04-xyo-pelda.md) 4.2. |

### Feltételek

| # | Feltétel | Teljesült? | Bizonyíték | Megjegyzés |
|---|---|---|---|---|
| G0-1 | Üzleti eset jóváhagyva, baseline terve | igen | aláírt üzleti eset | Kovács Anita |
| G0-2 | Cél és kizárások rögzítve | igen | projektalapító dokumentum | Horváth Júlia |
| G0-3 | AI Act-besorolás | igen | besorolási lap | dr. Fekete Zsolt + jogász |
| G0-4 | DPIA-döntés | **nem** | — | a Cloud Pilot projekttárában névvel ellátott nyers kérdőív-export van; a DPO addig nem ad állásfoglalást, amíg nem tisztázott, mi kerül a rendszerbe |
| G0-5–G0-10 | adatleltár, jogosultsági elv, szolgáltató, golden set gazdája, G1-küszöbök, PoC-keret | igen | a kapuk dokumentum szerinti bizonyítékok | tíz feltételből kilenc teljesül; a tételes bizonyíték-hivatkozások nincsenek a példában |

### Döntés

**A döntés:** **hiánypótlás**.\
**Indoklás:** a G0-4 nem teljesült, a többi kilenc igen; a kapuk dokumentum szerint a DPIA-kérdést az
adatkezelés előtt el kell dönteni. Leállítás nem indokolt, mert a hiány pótolható.\
**Feltételek a következő ülésre:** az adatleltár kiegészül egy kizárási szabállyal (a nyers
kérdőív-exportok kikerülnek, az összesítő riport bent marad, X-02), a DPO egyszerűsített DPIA-t készít.\
**Felszabaduló keret:** nincs. A kísérleti szakasz nem indulhat el.\
**Nyitott kérdések:** a DPIA és a kizárási szabály — dr. Fekete Zsolt és Tóth Gergő, a második G0-ig.\
**Következmény:** a hiánypótlás három hét csúszást okozott a tervezett indításhoz képest, de
megelőzött egy lehetséges adatvédelmi incidenst.\
**Aláírás:** Horváth Júlia, 2026. december 18.

---

## 2. lap — G0', második ülés (hiánypótlás után)

**Kapu:** G0 — Indulhat-e a kísérleti szakasz?\
**Dátum:** 2027. január 8.\
**Ez a kapu hányadik alkalommal ülésezik:** 2. (hiánypótlás után)

### Bemenetek

| Bemenet | Verzió / dátum | Hol érhető el |
|---|---|---|
| Adatleltár | 1.1 (X-02 felvéve, D-04 kizárva) | [adatleltár](adatleltar.md) |
| Egyszerűsített DPIA | dr. Fekete Zsolt, 2027. január 8. | a besorolási lap 5. pontja |
| AI Act-besorolási lap | 1.1 | [besorolási lap](ai-act-besorolasi-lap.md) |

### Feltételek

| # | Feltétel | Teljesült? | Bizonyíték | Megjegyzés |
|---|---|---|---|---|
| G0-1–G0-3, G0-5–G0-10 | az első lapon igen | igen | lásd az 1. lapot | az adatleltár G0-5 a 1.1-es változattal |
| G0-4 | DPIA-döntés | **igen** | DPO-állásfoglalás, egyszerűsített DPIA | a rendszer munkavállalói adatokat tartalmazó dokumentumokat dolgoz fel új technológiával |

### Döntés

**A döntés:** **go**.\
**Indoklás:** mind a tíz feltétel teljesült.\
**Feltételek a következő szakaszra:** a kísérleti szakasz 2027. január 11-én indul; a G1-küszöbök a mérés előtt
rögzítettek, nem módosíthatók.\
**Felszabaduló keret:** PoC-keret **6 500 000 Ft** (ebből tartalék 900 000 Ft). A bevezetési keret nem.\
**Nyitott kérdések:** nincs adat a példában.\
**Aláírás:** Horváth Júlia, 2027. január 8.

---

## 3. lap — G1, PoC-kapu

**Kapu:** G1 — PoC-kapu\
**Dátum:** 2027. március 3.\
**Ez a kapu hányadik alkalommal ülésezik:** 1.

### Bemenetek

| Bemenet | Verzió / dátum | Hol érhető el |
|---|---|---|
| Mérési jelentés esetszintű listával | a 3. iteráció, golden set v1.0 (40 elem) | [Xyo-példa](../04-xyo-pelda.md) 4.4. |
| Jogosultsági teszt | 12 eset | [mérési rendszer](../02-meresi-rendszer.md) MK-04 |
| Éves költségbecslés | 41 Ft × 77 280 kérdés ≈ 3,2 M Ft, a 3,6 M Ft-os futási kereten belül | 4.5. |
| Iterációs napló, kockázatnapló | a kísérleti szakasz végén | nincs adat a példában, hol |

### Mutatók

| Mutató | Típus | Küszöb (zöld) | Eredmény | Sáv |
|---|---|---|---|---|
| MK-04 Permission leakage | kizáró | 0 | 0/12 | zöld |
| MK-01 Faithfulness | kritikus | ≥ 0,90 | 0,92 | zöld |
| MK-02 Context recall | kritikus | ≥ 0,85 | 0,84 | **sárga** |
| MK-03 Correct refusal | kritikus | ≥ 90%, téves elutasítás ≤ 10% | 8/8; téves 2/24 (8,3%) | zöld |
| MK-05 Latency p95 | támogató | ≤ 8 s | 7,4 s | zöld |
| MK-06 Éves futási költség | támogató | a keretben (≤ 3,6 M Ft) | ≈ 3,2 M Ft | zöld |

**Esetszintű megjegyzések:** a 24 megválaszolható kérdésből 3-nál a keresés nem találja a választ.
Kiss Réka átnézése szerint mindhárom a Beszerzés tár szkennelt PDF-jeire vonatkozik, amelyeknek nincs
szövegrétegük.

### Döntés

**A döntés:** **pivot**.\
**Indoklás:** a kizáró mutató zöld, **egy** kritikus mutató sárga (a recall 0,84, épp a küszöb alatt),
és a hiba helye azonosított (1.3., döntési szabályok). Kill criterion nem teljesült. A küszöböt nem
lazítják („0,84 majdnem 0,85”), és nem kérnek cél nélküli újabb iterációt.\
**Feltételek a következő szakaszra:** hipotézis: a 112 szkennelt PDF szövegfelismerése (OCR) után a
keresés megtalálja a tartalmukat. Határidő: legfeljebb két hét (március 4–17.). Költség: kb.
850 000 Ft a PoC-keret tartalékából, Kovács Anita jóváhagyta. **A no-go feltétele:** ha a pivot után
a recall nem zöld, a döntés no-go (3. kill criterion).\
**Felszabaduló keret:** nincs; a bevezetési keret csak go esetén szabadul fel.\
**Nyitott kérdések:** nincs adat a példában.\
**Aláírás:** Horváth Júlia, 2027. március 3.

---

## 4. lap — G1', PoC-kapu a pivot után

**Kapu:** G1 — PoC-kapu\
**Dátum:** 2027. március 19.\
**Ez a kapu hányadik alkalommal ülésezik:** G1' (pivot után)

### Bemenetek

| Bemenet | Verzió / dátum | Hol érhető el |
|---|---|---|
| Teljes regressziós futás | golden set v1.0, a pivot (március 4–17.) után | [Xyo-példa](../04-xyo-pelda.md) 4.5. |
| OCR-szúrópróba | Molnár Katalin: két hiba, kézzel javítva | [adatleltár](adatleltar.md) T-02 |
| Adatleltár | 1.3 | [adatleltár](adatleltar.md) |

### Mutatók

| Mutató | Típus | Küszöb (zöld) | Eredmény | Sáv |
|---|---|---|---|---|
| MK-04 Permission leakage | kizáró | 0 | 0/12 | zöld |
| MK-01 Faithfulness | kritikus | ≥ 0,90 | 0,91 | zöld |
| MK-02 Context recall | kritikus | ≥ 0,85 | **0,88** | zöld |
| MK-03 Correct refusal | kritikus | ≥ 90%, téves ≤ 10% | 8/8; téves 2/24 | zöld |
| MK-05 Latency p95 | támogató | ≤ 8 s | 7,8 s | zöld |
| MK-06 Költség / kérdés | támogató | ≤ 46 Ft | 42 Ft | zöld |

**Esetszintű megjegyzések:** a faithfulness 0,92 → 0,91 csökkenése egyetlen válasz egyetlen állítása;
a kis mintás szabály szerint zaj, nem romlás. Kiss Réka az esetet átnézte, rendben találta.

### Döntés

**A döntés:** **go**.\
**Indoklás:** a kizáró mutató zöld, minden kritikus mutató zöld, a támogatók legalább sárgák (1.3.,
döntési szabályok). A pivot hipotézise igazolódott, a 3. kill criterion nem teljesült.\
**Feltételek a következő szakaszra:** a kettéválás 2027. március 22-től (termékág és bevezetési
ág). A golden set elutasítandó csoportja 20 elemre bővül, mert 8 elemen a ≥ 90%-os küszöb
gyakorlatilag 8/8-at jelent; a küszöböt a G1-en nem lazították.\
**Felszabaduló keret:** a **bevezetési keret 9 800 000 Ft** és az **éves futási keret 3 600 000 Ft**.
A kísérleti szakasz teljes költsége 6,3 M Ft, a 6,5 M Ft-os PoC-kereten belül.\
**Nyitott kérdések:** a golden set elutasítandó csoportjának bővítése — a termékág viszi
tovább (Kiss Réka mint a golden set gazdája; a határidő nincs adat a példában).\
**Aláírás:** Horváth Júlia, 2027. március 19.
