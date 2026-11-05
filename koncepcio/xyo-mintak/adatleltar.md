# Kitöltött adatleltár — Xyo

> Az [adatleltár](../sablonok/adatleltar.md) minta kitöltve a Xyo kísérleti szakaszának tárairól. A forrás a
> [Xyo-példa](../04-xyo-pelda.md) 4.2–4.4. pontja és a [szerepek](../03-szerepek.md) táblája. Ami a
> forrásban nincs kimondva, azt **feltevésnek** jelöltem; a darabszámokból csak az összeg szerepel
> (kb. 1 900), tárankénti bontást a példa nem rögzít.
> A szakszavak: [tudasbazis.md](../../kutatas/tudasbazis.md).

**Verzió:** 1.3 (története lent)\
**Állapot:** jóváhagyva\
**Készítette:** Tóth Gergő, projektmenedzser\
**Átnézte (DPO):** dr. Fekete Zsolt — a második G0 (2027. január 8.) feltételeként, az egyszerűsített DPIA mellett

A verziószámozás és a dátumok a példa **feltevései** (az események a 4.3–4.5. pontból valók).

| Verzió | Mikor | Mi változott |
|---|---|---|
| 1.0 | 2026. december 18. (első G0) | az első leltár; a kérdőív-export észrevétele miatt a G0-4 nem teljesült |
| 1.1 | 2027. január 8. (második G0) | D-04 kizárva, X-02 felvéve, D-05 (összesítő riport) bent marad |
| 1.2 | 2027. február 26. (3. iteráció) | T-01: 37 elavult dokumentum archiválva |
| 1.3 | 2027. március 17. (pivot) | T-02: 112 szkennelt PDF OCR-je kész |

## 1. Források

| # | Forrás (tár / mappa) | Adatgazda | Tartalom | Dokumentumok száma | Frissesség | Jogosultsági modell | Személyes adat? | Döntés |
|---|---|---|---|---|---|---|---|---|
| D-01 | HR-szabályzatok tár | Varga Eszter *(feltevés: a szakterületi átnéző a gazda)* | általános szabályzatok, nem egyéni anyagok | a négy tár együtt kb. 1 900 | nincs adat | SharePoint-jogosultság, a kérdező jogai szerint | nincs adat a példában | **be** — az egyéni HR-anyagok nélkül (X-01) |
| D-02 | IT-útmutatók tár | Nagy Péter *(feltevés)* | IT-útmutatók | lásd D-01 | nincs adat | SharePoint-jogosultság | nincs adat a példában | **be** |
| D-03 | Beszerzés tár | Molnár Katalin *(feltevés)* | beszerzési szabályok; köztük 112 szkennelt PDF | lásd D-01 | két változat él egyes szabályzatokból (régi és új) | SharePoint-jogosultság | nincs adat a példában | **tisztítás után be** (T-01, T-02) |
| D-04 | Cloud Pilot projekttár — a pilot elégedettségi kérdőíveinek névvel ellátott nyers exportja | Tóth Gergő *(feltevés: a projekttár gazdája a PM)* | névvel ellátott nyers kérdőív-export | nincs adat | nincs adat | a projekttár jogai | **igen: nevek**, munkavállalói adat | **ki** (X-02) |
| D-05 | Cloud Pilot projekttár — a többi anyag, köztük az összesítő riport | Tóth Gergő *(feltevés)* | projektdokumentumok, összesítő riport | lásd D-01 | nincs adat | a projekttár jogai | nincs adat a példában | **be** |
| D-06 | Pénzügy tár *(a 2. hullámhoz, G2-1)* | a hullám előtt kijelölendő | a pénzügy dokumentumai | nincs adat | nincs adat | **egy almappán megszakadt az öröklődés** — a 2. hullám G2-jén derült ki | nincs adat | **a 2. hullám előtt, jogosultsági teszttel** (2027. július) |

A D-01–D-05 a kísérleti szakasz négy tára (a projekttár két sorra bontva): HR-szabályzatok, IT-útmutatók, Beszerzés,
Cloud Pilot projekttár. A D-04 azt mutatja, miért kell a **vegyes** tárat mappa szintjén nézni.

## 2. Kizárási szabályok

| # | Szabály | Indok | Hogyan ellenőrizzük |
|---|---|---|---|
| X-01 | Egyéni HR-anyagok (teljesítményértékelések, bérek, fegyelmik) és vezetői levelezés nem kerülhet be. | A cél a szabályzatokból és útmutatókból való válasz; a rendszer nem támogat egyénekről szóló munkaügyi döntést (AI Act III. melléklet 4. pont). | Mappakizárás az indexelésnél és szúrópróba *(a példa javaslata)*; a HR-kizárás az irányító bizottság jóváhagyta scope-határa. |
| X-02 | A pilot kérdőíveinek névvel ellátott nyers exportja nem kerülhet be; az összesítő riport bent marad. | Munkavállalói adat, nem tartozik a cél körébe; a DPO addig nem ad állásfoglalást, amíg nem tisztázott, mi kerül a rendszerbe. | Mappakizárás az indexelés előtt *(a példa javaslata)*; a kísérleti szakasz **csak a második G0 után** indulhat. |

## 3. Tisztítási teendők

| # | Forrás | Teendő | Felelős | Határidő | Kész? |
|---|---|---|---|---|---|
| T-01 | a tárak elavult szabályzatai (a 3. iteráció) | 37 elavult dokumentum archiválása, hogy a keresés a legfrissebb érvényes változatot hozza | az adatgazdák | 2027. február 15–26. (3. iteráció) | [x] |
| T-02 | D-03 | 112 szkennelt PDF szövegfelismerése (OCR); szúrópróba, hogy az értékhatár-táblázatok számai helyesek-e (két hibát találtak, kézzel javították) | Cloudia Solutions (OCR), Molnár Katalin (szúrópróba) | 2027. március 4–17. (pivot) | [x] |

## 4. Jogosultsági elv

Az asszisztens csak azt használja, amit a kérdező a SharePointban lát (G0-6) — a SharePoint-jogosultságok
átvételét Szabó Márk ellenőrzi, a jogosultsági tesztkészlet (MK-04) minden új tár előtt lefut.
