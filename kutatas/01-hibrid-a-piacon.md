# 1. A hibrid megközelítés a piacon

> **Kérdés:** valós, elterjedt gyakorlat-e a hibrid projektmenedzsment, vagy csak tankönyvi
> kompromisszum? És ha elterjedt: jobb-e, mint a tiszta prediktív vagy agilis?
>
> **Rövid válasz:** elterjedt és terjed, az IT-ban a legjobban. **Önmagában viszont nem jobb**: a
> PMI szerint a megközelítés megválasztása nem befolyásolja érdemben az eredményt. A hibrid
> értéke nem a „keverés”, hanem az, hogy a projekt egyes részei más-más bizonytalanságot hordoznak,
> és mindegyikhez az illő módszer kell (*fit-for-purpose*).

A szakszavak magyarázata: [tudasbazis.md](tudasbazis.md).

---

## 1.1. Mennyire elterjedt?

A PMI 2024-es *Pulse of the Profession* jelentése (F-01) az éves globális felmérés adatai alapján:

- a **[hybrid approach](tudasbazis.md#hybrid-approach)** használata **20%-ról (2020) 31,5%-ra
  (2023)** nőtt — ez a jelentés kiemelt „+57%”-os adata;
- iparáganként a hibridet leggyakrabban az **információtechnológia (55%)**, az egészségügy (53%)
  és a pénzügyi szolgáltatások (53%) használják; a másik végen az építőipar áll, ahol a hibrid 37%,
  a **[predictive approach](tudasbazis.md#predictive-approach)** viszont 76%;
- egy 477 iparágközi projektet vizsgáló tanulmányban a projektek **52%-a** volt hibridként
  besorolható.

**Hogyan olvasd ezeket a számokat.** A százalékok különböző kérdésekre adott válaszok: a 31,5% a
felmérésben a projektek hibrid arányára vonatkozik, az iparági 55% arra, hogy a válaszadók
„mindig vagy gyakran” használnak-e hibridet — egy szervezet egyszerre több megközelítést is
használhat, ezért az iparági sorok nem adnak ki 100%-ot. A „+57%” relatív növekedés
(20 → 31,5), nem 57 százalékpont.

## 1.2. Jobb-e a hibrid?

**Nem — és ez a fejezet legfontosabb állítása.** A jelentés (F-01) két megállapítása:

- a csapatok **„egyformán jól teljesítenek”** prediktív, hibrid és agilis megközelítéssel;
- a hivatkozott 477 projektes tanulmány szerint **nincs statisztikailag szignifikáns különbség** a
  projektteljesítmény mutatóiban (költség, idő, scope, minőség) a megközelítések között.

A PMI saját mutatója, a **[project performance rate](tudasbazis.md#project-performance-rate)**
(minden válaszadóra átlagosan 73,8%) **önbevalláson** alapul: a válaszadó ítéli meg, elérte-e a
projekt az üzleti céljait.

**Mi következik ebből a modellünkre?**

- Nem állíthatjuk, hogy „a hibrid jobb”. Ilyen állítást a kutatás nem támaszt alá.
- Azt állíthatjuk, amit a PMI is: a választás **a helyzethez illesztés** kérdése
  (*[tailoring](tudasbazis.md#tailoring)*). A jelentés egyik idézett szakembere szerint a jó minta
  az, ha a projekt **„belül agilis, kívül prediktív”** (F-01) — vagyis rögzített keret
  (költségvetés, határidők, jóváhagyások), benne iteratív munkával. Ez pontosan a mi szerkezetünk
  váza.
- A modell értéke tehát nem a módszerek összeadása, hanem annak megmutatása, **melyik
  bizonytalanságra melyik eszköz felel** — ezt a [2. fejezet](02-miert-buknak-el-az-ai-projektek.md)
  bontja ki az AI-projektek sajátos bizonytalanságára.

## 1.3. A szabvány iránya: PMBOK 8

A **[PMBOK](tudasbazis.md#pmbok)** *Guide* nyolcadik kiadása 2025 novemberében jelent meg (F-02). A
kiadó ismertetője szerint:

- megtartja a hetedik kiadás **elveit** (hat alapelv) és **[performance domain](tudasbazis.md#performance-domain)**-jeit
  (hét terület), de egyszerűsítve;
- **visszahozza a folyamatszintű útmutatást**, „nem előíró” módon — ez a hetedik kiadás tisztán
  elvi megközelítésének részleges visszafordítása;
- kifejezetten a **tailoring**-ot, vagyis a gyakorlatok csapathoz, szervezethez és környezethez
  igazítását teszi központi témává;
- **bővített fejezetet** ad az **AI-ról**, a PMO-król és a beszerzésről.

**Korlát:** a szabvány teljes szövegét nem olvastuk, csak a kiadó ismertetőjét. Hogy az AI-fejezet
mit mond konkrétan, azt itt nem állítjuk.

**Mit jelent ez nekünk?** A legnagyobb PM-szabványalkotó maga is a „mindhárom megközelítés,
helyzethez igazítva” irányba lép, és külön foglalkozik az AI-val. Egy hibrid AI-projektmodell
tehát nem a szabványokkal szemben, hanem azok irányában áll.

---

## Összegzés

| Állítás | Bizonyíték | Erősség |
|---|---|---|
| A hibrid elterjedt és terjed, az IT-ban a leginkább | F-01 (globális felmérés) | B |
| A hibrid önmagában nem hoz jobb eredményt | F-01 (477 projekt, nincs szignifikáns különbség) | B |
| A jó hibrid „belül agilis, kívül prediktív” | F-01 (gyakorló szakember idézete) | C |
| A szabvány a helyzethez igazítás felé mozdul, és foglalkozik az AI-val | F-02 (kiadói ismertető) | A* |

\* A szabvány maga A szintű forrás, de csak az ismertetőjét olvastuk.

**Ami nincs benne:** a hazai (magyar) piac adatai. A felmérés globális; magyar bontást nem találtunk.
