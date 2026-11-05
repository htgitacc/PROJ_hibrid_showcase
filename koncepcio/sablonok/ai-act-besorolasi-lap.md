# AI Act-besorolási lap — [rendszer neve]

> **Használat.** A keretben, a G0 előtt (G0-3, G0-4), és **minden célváltozásnál újra**. A lap a
> jogi döntés **előkészítése**: összegyűjti a tényeket és a kérdéseket, hogy a DPO és a jogász
> dönthessen. **Ez nem jogi tanács, és nem helyettesíti a jogi vizsgálatot.**
>
> A kötelezettségek összefoglalása: [04-es kutatás](../../kutatas/04-szabalyozas.md). A
> legfontosabb szabály: a besorolás a **felhasználási célon** múlik, nem a technológián — ugyanaz a
> rendszer más céllal más kategóriába eshet ([Annex III](../../kutatas/tudasbazis.md#annex-iii)).

---

**Verzió:** [1.0]\
**Előkészítette:** [név, szerep]\
**Dátum:** [éééé.hh.nn.]

## 1. A rendszer és a cél

| Kérdés | Válasz |
|---|---|
| Mit csinál a rendszer? | [egy-két mondat] |
| Mi a **célja** (a projektalapító dokumentum szerint)? | [szó szerint] |
| Mit zár ki kifejezetten? | [a kizárások szó szerint] |
| Kik használják? | [munkatársak / ügyfelek / nyilvános] |
| Milyen adatokból dolgozik? | [hivatkozás az adatleltárra, verzióval] |
| Hoz-e vagy támogat-e döntést személyekről? | [igen / nem — ha igen, milyet] |

## 2. Szerep

| Kérdés | Válasz |
|---|---|
| Ki fejleszti a rendszert? | [cég] |
| Ki hozza forgalomba vagy helyezi üzembe a saját neve alatt? | [cég] |
| Ki használja a saját felelősségére? | [cég] |
| A szerepek ([provider és deployer](../../kutatas/tudasbazis.md#provider-and-deployer)) rögzítése | [szerződés, pont] |

## 3. Kockázati kategória

| Kérdés | Válasz | Indoklás |
|---|---|---|
| Tiltott gyakorlat (AI Act 5. cikk) szóba jöhet? | [nem / vizsgálandó] | [a jogász tölti ki] |
| III. melléklet: melyik pont jöhet szóba? | [pl. 4. pont — foglalkoztatás] | [miért igen / miért nem, a célból és a kizárásokból] |
| Szabályozott termék része (I. melléklet)? | [igen / nem] | |
| **A besorolás** | [nem magas kockázatú / magas kockázatú / vizsgálandó] | |

## 4. Kötelezettségek, amelyek a besorolástól függetlenül élnek

| Kötelezettség | Hogyan teljesítjük | Felelős | Mikorra |
|---|---|---|---|
| [Article 50](../../kutatas/tudasbazis.md#article-50) — a felhasználó tudja, hogy AI-val beszél | [pl. jelzés a felületen az első használatkor] | [név] | [kapu] |
| [AI literacy](../../kutatas/tudasbazis.md#ai-literacy) | [képzés, útmutató] | [név] | [kapu] |

## 5. GDPR

| Kérdés | Válasz |
|---|---|
| Kezel-e a rendszer személyes adatot? | [igen / nem — milyet] |
| Kell-e [DPIA](../../kutatas/tudasbazis.md#dpia) (GDPR 35. cikk)? | [igen / nem — indoklás] |
| Ha igen: elkészült? | [dátum, hivatkozás] |
| Megnéztük a nemzeti hatóság (NAIH) kötelező DPIA-listáját? | [igen / nem] |

## 6. Újravizsgálatot indító események

A besorolást újra kell vizsgálni, ha:

- [ ] a rendszer **célja** változik, vagy új felhasználói kör kapja meg;
- [ ] **új adatkör** kerül be (új tár, új adattípus — különösen HR- vagy ügyféladat);
- [ ] a rendszer **döntést** kezd hozni vagy támogatni személyekről;
- [ ] változáskérés érkezik, amely egy kizárást érint;
- [ ] a szabályozás változik (pl. az AI Act módosítása vagy új útmutató).

## 7. Döntés

**Besorolás:** [...]\
**DPIA:** [kell / nem kell — és ha kell, állapota]\
**Feltételek:** [pl. a kizárások betartása, az AI-jelzés]\
**DPO:** [név, dátum, aláírás]\
**Jogász:** [név, dátum, aláírás]

---

## Kitöltési útmutató

| Mező | Mit írj bele | Példa (Xyo Tudásasszisztens) | Tipikus hiba |
|---|---|---|---|
| A cél | szó szerint a projektalapító dokumentumból | „forrásmegjelöléssel válaszol a szabályzatokból, útmutatókból és projektdokumentumokból, a saját jogosultság szerint” | a technológiát leírni a cél helyett („RAG-chatbot”) |
| Kizárások | szó szerint | egyéni HR-anyagok; nem támogat egyénekről szóló munkaügyi döntést | a kizárást csak szóban rögzíteni |
| Döntés személyekről | igen / nem, konkrétan | nem — és a HR-kizárás ezt őrzi | „csak információt ad” — ha egyénekről ad értékelést, az döntéstámogatás |
| III. melléklet | a szóba jöhető pont és az indoklás | 4. pont (foglalkoztatás) szóba jöhetne; a cél és a kizárás miatt nem esik ide | a vizsgálatot kihagyni, mert „chatbot” |
| Szerep | ki fejleszt, ki üzemeltet | Cloudia Solutions építi, a Xyo üzemelteti; a szerződés rögzíti | feltételezni, hogy a felhasználó cégnek nincs kötelezettsége |
| Article 50 | konkrét megoldás és kapu | AI-jelzés a felületen; a G1 elfogadási feltétele | ÁSZF-be vagy súgóba rejteni |
| DPIA | indoklással | kell: munkavállalói adatokat tartalmazó dokumentumok, új technológia; egyszerűsített DPIA, 2027.01.08. | „belső rendszer, nem kell” |
| Újravizsgálat | a jelölőnégyzetek élnek a projekt alatt | 2027 júniusában a HR-változáskérés ezt indította el → elutasítás | egyszer kitölteni és elfelejteni |
