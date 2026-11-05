# 2. Miért buknak el az AI-projektek?

> **Kérdés:** valóban olyan sok AI-projekt bukik el, ahogy a sajtó írja — és ha igen, miért?
> Technikai a gond, vagy projektmenedzsment-kérdés?
>
> **Rövid válasz:** a bukási arány magas, de **a hírekben keringő számok mást-mást mérnek**, és
> egyik sem „az AI-projektek X%-a bukik el” általános tény. A források abban viszont egyetértenek,
> hogy **a fő okok nem a modell minőségében vannak**, hanem a cél tisztázásában, az adatban, a
> kockázatkezelésben, a költségben és a bevezetésben. Ezek egy része prediktív, más része
> kísérleti kérdés — ezért illik rájuk a hibrid szerkezet.

A szakszavak magyarázata: [tudasbazis.md](tudasbazis.md).

---

## 2.1. A számok — és hogy mit mérnek valójában

| Forrás | Állítás | Mit mér valójában | Korlát |
|---|---|---|---|
| RAND, 2024 (F-03) | „egyes becslések szerint” az AI-projektek **több mint 80%-a** elbukik, ez kétszerese a nem AI-s IT-projektekének | **idézett becslés**, nem a RAND saját mérése | a RAND vizsgálata kifejezetten **kizárta** a kész [LLM](tudasbazis.md#llm)-et csak használó (saját modellt nem tanító) projekteket |
| MIT NANDA, 2025 (F-04) | a szervezetek **95%-a** nem lát megtérülést a [GenAI](tudasbazis.md#genai)-ból; az egyedi, folyamatba ágyazott eszközök **5%-a** jut el élesig | interjúkon és felmérésen alapuló **önbevallás**; „sikeres” = a felhasználók vagy vezetők szerint tartós termelékenységi vagy [P&L](tudasbazis.md#pl)-hatás | 52 szervezet, 153 válaszadó, 300+ nyilvános kezdeményezés; a szerzők szerint a számok „irányukban pontosak”, nem hivatalos céges adatok |
| Gartner, 2026 (F-05) | 2025 végére a GenAI-projektek **legalább 50%-át** feladták a [PoC](tudasbazis.md#poc) után | elemzői megállapítás | a módszertan nyilvánosan nem látszik |
| Gartner, 2025 (F-06) | 2026-ig a szervezetek az **[AI-ready data](tudasbazis.md#ai-ready-data)** nélküli AI-projektek **60%-át** fel fogják adni; a szervezetek 63%-ánál hiányzik, vagy bizonytalan, hogy megvan-e az AI-hoz megfelelő adatkezelési gyakorlat | **előrejelzés**, illetve felmérés | a közlemény a mintát egyszer 248, egyszer 1203 adatkezelési vezetőként adja meg |
| S&P Global, 2025 (F-07) | a cégek **42%-a** hagyta el AI-kezdeményezései többségét (egy évvel korábban 17%); átlagosan a PoC-k **46%-a** áll le élesítés előtt | felmérés, több mint 1000 válaszadó Észak-Amerikában és Európában | másodlagos forrásból (CIO Dive) ismert |

**Hogyan olvasd ezt a táblát.**

- A „80%”, a „95%” és az „50%” **nem ugyanannak a mérése**, nem lehet őket összevetni vagy
  átlagolni. A 80% régebbi, saját modellt tanító ML-projektekre vonatkozó becslés; a 95% a
  megtérülés hiányát méri önbevallással; az 50% a PoC utáni leállítást.
- A **leállítás nem feltétlenül kudarc.** Ha egy PoC időben kimutatja, hogy a feladat nem oldható
  meg a kért minőségben, a leállítás a helyes döntés — a hiba az, ha ez csak hónapok és nagy
  költség után derül ki. Ez a modellünk egyik kulcsgondolata (go/no-go kapu, [*kill criteria*](tudasbazis.md#kill-criteria)).
- Az MIT-jelentés egy fontos árnyalata: az általános célú chatbotoknál a [pilot](tudasbazis.md#pilot)ból élesbe jutás
  aránya ([pilot-to-production rate](tudasbazis.md#pilot-to-production-rate)) magas (kb. 83%), a **feladatspecifikus, folyamatba ágyazott** eszközöknél viszont
  alacsony (20% pilot, 5% sikeres bevezetés) (F-04). A Xyo Tudásasszisztens ez utóbbi típus.

## 2.2. A visszatérő okok

A három fő forrás saját szavaival:

**RAND (F-03)** — 65 tapasztalt adattudós és mérnök interjúja alapján öt fő ok:
1. az érintettek **félreértik vagy rosszul kommunikálják**, milyen problémát kell az AI-val
   megoldani (a modell a rossz mutatót optimalizálja, vagy nem illik a munkafolyamatba);
2. **nincs elég adat** egy hatékony modellhez;
3. a szervezet **a legújabb technológiára** figyel, nem a felhasználó valódi problémájára;
4. **hiányzik az infrastruktúra** az adatkezeléshez és az élesítéshez;
5. a feladat **túl nehéz** az AI-nak.

**Gartner (F-05)** — öt bukási pont GenAI-projekteknél: **nem látható üzleti érték**, az **adat
nem kész**, **elszálló teljes bekerülési költség** ([TCO](tudasbazis.md#tco)), a **[responsible
AI](tudasbazis.md#responsible-ai) utólagos gondolat**, és **gyenge változáskezelés**
([change management](tudasbazis.md#change-management)).

**MIT NANDA (F-04)** — a **[learning gap](tudasbazis.md#learning-gap)**: a bevezetett eszközök nem
tanulnak a visszajelzésből és nem illeszkednek a munkafolyamatba (a válaszadók 66%-a szerint „nem
tanul a visszajelzésünkből”, 63%-a szerint „minden alkalommal túl sok kézi kontextus kell”). A
külső partnerrel épített pilotok kétszer akkora eséllyel jutottak teljes bevezetésig, mint a
belső fejlesztésűek.

**S&P Global (F-07)** — a cégek a költséget, az adatvédelmi és a biztonsági kockázatot nevezték
meg fő akadályként.

## 2.3. Melyik ok melyik megközelítés dolga?

Ez a fejezet saját értelmezés: a fenti okokat aszerint soroljuk be, hogy a projekt melyik
részében kezelhetők a legolcsóbban.

| Ok | Hol kezeljük | Miért ott |
|---|---|---|
| Tisztázatlan probléma, nem látható üzleti érték | **prediktív keret** — üzleti eset, mérhető sikerkritérium | ezt a projekt elején, írásban, számokkal kell rögzíteni; később drága |
| Kockázat, adatvédelem, responsible AI | **prediktív keret** — [DPIA](tudasbazis.md#dpia), [AI Act](tudasbazis.md#ai-act)-besorolás, jogosultsági szabályok | fix követelmények és határidők, jóváhagyással |
| Költség, TCO | **prediktív keret** — költségkeret, futási költség becslése | a beszerzési és üzemeltetési döntés ezen múlik |
| Az adat nincs kész | **mindkettő** — adatleltár a keretben, adatminőség mérése a kísérleti szakaszban | a leltár tervezhető; hogy elég-e, csak méréssel derül ki |
| A feladat túl nehéz az AI-nak | **kísérleti szakasz** — értékelőkészlet, mérőszám-küszöb, PoC-kapu | előre nem tudható, csak kipróbálva |
| Technológia-központúság | **kísérleti szakasz** — az iteráció azt javítja, ami a mérést mozdítja | a mérés köti a munkát a felhasználói problémához |
| Learning gap, munkafolyamatba illesztés | **agilis termékfolyamat** a kapu után — visszajelzés, monitorozás | folyamatos, nem egyszeri feladat |
| Gyenge változáskezelés | **prediktív bevezetés** a kapu után — képzés, kommunikáció, támogatás | ütemezhető, felelőshöz köthető feladat |

**A tanulság a modellnek:** a bukási okok nagyjából fele klasszikus, tervezhető PM-feladat,
negyede csak méréssel dönthető el, a maradék a bevezetés után folyamatos munka. Egyik tiszta
megközelítés sem fedi le mindet — ez a hibrid szerkezet indoka, nem a „hibrid divat”.

---

## Összegzés

| Állítás | Bizonyíték | Erősség |
|---|---|---|
| Az AI-projektek jelentős része nem hozza a várt értéket | F-03, F-04, F-05, F-07 | B–C (eltérő mérések) |
| A gyakori „80% / 95% / 50%” számok mást mérnek, nem összevethetők | a források saját módszertani leírása | — |
| A fő okok nem a modellben, hanem a célban, az adatban, a kockázatban, a költségben és a bevezetésben vannak | F-03, F-05, F-04 | A–B |
| A feladatspecifikus, folyamatba ágyazott eszközök jutnak el legnehezebben élesig | F-04 | C |
| Az okok a prediktív keret, a kísérleti szakasz és a bevezetés után szétoszthatók | saját értelmezés | — |

**Ami nincs benne:** magyar vagy kkv-specifikus bukási adat; a RAND-vizsgálat nem fedi le a kész
LLM-re épülő ([RAG](tudasbazis.md#rag)) projekteket, ezért azokra csak az MIT és a Gartner adatai vonatkoznak.
