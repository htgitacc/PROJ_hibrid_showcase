# 2. Mérési rendszer és mérőszámkártyák

> **Mit ad ez a dokumentum?** Mit mérünk a projekt melyik részében, melyik kapunál dönt a mérés,
> és **minden mutatóhoz egy kitöltött mérőszámkártyát** egységes szerkezetben. A kártyák üres,
> letölthető mintája a [`sablonok/`](sablonok/) mappában lesz, kitöltési útmutatóval.
>
> **Alapelv** (a [05-ös kutatásból](../kutatas/05-meres-es-ertekeles.md)): egyetlen szám nem dönt.
> A keresést és a válaszadást külön mérjük, a szabványos mutatók mellé saját üzleti és biztonsági
> mutatók kellenek, és minden eredményt a [baseline](../kutatas/tudasbazis.md#baseline)-hoz és
> **esetenként** is olvasunk.

A szakszavak magyarázata: [tudasbazis.md](../kutatas/tudasbazis.md). A küszöbértékek a Xyo-példa
**feltevései**, egyeznek a [kapuk](01-kapuk-es-kill-criteria.md) G1-táblájával.

---

## 2.1. A mérési térkép

| Rész | Mit mérünk | Mivel | Melyik döntést vezérli |
|---|---|---|---|
| **Keret** | a mai helyzet: mennyi idő egy információt megtalálni, hányszor kérdezik egymást a kollégák | időmért feladatok, rövid kérdőív, Service Desk-jegyek | az üzleti eset baseline-ja; G0 |
| **Kísérleti szakasz** | válaszminőség, keresésminőség, elutasítás, jogosultság, válaszidő, költség | [golden set](../kutatas/tudasbazis.md#golden-set), jogosultsági tesztkészlet, [LLM-as-a-judge](../kutatas/tudasbazis.md#llm-as-a-judge) emberi szúrópróbával | iterációnként a következő hipotézis; **G1** |
| **Bevezetési ág** | átvétel, elégedettség, hibajegyek, megtakarított idő | használati napló, kérdőív, időmért feladatok (ugyanazok, mint a keretben) | **G2** hullámonként; haszonmérés |
| **Termékág** | ugyanazok a minőségi mutatók élesben + felhasználói visszajelzés | heti regressziós futás, havi emberi mintavétel, válaszonkénti „hasznos volt?” jelzés | sprintcélok; beavatkozás |

## 2.2. A Xyo golden set felépítése (v1)

A kísérleti szakasz 0. iterációjának terméke. **Gazdája:** Kiss Réka (Service Desk vezető — ő látja, mit
kérdeznek a kollégák a jegyekben). **Szakterületi átnézők:** Varga Eszter (HR-szabályzatok), Nagy
Péter (IT-útmutatók), Molnár Katalin (beszerzési szabályok).

| Csoport | Elemszám | Mit tesztel |
|---|---|---|
| Megválaszolható kérdések a kísérleti szakasz tárairól (szabályzatok, útmutatók, projekt-dokumentáció) | 24 | faithfulness, context recall, context precision |
| A tárakban **nem** megválaszolható kérdések | 8 | correct refusal rate |
| Nehéz esetek: kétértelmű, többrészes, angol nyelvű kérdés, prompt-injection kísérlet | 8 | robusztusság; minden mutató |
| **Összesen** | **40** | |

Mellette külön **jogosultsági tesztkészlet**: 3 tesztfelhasználó eltérő jogosultsággal × 4
olyan kérdés, amelyre a válasz csak egy általa **nem** látható dokumentumban van = 12 eset.

**Forrás:** a kérdések a Service Desk-jegyekből és az átnézők gyűjtéséből jönnek (valós
használat), nem generáltak — a [Langfuse-útmutató](../kutatas/05-meres-es-ertekeles.md) szerint ez
az elsődleges forrás. Minden referenciaválaszt egy átnéző jóváhagy.

## 2.3. Egyszerű szabály kis mintára

A 40 elemes készleten **egy eset 2,5 százalékpont**. Egy változtatást ezért csak akkor tekintünk
javulásnak, ha **legalább két esettel több** felel meg, **és** egyetlen korábban jó eset sem romlott
el a kritikus csoportokban. Ennél kisebb különbség zaj lehet. Ez saját, egyszerűsítő szabály — nem
statisztikai próba; a teljes regressziós készlet (100+ elem) a termékágban épül fel.

---

## 2.4. A mérőszámkártya szerkezete

Minden kártya ugyanazt a nyolc kérdést válaszolja meg:

| Szakasz | Kérdés |
|---|---|
| **Mit mér, és miért** | melyik célhoz, kockázathoz vagy kötelezettséghez kötődik |
| **Kiválasztás szempontjai** | miért ez a mutató, és **mit nem mér** (korlátai) |
| **Hol és mikor** | melyik részben, milyen gyakran, melyik kapunál dönt |
| **Ki és mivel** | felelős, adatforrás, módszer és eszköz |
| **Kiértékelés** | képlet, mintanagyság, hogyan olvasd |
| **Mi számít jónak** | zöld / sárga / piros sáv, a kapuhatár |
| **Hosszú távú követés** | mérési ritmus élesítés után, trend, ki nézi |
| **Beavatkozási feltétel** | mi indít újra munkát, és milyet |

---

## 2.5. Minőségi mutatók (a kísérleti szakasz és a G1)

### MK-01 — Faithfulness

| Szakasz | Tartalom |
|---|---|
| **Mit mér, és miért** | A válasz állításai közül hány támasztható alá a megtalált dokumentumrészletekkel. A hallucináció — a forrásban nem szereplő, kitalált állítás — fő jelzője; a felhasználói bizalom ezen áll. |
| **Kiválasztás szempontjai** | Szabványos, jól definiált RAG-mutató ([Ragas](../kutatas/tudasbazis.md#faithfulness)). **Nem méri**, hogy a megtalált forrás helyes-e: rossz dokumentumhoz hű válasz is magas pontot kap — ezért mindig a context recall-lal együtt olvassuk. |
| **Hol és mikor** | A kísérleti szakasz minden iterációjának végén; **G1 kritikus** mutató; élesítés után heti regressziós futás. |
| **Ki és mivel** | A mérést a megvalósító partner (Cloudia Solutions) futtatja a golden set megválaszolható és nehéz csoportján (32 elem), LLM-bíróval; Kiss Réka iterációnként 8 esetet emberileg ellenőriz. |
| **Kiértékelés** | Elemenként: alátámasztott állítások / összes állítás; a készletre átlag. Olvasd esetenként is: melyik kérdéseken alacsony, és ott mi a kitalált állítás. |
| **Mi számít jónak** | Zöld ≥ 0,90 · sárga 0,80–0,89 · piros < 0,80 *(feltevés)*. A végső G1-mérésben piros = **kill criterion**. |
| **Hosszú távú követés** | Heti automatikus futás a teljes golden seten; havi trend az irányítói riportban; a product owner nézi. |
| **Beavatkozási feltétel** | Két egymást követő sárga heti mérés → a következő sprint célja. Bármely piros mérés → a legutóbbi változás visszavonása, amíg az ok nem tisztázott. |

### MK-02 — Context recall

| Szakasz | Tartalom |
|---|---|
| **Mit mér, és miért** | A helyes válaszhoz szükséges információból mennyit talált meg a keresés. Ha alacsony, a hiba a keresésben vagy az adatban van, és a válaszadás promptolással nem javítható. |
| **Kiválasztás szempontjai** | Ez mutatja meg, **hol** kell javítani ([diagnosztikai tábla](../kutatas/05-meres-es-ertekeles.md)). Referenciaválasz kell hozzá — ezért csak a golden seten mérhető, élesben nem. |
| **Hol és mikor** | A kísérleti szakasz minden iterációjában; **G1 kritikus**; élesítés után heti futás és minden új tár indexelése után. |
| **Ki és mivel** | Cloudia Solutions, a golden set megválaszolható csoportján (24 elem), a jóváhagyott referenciaválaszokkal. |
| **Kiértékelés** | Elemenként: a referenciaválasz állításai közül a megtalált szövegre visszavezethetők aránya; a készletre átlag. Alacsony értéknél nézd meg, **hiányzik**-e a dokumentum, **elavult**-e, vagy csak a keresés nem találja. |
| **Mi számít jónak** | Zöld ≥ 0,85 · sárga 0,70–0,84 · piros < 0,70 *(feltevés)*. Tartósan nem zöld recall adatminőségi okból = **kill criterion** (adatrendezési projekt kell). |
| **Hosszú távú követés** | Heti futás; minden új hullám tárainak indexelése után külön mérés. |
| **Beavatkozási feltétel** | Új tár indexelése után sárga → a tár dokumentumainak átnézése az adatgazdával a hullám élesítése (G2) előtt. |

### MK-03 — Correct refusal rate

| Szakasz | Tartalom |
|---|---|
| **Mit mér, és miért** | Azokra a kérdésekre, amelyekre a tárakban nincs válasz, hányszor mondja a rendszer, hogy nem talált forrást — ahelyett, hogy kitalálna egyet. Egy belső asszisztensnél a magabiztos téves válasz a legdrágább hiba. |
| **Kiválasztás szempontjai** | Saját mutató: a faithfulness ezt nem fedi le, ha nincs találat. **Párban** kell olvasni a téves elutasítással (amikor lenne válasz, de elutasít) — a kettő egymás rovására javítható. |
| **Hol és mikor** | A kísérleti szakasz minden iterációjában; **G1 kritikus**; élesítés után heti futás, és élesben a „nem találtam” válaszok aránya. |
| **Ki és mivel** | Cloudia Solutions a golden set 8 nem megválaszolható elemén; a téves elutasítást a 24 megválaszolhatón. Kiss Réka minden elutasítást átnéz. |
| **Kiértékelés** | Helyes elutasítás / nem megválaszolható kérdés. Mellette: téves elutasítás / megválaszolható kérdés. 8 elemnél **egy eset 12,5 pont** — itt különösen esetenként kell olvasni. |
| **Mi számít jónak** | Zöld ≥ 90% · sárga 80–89% · piros < 80% *(feltevés)*, **és** a téves elutasítás legfeljebb 10%. |
| **Hosszú távú követés** | Élesben a „nem találtam” válaszok heti aránya: hirtelen emelkedés új, le nem fedett kérdéstípusra vagy indexelési hibára utal. |
| **Beavatkozási feltétel** | Élesben gyakran visszatérő, el nem utasítható kérdés → új golden set-elem és döntés: hiányzó dokumentum (adatgazda) vagy rendszerhiba (sprint). |

### MK-04 — Permission leakage

| Szakasz | Tartalom |
|---|---|
| **Mit mér, és miért** | Hány esetben kap a felhasználó választ vagy forrásmegjelölést olyan dokumentumból, amelyet a SharePointban nem láthatna. Adatvédelmi és bizalmi kockázat ([GDPR](../kutatas/tudasbazis.md#gdpr)); egyetlen eset is incidens lehet. |
| **Kiválasztás szempontjai** | Saját, **kizáró** mutató. Nem minőségi kérdés, ezért nincs sávja. Csak célzott tesztekkel mérhető — élesben a hiánya nem bizonyíték. |
| **Hol és mikor** | A kísérleti szakasz végén (G1, **kizáró**); minden hullám előtt (G2); élesítés után minden jogosultsági, indexelési vagy verzióváltozásnál. |
| **Ki és mivel** | Szabó Márk (M365 / Entra ID) állítja be a tesztfelhasználókat; a jogosultsági tesztkészletet (12 eset) Cloudia Solutions futtatja; az eredményt dr. Fekete Zsolt (DPO) kapja meg. |
| **Kiértékelés** | Darabszám. Minden eset kivizsgálandó: melyik dokumentum, milyen úton került a válaszba. |
| **Mi számít jónak** | **0.** Bármely ≥ 1 a G1-en kill criterion (ha a jogosultsági elv nélkül nem javítható), a G2-n halasztás. |
| **Hosszú távú követés** | A jogosultsági tesztkészlet bővül minden új tárral és szereppel; havonta teljes futás. |
| **Beavatkozási feltétel** | Bármely eset → az érintett tár **azonnali** kivétele az indexből, incidenskezelés, DPO értesítése, ok feltárása az újraindexelés előtt. |

---

## 2.6. Üzemeltetési és üzleti mutatók (G1 támogató, bevezetési ág, termékág)

### MK-05 — Latency p95

| Szakasz | Tartalom |
|---|---|
| **Mit mér, és miért** | A válaszidő, amelynél a válaszok 95%-a gyorsabb. A lassú eszközt a felhasználók elhagyják, és visszatérnek a „megkérdezem a kollégát” megoldáshoz — ez a [learning gap](../kutatas/tudasbazis.md#learning-gap) egyik gyakorlati oka. |
| **Kiválasztás szempontjai** | A percentilis a „rossz napot” mutatja, az átlag elrejtené ([tudásbázis](../kutatas/tudasbazis.md#latency)). **Nem méri** az észlelt sebességet (pl. ha a válasz fokozatosan jelenik meg, a várakozás rövidebbnek tűnik). |
| **Hol és mikor** | A kísérleti szakasz végén (G1, **támogató**); élesítés után folyamatosan, a rendszer naplójából. |
| **Ki és mivel** | Cloudia Solutions a golden set futtatásakor méri; élesben az alkalmazás naplójából automatikusan; Nagy Péter (IT) felel az üzemeltetési riportért. |
| **Kiértékelés** | A kérdés elküldésétől a teljes válaszig eltelt idő; a mérések 95. percentilise. A G1-en a golden set 40 elemének futtatásából — ez kevés, ezért élesben, nagyobb mintán újra kell nézni. |
| **Mi számít jónak** | Zöld ≤ 8 s · sárga 8–15 s · piros > 15 s *(feltevés)*. |
| **Hosszú távú követés** | Napi automatikus érték, heti trend; csúcsidőszakonként (pl. hétfő reggel) külön is. |
| **Beavatkozási feltétel** | Egy héten át sárga → a product owner sprintcélt dönt (pl. kevesebb találat, gyorsabb modellváltozat — utóbbinál kötelező a teljes regressziós mérés). |

### MK-06 — Kérdésenkénti költség (cost per query)

| Szakasz | Tartalom |
|---|---|
| **Mit mér, és miért** | Egy megválaszolt kérdés átlagos futási költsége (modell- és keresési díjak). A [TCO](../kutatas/tudasbazis.md#tco) legnehezebben becsülhető része, mert a használattal nő; a Gartner szerint az elszálló költség a GenAI-projektek egyik bukási pontja. |
| **Kiválasztás szempontjai** | Egyszerű, közvetlenül a szolgáltatói számlából ellenőrizhető. **Nem tartalmazza** az üzemeltetés és a továbbfejlesztés munkaköltségét — azok a TCO többi sorában vannak. |
| **Hol és mikor** | A kísérleti szakasz végén éves becslésként (G1, **támogató**); élesítés után havonta a számla alapján. |
| **Ki és mivel** | Becslés: Cloudia Solutions; havi ellenőrzés: Balogh Tamás (pénzügyi kontroller) a szolgáltatói számlából és a használati naplóból. |
| **Kiértékelés** | Havi futási díj / havi megválaszolt kérdések száma. **Éves becslés a G1-en:** kérdésenkénti költség × várható heti kérdésszám (a keret kérdőívéből) × aktív felhasználók × 46 munkahét. |
| **Mi számít jónak** | Az éves becslés a G0-n jóváhagyott futási kereten belül: zöld; a keret 100–120%-a: sárga; afölött piros, és ha nincs olcsóbb változat, **kill criterion** *(feltevés)*. |
| **Hosszú távú követés** | Havi összeg és kérdésenkénti költség, a keret időarányos részéhez mérve; negyedévente az irányító bizottságnak. |
| **Beavatkozási feltétel** | Két egymást követő hónap a keret időarányos része fölött → költségcsökkentő sprint vagy szolgáltatói egyeztetés; afölött változáskérés a keretnek. |

### MK-07 — Heti aktív felhasználók aránya

| Szakasz | Tartalom |
|---|---|
| **Mit mér, és miért** | A hozzáféréssel rendelkező munkatársak hány százaléka használta az asszisztenst az adott héten. Az átvétel legegyszerűbb jele; a [változáskezelés](../kutatas/tudasbazis.md#change-management) sikerét méri. |
| **Kiválasztás szempontjai** | Olcsón, automatikusan mérhető. **Nem méri**, hogy a használat hasznos-e — ezért a válaszonkénti „hasznos volt?” jelzés aránya is mellette áll. Az új eszköz kezdeti kíváncsisága felfelé torzít: az első hetek nem mérvadók. |
| **Hol és mikor** | A bevezetési ágban hullámonként; a következő hullám G2-feltétele (G2-6); a haszonmérés része. |
| **Ki és mivel** | A használati naplóból automatikusan; Tóth Gergő (PM) a bevezetés alatt, utána a product owner (Kiss Réka) nézi. |
| **Kiértékelés** | Az adott héten legalább egy kérdést feltevő felhasználók / hozzáféréssel rendelkezők. Hullámonként külön, a hullám élesítése óta eltelt hetek szerint. |
| **Mi számít jónak** | Az élesítés utáni 8. héten: zöld ≥ 50% · sárga 30–49% · piros < 30% *(feltevés)*; a „hasznos volt” arány legalább 70%. |
| **Hosszú távú követés** | Heti érték, havi trend; szervezeti egységenként is, hogy látszódjon, hol nem vették át. |
| **Beavatkozási feltétel** | Egy egységben a 8. héten piros → célzott megkeresés (mi hiányzik: tartalom, képzés, bizalom?), és a válasz alapján képzés vagy backlog-elem. |

### MK-08 — Megtakarított idő

| Szakasz | Tartalom |
|---|---|
| **Mit mér, és miért** | Mennyivel rövidebb egy tipikus információkeresési feladat az asszisztenssel, mint nélküle. Az üzleti eset haszonoldala. |
| **Kiválasztás szempontjai** | A **mért feladatidő** az elsődleges, mert a saját időbecslés torzít; a kérdőív csak a gyakoriság becsléséhez kell. **Nem azonos** a pénzügyi haszonnal: [P&L](../kutatas/tudasbazis.md#pl)-hatás csak akkor, ha a felszabaduló idő máshol értéket termel. |
| **Hol és mikor** | **Baseline a keretben** (T0, az asszisztens előtt); második mérés a pilot élesítése után 4 héttel (T1); a haszonmérésben negyedévente. |
| **Ki és mivel** | 10 időmért feladat (pl. „keresd meg, hány nap szabadság vihető át”, „mi a beszerzési értékhatár árajánlatkéréshez”), 10 pilot-résztvevő, Tóth Gergő vezeti; a feladatsort Kiss Réka és az átnézők állítják össze a Service Desk-jegyekből. |
| **Kiértékelés** | Feladatonként a medián idő T0-n és T1-en; a csökkenés százalékban. Éves becslés: megtakarítás / feladat × heti feladatszám (kérdőív) × aktív felhasználók × 46 hét — **becslésként** jelölve. |
| **Mi számít jónak** | A medián feladatidő csökkenése: zöld ≥ 30% · sárga 15–29% · piros < 15% *(feltevés)* — és egyetlen feladatnál sem nő a hibás eredmények száma. |
| **Hosszú távú követés** | Negyedéves ismétlés kisebb mintán; a feladatsor évente frissül a jegyek alapján. |
| **Beavatkozási feltétel** | Ha egy feladattípusnál nincs megtakarítás → a tartalom vagy a keresés vizsgálata (MK-02), nem a képzés növelése. |

---

## 2.7. Összesítő: melyik kártya melyik döntést vezérli

| Kártya | G1 szerepe | G2 | Felelős a mérésért | Ritmus élesítés után |
|---|---|---|---|---|
| MK-01 Faithfulness | kritikus | regresszió (G2-3) | Cloudia Solutions / Kiss Réka | heti |
| MK-02 Context recall | kritikus | új tár után | Cloudia Solutions | heti + indexelés után |
| MK-03 Correct refusal rate | kritikus | regresszió | Cloudia Solutions / Kiss Réka | heti |
| MK-04 Permission leakage | **kizáró** | **kizáró** (G2-2) | Szabó Márk / Cloudia / DPO | minden változásnál + havi |
| MK-05 Latency p95 | támogató | — | Nagy Péter | napi |
| MK-06 Kérdésenkénti költség | támogató (éves becslés) | — | Balogh Tamás | havi |
| MK-07 Heti aktív felhasználók | — | előző hullám (G2-6) | Tóth Gergő → Kiss Réka | heti |
| MK-08 Megtakarított idő | — (baseline a keretben) | — | Tóth Gergő | negyedéves |

Az [answer relevancy](../kutatas/tudasbazis.md#answer-relevancy) és a [context precision](../kutatas/tudasbazis.md#context-precision)
diagnosztikai mutatók: a kísérleti szakasz iterációiban segítenek megtalálni a hiba helyét, de döntést nem
alapozunk rájuk, ezért nincs kártyájuk.
