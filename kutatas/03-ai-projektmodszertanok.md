# 3. AI-projektmódszertanok: CRISP-DM, CPMAI, eval-driven development

> **Kérdés:** van-e kiforrott módszertan kifejezetten AI-projektekre? Ha igen, kiváltja-e a
> projektmenedzsmentet, vagy kiegészíti?
>
> **Rövid válasz:** van, és mind ugyanazt mondja: **az AI-munka ciklikus, adatvezérelt, és a
> fázisok között oda-vissza kell lépni.** Egyik sem projektmenedzsment-keretrendszer a szó
> teljes értelmében: nem foglalkozik költségkerettel, beszerzéssel, megfeleléssel, bevezetéssel.
> A PMI maga is úgy fogalmaz, hogy a CPMAI **kiegészíti** a hagyományos PM-gyakorlatot. Ez a
> hibrid szerkezet második indoka: a kísérleti szakaszra van módszertan, a keretet a PM adja.

A szakszavak magyarázata: [tudasbazis.md](tudasbazis.md).

---

## 3.1. CRISP-DM — az ősforrás (2000)

A **[CRISP-DM](tudasbazis.md#crisp-dm)** egy ipari konzorcium (NCR, SPSS, DaimlerChrysler, OHRA)
adatbányászati folyamatmodellje (F-08). Hat fázisa:

1. *Business Understanding* — üzleti megértés;
2. *Data Understanding* — adatmegértés;
3. *Data Preparation* — adatelőkészítés;
4. *Modeling* — modellezés;
5. *Evaluation* — értékelés;
6. *Deployment* — élesítés.

Két mondata ma is a lényeg (F-08):

- „**A fázisok sorrendje nem merev. A fázisok közötti oda-vissza lépés mindig szükséges.** Az
  egyes fázisok eredménye határozza meg, melyik fázis vagy feladat következik.”
- Az értékelés célja annak eldöntése, hogy a modell **valóban eléri-e az üzleti célokat**, és
  maradt-e figyelmen kívül fontos üzleti szempont; **„a fázis végén döntést kell hozni az
  eredmények felhasználásáról.”**

Ez utóbbi lényegében egy **[stage gate](tudasbazis.md#stage-gate)**: 25 évvel ezelőtt már benne
volt a modellben, hogy az élesítés előtt döntési pont áll.

## 3.2. CPMAI — a PMI AI-módszertana

A **[CPMAI](tudasbazis.md#cpmai)** (*Cognitive Project Management for AI*) a PMI saját minősítéseként
(PMI-CPMAI) kínált módszertan. A PMI blogja szerint (F-09) hat fázisa:

| Fázis | Lényege (F-09) |
|---|---|
| 1. Business understanding | a probléma és a cél tisztázása; **annak eldöntése, hogy egyáltalán az AI-e a jó megoldás** |
| 2. Data understanding | milyen adat létezik, hozzáférhető-e, tükrözi-e a valós helyzetet; korai adatkormányzás |
| 3. Data preparation | tisztítás, címkézés, egységesítés, duplikátumok szűrése |
| 4. Model development | modellválasztás, tanítás, hangolás — **a korábban rögzített mérhető célok vezérlik, nem a kísérletezés öncélúan** |
| 5. Model evaluation | értékelés üzleti és technikai kritériumok szerint; teljesítmény, méltányosság, megbízhatóság |
| 6. Model operationalization | beillesztés a munkafolyamatba, monitorozás és visszajelzési hurok, változáskezelés |

A fázisok **sorrendben szerepelnek, de iteratívak**: a csapat oda-vissza léphet, ahogy új
felismerések jönnek (F-09). A cikk szerint a hagyományos PM „szilárd alapot” ad (scope,
érintettek, kockázat), az AI-projektek viszont rugalmasságot, kísérletezést és folyamatos
tanulást is igényelnek — a CPMAI ezt **kiegészítő struktúraként** adja hozzá.

**Hogyan olvasd.** A CPMAI fázisai szinte szó szerint a CRISP-DM fázisai; az újdonság a hangsúly:
az 1. fázisban ott a „kell-e egyáltalán AI” kérdés, a 6. fázisban a változáskezelés és a
visszajelzési hurok. **Forráskorlát:** a PMI saját minősítését népszerűsítő blogcikkről van szó
(C szint); a CPMAI teljes tananyagát nem olvastuk.

## 3.3. Eval-driven development — az LLM-korszak válasza

A CRISP-DM és a CPMAI a **saját modellt tanító** projektekre készült. Egy [RAG](tudasbazis.md#rag)-
asszisztensnél nincs tanítás: a modellt szolgáltatótól vesszük, és a minőséget a dokumentumok
előkészítése, a keresés beállítása és a [prompt](tudasbazis.md#prompt) határozza meg. Itt a mérés
lesz a munka gerince: ez az **[eval-driven development](tudasbazis.md#eval-driven-development)**.

Egy 2026-os technikai jelentés (F-10) jól mutatja, miért:

- az LLM-alkalmazások értékelése azért más, mint a hagyományos szoftvertesztelés, mert a
  kimenet **valószínűségi**, jelentésében változékony, és érzékeny a prompt és a modell
  változására;
- reprodukálható kísérletben **az „általános jó tanácsok” hozzáadása a prompthoz nem javított
  egyenletesen**: a szigorúbb kimeneti szerződés javította a strukturált kinyerést, a RAG
  hivatkozási és tartalmi megfelelése viszont egyes esetekben romlott — a legnagyobb esés 30-ból
  **26 helyes válaszról 9-re**;
- a következtetés: **minden promptváltozás regressziós kockázat**, és élesítés előtt
  feladatspecifikus tesztkészleten kell ellenőrizni.

**Hogyan olvasd.** A kísérlet kis helyi modellekkel (8 és 7 milliárd paraméteres) és esetenként
30 tesztesettel készült; a konkrét számok nem vihetők át egy nagy, felhőben futó modellre. Ami
átvihető: **amit nem mérsz, arról nem tudod, javult-e vagy romlott** — és a „nyilvánvaló
javítás” is ronthat.

## 3.4. Mit veszünk át a modellbe?

Saját értelmezés: a CPMAI fázisai egy RAG-projektre lefordítva, és hogy melyik a hibrid
szerkezet melyik részébe esik.

| CPMAI-fázis | A Xyo Tudásasszisztensnél | Hol a modellben |
|---|---|---|
| 1. Business understanding | üzleti eset, mérhető sikerkritériumok, „kell-e AI” döntés | **prediktív keret** |
| 2. Data understanding | adatleltár: mely SharePoint-tárak, kié, mennyire friss, ki láthatja | **prediktív keret** (leltár) + **kísérleti szakasz** (minőség mérése) |
| 3. Data preparation | dokumentumok tisztítása, darabolása, jogosultságok átvétele | **kísérleti szakasz** |
| 4. Model development | nincs tanítás: modell- és szolgáltatóválasztás, keresés és prompt beállítása | **kísérleti szakasz**, iterációnként |
| 5. Model evaluation | értékelőkészlet és mérőszám-küszöbök → **PoC-kapu** | **a kapu** |
| 6. Operationalization | bevezetés, képzés, monitorozás, visszajelzés | **kettéválás**: prediktív bevezetés + agilis termékfolyamat |

**A tanulság a modellnek:**

- A kísérleti szakaszra van kiforrott, 25 éves mintázat (CRISP-DM), és a PMI által is elfogadott
  változata (CPMAI) — nem kell kitalálni.
- Az **5. fázis a kulcs**: ott dől el a mérés alapján, hogy megy-e tovább a projekt. LLM-nél ez
  nem egyszeri lépés, hanem minden változtatás után újrafutó tesztkészlet
  ([regression testing](tudasbazis.md#regression-testing), F-10).
- Amit ezek a módszertanok **nem adnak**: költségkeret, beszerzés, szerződés, megfelelés
  (DPIA, AI Act), bevezetési terv, haszonrealizálás. Ezt a prediktív keret adja — innen a hibrid.

---

## Összegzés

| Állítás | Bizonyíték | Erősség |
|---|---|---|
| Az AI-munka ciklikus, a fázisok között oda-vissza kell lépni | F-08, F-09 | B, C |
| Az értékelés végén döntési pont áll az élesítés előtt | F-08 | B |
| A CPMAI a hagyományos PM-et kiegészíti, nem kiváltja | F-09 | C |
| LLM-alkalmazásnál minden promptváltozás regressziós kockázat, mérni kell | F-10 | B |
| A CPMAI-fázisok a prediktív keret, a kísérleti szakasz és a kettéválás közt szétoszthatók | saját értelmezés | — |

**Ami nincs benne:** az agilis ML-gyakorlatok (pl. a Scrum adattudományi alkalmazása) és az
[MLOps](tudasbazis.md#mlops) részletei; ezekre csak akkor térünk ki, ha a koncepció igényli.
