# Összefoglaló — mit tudunk, mit nem, és mi következik

Ez a kutatás vezetői összefoglalója. A részletek és a hivatkozások a tematikus dokumentumokban
vannak; a teljes forrásjegyzék megbízhatósági szintezéssel a [forrasok.md](forrasok.md), a
szakszavak magyarázata — angol alakjukban, olvasási útmutatóval — a [tudasbazis.md](tudasbazis.md)
fájlban.

## A kutatás egymondatos eredménye

**Egy AI-projektben három különböző bizonytalanság él egyszerre — mit akar az üzlet és mit enged
a jog (prediktív kérdés), megoldható-e a feladat a kért minőségben (csak méréssel eldönthető
kérdés), és beválik-e a munkában (folyamatos kérdés) —, ezért egyik tiszta megközelítés sem
fedi le; a hibrid itt nem divat, hanem a bizonytalanságok szétválasztása.**

## A hat legfontosabb tanulság

### 1. A hibrid elterjedt — de önmagában nem jobb

A PMI szerint a hibrid használata 2020 és 2023 között 20%-ról 31,5%-ra nőtt, az IT-ban a
leggyakoribb (55%). Ugyanez a jelentés viszont azt is kimondja, hogy **nincs statisztikailag
szignifikáns teljesítménykülönbség** a prediktív, a hibrid és az agilis projektek között. A
modell tehát nem állíthatja, hogy „a hibrid jobb”; azt állíthatja, hogy **a helyzethez illesztett**
módszer a jó — a PMBOK 8 is ebbe az irányba lép. → [01](01-hibrid-a-piacon.md)

### 2. A bukási számok mást mérnek, de az okok egybevágnak

A sajtóban keringő „80% / 95% / 50%” rendre egy idézett becslés, egy önbevalláson alapuló
megtérülési felmérés és egy PoC utáni leállítási arány — nem összevethetők. Amiben a RAND, az MIT
és a Gartner egyetért: **a fő okok nem a modellben vannak**, hanem a cél tisztázásában, az adatban,
a kockázatkezelésben, a költségben és a bevezetésben. Ezek fele tervezhető PM-feladat, egy része
csak méréssel dönthető el, a maradék a bevezetés után folyamatos munka. → [02](02-miert-buknak-el-az-ai-projektek.md)

### 3. A leállítás jó kimenet lehet — ha korán és mérés alapján történik

A PoC-k jelentős része (az S&P szerint átlagosan 46%) élesítés előtt leáll. Ez nem feltétlenül
kudarc: ha egy rövid PoC kimutatja, hogy a feladat nem oldható meg a kért minőségben, a leállítás
a helyes döntés. **A hiba az, ha ez hónapok és nagy költség után derül ki.** Ezért kell előre,
számokkal rögzített go/no-go kapu és leállítási feltétel. → [02](02-miert-buknak-el-az-ai-projektek.md)

### 4. A kísérleti szakaszra van kiforrott módszer — a keretre nincs

A CRISP-DM (2000) és utódja, a PMI CPMAI ugyanazt mondja: az AI-munka ciklikus, a fázisok között
oda-vissza kell lépni, és az értékelés végén döntési pont áll. Egyik sem ad viszont választ a
költségkeretre, a beszerzésre, a megfelelésre és a bevezetésre — a PMI szerint a CPMAI a
hagyományos PM-et **kiegészíti**. LLM-alapú rendszernél ráadásul nincs tanítás: a minőséget a mérés
vezérli, és **minden promptváltozás regressziós kockázat**. → [03](03-ai-projektmodszertanok.md)

### 5. A szabályozás fix pontokat ad — és egy éles scope-határt

Az AI literacy (2025 óta) és az átláthatósági kötelezettség (2026. augusztus óta) **már
alkalmazandó**: a felhasználónak tudnia kell, hogy AI-val beszél. Egy belső tudásasszisztens a
célja szerint nem magas kockázatú — de **ha egyénekről szóló munkaügyi döntéseket támogatna,
azzá válna** (AI Act III. melléklet), 2027. decembertől szigorú követelményekkel. Ezért a cél és a
kizárás írásban rögzített, a HR-anyagok nem kerülnek az indexbe, és a DPIA kérdése a valós adattal
végzett munka előtt eldől. Ezek nem iterálhatók: a prediktív keret mérföldkövei. → [04](04-szabalyozas.md)

### 6. A mérés a munka gerince — és nem egyetlen szám

A döntés alapja egy szakterületi átnéző által jóváhagyott **golden set** (20–50 elemmel indul,
100–1000-re nő). A keresést és a válaszadást **külön** kell mérni, mert másként romlanak el; a
faithfulness csak a megtalált szöveghez mért hűséget méri, az answer relevancy pedig a
pontosságot egyáltalán nem. Az LLM-bíró olcsó, de torzít, ezért emberi szúrópróbával kell
kalibrálni. A szabványos mutatók mellé **saját üzleti és biztonsági mutatók** kellenek —
jogosultság-szivárgásból egyetlen eset is leállító ok. → [05](05-meres-es-ertekeles.md)

## Amit nem tudunk

- **Magyar és kkv-specifikus adatot** sem a hibrid elterjedtségéről, sem az AI-projektek
  bukásáról nem találtunk; a források globálisak, és jellemzően nagyvállalati mintájúak.
- A **RAND-vizsgálat nem fedi le** a kész LLM-re épülő (RAG-) projekteket; ezekre csak az MIT
  (C szint) és a Gartner (B szint) adatai vonatkoznak.
- A **küszöbértékekre** (mi számít „elég jó” faithfulnessnek vagy recallnak) nincs szakmai
  szabvány: ezek üzleti döntések. A koncepció példaértékei feltevésként lesznek jelölve.
- A NAIH DPIA-listáját, a munkajogi egyeztetési kötelezettséget és a szerzői jogi kérdéseket
  nem dolgoztuk fel.

## Mi következik a koncepcióra

| Kutatási tanulság | Koncepcióelem |
|---|---|
| A bizonytalanságok szétválaszthatók (1, 2) | **működési modell**: prediktív keret · kísérleti szakasz · kettéválás a PoC-kapu után |
| A leállítás korán és mérés alapján történjen (3) | **kapuk és kill criteria**, számokkal, előre rögzítve |
| A kísérleti szakaszra a CPMAI-ciklus illik (4) | a kísérleti szakasz **időkeretes iterációi** a CPMAI-fázisokon át, eval-driven módon |
| A szabályozás fix pontokat ad (5) | a prediktív keret **kötelező mérföldkövei** és a scope-kizárás |
| A mérés több mutatóból áll, saját mutatók is kellenek (6) | **mérési rendszer** egységes **mérőszámkártyákkal** és letölthető mintákkal |
| A szakszavak angolul maradnak, olvasni kell tudni őket | a **tudásbázis** a felületen is kereshető nézet lesz |
