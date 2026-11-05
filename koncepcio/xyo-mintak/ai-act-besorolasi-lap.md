# Kitöltött AI Act-lap — Xyo

> Az [AI Act-besorolási lap](../sablonok/ai-act-besorolasi-lap.md) minta kitöltve a Xyo
> Tudásasszisztensre. A tények forrása a [Xyo-példa](../04-xyo-pelda.md) 4.2. és 4.7. pontja, az
> [adatleltár](adatleltar.md) és a [szabályozási kutatás](../../kutatas/04-szabalyozas.md).
> **A lap jogi döntés-előkészítés, nem jogi tanács**: a besorolást dr. Fekete Zsolt (DPO) és a cég
> jogásza mondta ki, a lap csak azt rögzíti, amit a példa tartalmaz. Ami a forrásban nincs kimondva,
> azt **„nincs adat a példában”** jelöli, nem találtam ki.
> A szakszavak: [tudasbazis.md](../../kutatas/tudasbazis.md).

**Verzió:** 1.2 (története lent)\
**Előkészítette:** Tóth Gergő, projektmenedzser\
**Dátum:** 2026. december 18. (első G0); frissítve 2027. január 8. (második G0) és 2027. júniusban

| Verzió | Mikor | Mi változott |
|---|---|---|
| 1.0 | 2026. december 18. | a besorolás és a szerepek; a DPIA-döntés még nyitott (G0-4 nem teljesült) |
| 1.1 | 2027. január 8. | DPIA-döntés: kell, egyszerűsített DPIA elkészült; az adatleltár X-02 szabálya felvéve |
| 1.2 | 2027. június | a HR-változáskérés újravizsgálatot indított (6. pont); a besorolás nem változott, mert a kérést elutasították |

A verziószámozás és a dátumok a példa **feltevései** (az események a 4.2–4.3. és 4.7. pontból valók).

## 1. A rendszer és a cél

| Kérdés | Válasz |
|---|---|
| Mit csinál a rendszer? | Belső információkereső (RAG) asszisztens: a Xyo SharePoint-tárainak dokumentumaiból, forrásmegjelöléssel válaszol a munkatársak kérdéseire. |
| Mi a **célja** (a projektalapító dokumentum szerint)? | A munkatársak a céges szabályzatokból, útmutatókból és projektdokumentumokból forrásmegjelöléssel kapjanak választ, a saját SharePoint-jogosultságuk szerint. |
| Mit zár ki kifejezetten? | Egyéni HR-anyagok (teljesítményértékelések, bérek, fegyelmik), vezetői levelezés; a rendszer nem támogat egyénekről szóló munkaügyi döntést. |
| Kik használják? | A Xyo munkatársai (kb. 240 fő): a pilot 50 fője, majd három hullámban a maradék 190. |
| Milyen adatokból dolgozik? | A kísérleti szakasz négy SharePoint-tára, [adatleltár](adatleltar.md) 1.3-as verzió; a nyers kérdőív-export kizárva (X-02). |
| Hoz-e vagy támogat-e döntést személyekről? | Nem. A HR-kizárás ezt őrzi; a 2027. júniusi változáskérés (egyének teljesítményének összefoglalása) pontosan ezt lépte volna át, ezért elutasították. |

## 2. Szerep

| Kérdés | Válasz |
|---|---|
| Ki fejleszti a rendszert? | Cloudia Solutions Kft. |
| Ki hozza forgalomba vagy helyezi üzembe a saját neve alatt? | A Cloudia építi, a Xyo üzemelteti; a pontos szerepkiosztást ([provider és deployer](../../kutatas/tudasbazis.md#provider-and-deployer)) a jogász rögzíti. Nincs adat a példában, hogy melyik cég számít providernek. |
| Ki használja a saját felelősségére? | A Xyo Kft. |
| A szerepek rögzítése | A szerződésben (a példa szerint); a szerződés pontjának száma nincs adat a példában. |

## 3. Kockázati kategória

| Kérdés | Válasz | Indoklás |
|---|---|---|
| Tiltott gyakorlat (AI Act 5. cikk) szóba jöhet? | Nincs adat a példában. | A jogász tölti ki. |
| III. melléklet: melyik pont jöhet szóba? | A 4. pont (foglalkoztatás) szóba jöhetne, de nem esik ide. | A cél (szabályzatokból való információkeresés) és a kizárás (egyéni HR-anyagok, nincs döntés személyekről) miatt. A 4(b) pont (teljesítmény értékelése) akkor lépne életbe, ha a rendszer egyének teljesítményét támogatná. |
| Szabályozott termék része (I. melléklet)? | Nem. | Belső információkereső, nem szabályozott termék része *(a lap előkészítőjének megállapítása)*. |
| **A besorolás** | **Nem magas kockázatú** belső információkereső rendszer. | dr. Fekete Zsolt (DPO) és a cég jogásza szerint (4.2.). |

## 4. Kötelezettségek, amelyek a besorolástól függetlenül élnek

| Kötelezettség | Hogyan teljesítjük | Felelős | Mikorra |
|---|---|---|---|
| [Article 50](../../kutatas/tudasbazis.md#article-50) — a felhasználó tudja, hogy AI-val beszél | AI-jelzés a felületen, legkésőbb az első interakciónál | Cloudia Solutions (felület), ellenőrzi Tóth Gergő *(feltevés)* | elfogadási feltétel; hullámonként a G2-4 ellenőrzi |
| [AI literacy](../../kutatas/tudasbazis.md#ai-literacy) | Képzés és egyoldalas „mire figyelj” kártya (a válasz hibás lehet, nézd meg a forrást, mit nem tud a rendszer) | Varga Eszter (HR) | minden hullám előtt (G2-4) |

Mindkét kötelezettség a kutatás szerint már ma alkalmazandó (az AI literacy 2025. február 2-tól,
az 50. cikk 2026. augusztus 2-től), ezért nem „felkészülni” kell rájuk, hanem az első naptól teljesíteni.

## 5. GDPR

| Kérdés | Válasz |
|---|---|
| Kezel-e a rendszer személyes adatot? | Igen: munkavállalói adatokat tartalmazó dokumentumokat dolgoz fel (a kérdőív-export névvel, amelyet kizártak). |
| Kell-e [DPIA](../../kutatas/tudasbazis.md#dpia) (GDPR 35. cikk)? | Igen: munkavállalói adatokat tartalmazó dokumentumok feldolgozása új technológiával. A DPIA-t az adatkezelés előtt el kell dönteni. |
| Ha igen: elkészült? | Egyszerűsített DPIA, dr. Fekete Zsolt, 2027. január 8. (a második G0 feltétele). |
| Megnéztük a nemzeti hatóság (NAIH) kötelező DPIA-listáját? | Nincs adat a példában. A kutatás sem tartalmazza a listát, ezért a DPO-nak a G0 előtt meg kell néznie. |

## 6. Újravizsgálatot indító események

- [ ] a rendszer **célja** változik, vagy új felhasználói kör kapja meg — nem történt;
- [x] **új adatkör** kerül be — a Pénzügy tár a 2. hullámmal ([adatleltár](adatleltar.md) D-06), jogosultsági teszttel;
- [ ] a rendszer **döntést** kezd hozni vagy támogatni személyekről — nem;
- [x] változáskérés érkezik, amely egy kizárást érint — **igen**, 2027. június: a beosztottak teljesítményének összefoglalása. Hatáselemzés (Varga Eszter, dr. Fekete Zsolt): III. melléklet 4(b), magas kockázatú, új DPIA kellene. **Elutasítás ebben a projektben**; új projekt saját besorolással és DPIA-val;
- [ ] a szabályozás változik — a példában nem szerepel; a kutatás az Omnibus utáni idővonalat vette alapul (a magas kockázatú szabályok 2027. december 2-tól alkalmazandók).

A kipipált sor azt jelzi, hogy az esemény **felmerült** a projekt alatt. A Pénzügy tár felvétele
nem változtatta meg a besorolást; a változáskérés elutasítása óta a besorolás érvényes.

## 7. Döntés

**Besorolás:** nem magas kockázatú belső információkereső rendszer.\
**DPIA:** kell; az egyszerűsített DPIA elkészült (2027. január 8.).\
**Feltételek:** az X-01 és X-02 kizárások betartása; AI-jelzés a felületen; AI literacy képzés
hullámonként; bármely, a kizárást vagy a célt érintő változás újravizsgálatot indít.\
**DPO:** dr. Fekete Zsolt, 2027. január 8. *(aláírás: a mintában nem szerepel)*\
**Jogász:** a cég jogásza *(neve nincs adat a példában)*
