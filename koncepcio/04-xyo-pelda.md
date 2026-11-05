# 4. A Xyo Tudásasszisztens végigvezetve

> **Mit ad ez a dokumentum?** A modell próbáját egy kitalált, de valószerű projekten. A cél nem
> az, hogy minden jól menjen, hanem hogy **minden kapu működésbe lépjen**: a G0-n hiánypótlás
> lesz, a G1-en pivot, a bevezetésben egy G2-halasztás, a termékágban pedig egy elutasított
> változáskérés.
>
> **A számok feltevések**, de egymással és a [kapuk](01-kapuk-es-kill-criteria.md) és a [mérési
> rendszer](02-meresi-rendszer.md) küszöbeivel összhangban vannak. A cég, a szereplők és a
> felhő-kiterjesztés ütemterve a `PROJ_pm_all` Xyo-projektjéből jön.

A szakszavak magyarázata: [tudasbazis.md](../kutatas/tudasbazis.md).

---

## 4.1. A kiinduló helyzet

A Xyo Kft. (kb. 240 fő) 2026 nyarán lezárta a Cloud Pilotot: 50 munkatárs SharePointon és
OneDrive-on dolgozik, a kiterjesztés a maradék 190 főre három hullámban fut 2027. január 11. és
szeptember 30. között. A pilot értékelése szerint a csapatok **sokkal többet dokumentálnak a
SharePointon**, mint korábban. Ennek ára is van: a Service Desk egyre több „hol találom?” kérdést
kap, és a kollégák egymást kérdezik.

Kiss Réka (Service Desk vezető) 2026 októberében javasolja, hogy a cég próbáljon ki egy belső
tudásasszisztenst. Horváth Júlia ügyvezető azzal a feltétellel fogadja be az ötletet, hogy
**előbb derüljön ki olcsón, működik-e**, és csak utána költsenek a bevezetésre.

## 4.2. Keret (2026. december 1–18.)

Tóth Gergő projektmenedzser három hét alatt összeállítja a keretet.

**Baseline (T0, december 7–11.).** Tíz pilot-résztvevő tíz időmért keresési feladatot old meg az
asszisztens nélkül (MK-08). A feladatsort Kiss Réka állítja össze a Service Desk-jegyekből.

| Baseline-adat *(feltevés)* | Érték |
|---|---|
| Medián feladatidő (10 feladat × 10 fő) | **6 perc 30 mp** |
| Heti keresési alkalmak egy főre (kérdőív) | 7 |
| „Hol találom?” jegyek a Service Desken | havonta 85 |

**Üzleti eset** *(feltevés)*:

| Sikerkritérium | Célérték | Kártya |
|---|---|---|
| A medián feladatidő csökkenése | ≥ 30% (≤ 4 perc 33 mp) | MK-08 |
| Heti aktív felhasználók az élesítés utáni 8. héten | ≥ 50% | MK-07 |
| „Hol találom?” jegyek | −40% a teljes bevezetés után fél évvel | — |

**Haszonbecslés.** 240 fő × 7 keresés × 46 hét = **77 280 keresés évente**. 30%-os csökkenésnél
keresésenként 117 mp a megtakarítás, ez **kb. 2 500 óra évente**, ha mindenki használja; 50%-os
használatnál kb. 1 250 óra. A [P&L](../kutatas/tudasbazis.md#pl)-hatást Kovács Anita szándékosan
nem forintosítja: a felszabaduló idő a Service Desknél (kevesebb jegy) mérhető közvetlenül, a
többi becslés marad.

**Szakaszos költségkeret** *(feltevés)*:

| Keret | Összeg | Mikor szabadul fel |
|---|---|---|
| PoC-keret (kísérleti szakasz), ebből tartalék 900 000 Ft | **6 500 000 Ft** | G0 |
| Bevezetési keret (pilot + 3 hullám + képzés) | 9 800 000 Ft | **csak G1 go esetén** |
| Éves futási keret | 3 600 000 Ft/év → kb. **46 Ft/kérdés** a 77 280 kérdésre | G1 go esetén |

**Cél és kizárások** (projektalapító dokumentum, Horváth Júlia jóváhagyásával):

- *Cél:* a munkatársak a céges szabályzatokból, útmutatókból és projektdokumentumokból forrásmegjelöléssel
  kapjanak választ, a saját SharePoint-jogosultságuk szerint.
- *Kizárva:* egyéni HR-anyagok (teljesítményértékelések, bérek, fegyelmik), vezetői levelezés;
  **a rendszer nem támogat egyénekről szóló munkaügyi döntést** (AI Act III. melléklet 4. pont).

**AI Act-besorolás.** dr. Fekete Zsolt (DPO) és a cég jogásza szerint: nem magas kockázatú,
belső információkereső rendszer. A rendszert a Cloudia Solutions építi és a Xyo üzemelteti; a
szerepek ([provider és deployer](../kutatas/tudasbazis.md#provider-and-deployer)) a szerződésben
rögzítve. Az AI-jelzés a felületen ([Article 50](../kutatas/tudasbazis.md#article-50)) mindkét
esetben elfogadási feltétel.

**A kísérleti szakasz tárai:** a pilot négy SharePoint-tára — HR-szabályzatok (általános szabályzatok, nem
egyéni anyagok), IT-útmutatók, Beszerzés, Cloud Pilot projekttár —, összesen kb. 1 900 dokumentum.

**G1-küszöbök és kill criteria:** a [kapuk dokumentum](01-kapuk-es-kill-criteria.md) táblája szerint,
az irányító bizottság jóváhagyásával — **még a kísérleti szakasz előtt**.

## 4.3. G0 — hiánypótlással

**December 18., első G0.** Tíz feltételből kilenc teljesül. **A G0-4 (DPIA-döntés) nem**: az
adatleltár készítése közben Tóth Gergő észreveszi, hogy a Cloud Pilot projekttárában ott van a
pilot elégedettségi kérdőíveinek **névvel ellátott nyers exportja**. Ez nem tartozik a cél körébe,
de a tárban van, és a DPO addig nem ad állásfoglalást, amíg nem tisztázott, mi kerül a rendszerbe.

**Döntés: hiánypótlás.** Az adatleltár kiegészül egy kizárási szabállyal (a nyers kérdőív-exportok
kikerülnek, az összesítő riport bent marad), a DPO pedig egyszerűsített DPIA-t készít, mert a
rendszer munkavállalói adatokat tartalmazó dokumentumokat dolgoz fel új technológiával.

**2027. január 8., második G0: go.** A PoC-keret felszabadul, a kísérleti szakasz január 11-én indul.

> **Mit mutat ez a kapu?** Ha a kísérleti szakasz „párhuzamosan” elindult volna, a névvel ellátott kérdőívek
> bekerülnek az indexbe, mielőtt bárki döntött volna róluk. A hiánypótlás három hét csúszást
> okozott a tervezett indításhoz képest — és egy lehetséges adatvédelmi incidenst előzött meg.

## 4.4. Kísérleti szakasz (2027. január 11. – február 26., 7 hét)

A golden set gazdája Kiss Réka; a referenciaválaszokat Varga Eszter, Nagy Péter és Molnár Katalin
hagyja jóvá. A rendszert a Cloudia Solutions építi és méri. A mérések a golden set **v1.0**-s
verzióján futnak (40 elem), mellettük a 12 esetes jogosultsági készleten.

### Az eredmények iterációnként *(feltevés)*

| Mutató | Küszöb (zöld) | 0. iteráció | 1. | 2. | 3. |
|---|---|---|---|---|---|
| MK-01 Faithfulness | ≥ 0,90 | 0,78 | 0,84 | **0,92** | 0,92 |
| MK-02 Context recall | ≥ 0,85 | 0,66 | 0,81 | 0,81 | 0,84 |
| Context precision *(diagnosztika)* | — | 0,58 | 0,71 | 0,71 | 0,79 |
| MK-03 Correct refusal | ≥ 90% | 5/8 (62,5%) | 5/8 | 7/8 (87,5%) | **8/8 (100%)** |
| Téves elutasítás | ≤ 10% | 1/24 (4,2%) | 1/24 | 3/24 (12,5%) | 2/24 (8,3%) |
| MK-04 Permission leakage | 0 | 0/12 | 0/12 | 0/12 | 0/12 |
| MK-05 Latency p95 | ≤ 8 s | 11,2 s | 9,6 s | 9,8 s | **7,4 s** |
| MK-06 Költség / kérdés | ≤ 46 Ft | 52 Ft | 48 Ft | 49 Ft | **41 Ft** |

### 0. iteráció (január 11–15.) — a mérés építése

Elkészül a golden set v1.0: 24 megválaszolható, 8 elutasítandó és 8 nehéz kérdés, a jegyekből és
az átnézők gyűjtéséből. A Cloudia Solutions egy **egyszerű kiinduló beállítást** mér: alapértelmezett
darabolás, általános prompt. Ez a [baseline](../kutatas/tudasbazis.md#baseline) a kísérleti szakasz számára.

**Olvasat:** a recall alacsony (0,66), ezért a faithfulness (0,78) még nem értelmezhető jól — a
válasz egy része eleve rossz forrásra épül. **Az első hipotézis tehát a keresésről szól, nem a
promptról.**

### 1. iteráció (január 18–29.) — darabolás

*Hipotézis:* a szabályzatok táblázatai (értékhatárok, határidők) a darabolásnál szétesnek, ezért
a keresés nem találja őket. *Változtatás:* fejezet- és bekezdéshatár szerinti
[darabolás](../kutatas/tudasbazis.md#chunk), a táblázatok egyben maradnak.

**Eredmény:** a recall 0,66 → 0,81, a precision 0,58 → 0,71; a faithfulness is javul (0,84), mert
jobb forrásból válaszol. Esetszinten: 6 korábban sikertelen kérdés javult, egy sem romlott.

### 2. iteráció (február 1–12.) — „csak a forrásból”

*Hipotézis:* a modell a megtalált szövegen túl „kiegészít” — ez rontja a faithfulnesst és az
elutasítást. *Változtatás:* a promptban: csak a megtalált forrásból válaszoljon, jelölje meg, és ha
a forrás nem tartalmazza a választ, mondja ki.

**Eredmény:** a faithfulness 0,92 (zöld), a helyes elutasítás 7/8. **De** a téves elutasítás
1/24-ről 3/24-re nőtt (12,5%) — a rendszer olyankor is „nem talál forrást”, amikor van. **Ez a
párban olvasás haszna** (MK-03): az elutasítás javulása önmagában jónak látszott volna.

### 3. iteráció (február 15–26.) — elavult változatok és kevesebb találat

*Hipotézis A:* a recall maradék hibáinak egy része abból adódik, hogy egyes szabályzatoknak két
változata él (pl. régi és új utazási szabályzat), és a keresés a régit hozza. *Változtatás:* az
adatgazdák 37 elavult dokumentumot archiválnak, a keresés a legfrissebb érvényes változatot
részesíti előnyben.

*Hipotézis B:* a 3 téves elutasítás oka, hogy a sok, részben releváns találat között a modell
bizonytalan lesz. *Változtatás:* kevesebb, jobban rangsorolt találat kerül a válaszba (8 helyett
5).

A két változtatást **külön futtatással** mérik, hogy kiderüljön, melyik mit okoz; utána együtt.

**Eredmény:** a recall 0,84 (sárga, épp a küszöb alatt), a precision 0,79; a helyes elutasítás
8/8, a téves elutasítás 2/24 (8,3%); a válaszidő és a költség csökken (7,4 s, 41 Ft), mert
kevesebb szöveg megy a modellhez.

**A maradék recall-hibák:** a 24 megválaszolható kérdésből 3-nál a keresés nem találja a
választ. Kiss Réka esetszintű átnézése szerint **mindhárom a Beszerzés tár szkennelt PDF-jeire**
vonatkozik, amelyeknek nincs szövegrétegük — a keresés nem „látja” a tartalmukat.

> **Kis mintás figyelmeztetés** (a [mérési rendszer](02-meresi-rendszer.md) 2.3. pontja szerint):
> a 8 elutasítandó elemen a ≥ 90%-os küszöb gyakorlatilag 8/8-at jelent — egyetlen hiba sárgába
> visz. A tanulságot a termékág viszi tovább: a golden set elutasítandó csoportja 20 elemre bővül.
> A küszöböt a G1-en **nem** lazítják.

## 4.5. G1 — pivot, majd go

**Március 3., G1.** A bemenetek: a 3. iteráció mérési jelentése esetszintű listával, a
jogosultsági teszt, az éves költségbecslés (41 Ft × 77 280 kérdés ≈ 3,2 M Ft — a 3,6 M Ft-os
futási kereten belül), az iterációs napló és a kockázatnapló.

| Mutató | Szerep | Eredmény | Sáv |
|---|---|---|---|
| Permission leakage | kizáró | 0/12 | zöld |
| Faithfulness | kritikus | 0,92 | zöld |
| Context recall | kritikus | 0,84 | **sárga** |
| Correct refusal | kritikus | 8/8 (téves elutasítás 2/24) | zöld |
| Latency p95 | támogató | 7,4 s | zöld |
| Éves futási költség | támogató | ≈ 3,2 M Ft | zöld |

**Döntés a szabályok szerint:** a kizáró mutató zöld, **egy** kritikus mutató sárga, és a hiba
helye azonosított (a Beszerzés tár szkennelt PDF-jei). Ez **pivot**: egyszer, legfeljebb két hét.
A hipotézis: a 112 szkennelt PDF szövegfelismerése (OCR) után a keresés megtalálja a tartalmukat.

A pivot költségét (kb. 850 000 Ft) a PoC-keret tartalékából fedezik; Kovács Anita jóváhagyja. Az
irányító bizottság rögzíti: **ha a pivot után a recall nem zöld, a döntés no-go** (kill criterion 3).

**Pivot: március 4–17.** A Cloudia Solutions OCR-rel feldolgozza a 112 dokumentumot; Molnár Katalin
szúrópróbával ellenőrzi, hogy az értékhatár-táblázatok számai helyesek-e a felismert szövegben (két
hibát találnak, kézzel javítják). Utána teljes regressziós futás a golden set v1.0-n.

**Március 19., G1': go.**

| Mutató | 3. iteráció | Pivot után | Sáv |
|---|---|---|---|
| Context recall | 0,84 | **0,88** | zöld |
| Faithfulness | 0,92 | 0,91 | zöld |
| Correct refusal / téves | 8/8 · 2/24 | 8/8 · 2/24 | zöld |
| Permission leakage | 0/12 | 0/12 | zöld |
| Latency p95 | 7,4 s | 7,8 s | zöld |
| Költség / kérdés | 41 Ft | 42 Ft | zöld |

A faithfulness 0,01-es csökkenése esetszinten egyetlen válasz egyetlen állítása — a kis mintás
szabály szerint zaj, nem romlás; Kiss Réka az esetet átnézi és rendben találja. A kísérleti szakasz teljes
költsége **6,3 M Ft**, a 6,5 M Ft-os PoC-kereten belül. A **bevezetési keret (9,8 M Ft) és a
futási keret felszabadul.**

> **Mit mutat ez a kapu?** Egy „majdnem jó” eredménynél két rossz út kínálkozik: a küszöb
> lazítása („0,84 majdnem 0,85”) vagy egy újabb, cél nélküli iteráció. A pivot szabálya egyiket
> sem engedi: csak azonosított hibahellyel, egyszer, határidővel — és előre kimondott no-go-val, ha
> nem sikerül.

## 4.6. Kettéválás (2027. március 22-től)

### Termékág — Kiss Réka (product owner)

Kéthetes sprintek március 22-től. A backlog első elemei:

- válaszonkénti **„hasznos volt?”** jelzés (MK-07 mellé);
- **forrás-előnézet**: a megjelölt dokumentum részlete a válasz mellett, hogy a felhasználó
  ellenőrizhesse;
- a **golden set bővítése**: a zárásig 40-ről 120 elemre, az elutasítandó csoport 8-ról 20-ra (a
  kísérleti szakasz kis mintás tanulsága); minden élesben előjött hibából jelölt elem;
- heti automatikus regressziós futás (MK-01–03), havi teljes jogosultsági teszt (MK-04).

### Bevezetési ág — Tóth Gergő (projektmenedzser)

| Lépés | Kör | Tervezett | Tényleges | G2 |
|---|---|---|---|---|
| Pilot | a Cloud Pilot 50 fője | 2027. április 5. | április 5. | élesítés |
| 1. hullám | kb. 60 fő (a felhő-kiterjesztés 1. hulláma) | május 3. | május 3. | élesítés |
| 2. hullám | kb. 65 fő | július 5. | **július 19.** | **halasztás**, majd élesítés |
| 3. hullám | kb. 65 fő | október 4. | október 4. | élesítés |

Az asszisztens egy hullámot csak a felhő-kiterjesztés megfelelő hulláma **után** kap meg, amikor
annak SharePoint-tárai már élnek (G2-1). A 3. hullám ezért a kiterjesztés szeptember 30-i vége
utánra esik. 60 + 65 + 65 = 190 fő, a pilottal együtt 240.

Minden hullám előtt: AI literacy képzés (Varga Eszter), egyoldalas „mire figyelj” kártya (a válasz
hibás lehet, nézd meg a forrást, mit nem tud a rendszer), és a Service Desk felkészítése (Kiss Réka,
a PM ellenjegyzésével).

**A 2. hullám G2-halasztása (július 1.).** A hullámhoz tartozó Pénzügy tár indexelése után a
jogosultsági tesztkészlet (MK-04), amelyet Szabó Márk két új tesztfelhasználóval bővített, **egy
szivárgást** talál: egy almappán megszakadt a jogosultság-öröklődés, így egy általános jogú
tesztfelhasználó választ kapott egy csak a pénzügy számára látható táblázatból.

A beavatkozási szabály szerint a tárat azonnal kiveszik az indexből, dr. Fekete Zsolt értesítést
kap, Szabó Márk javítja az öröklődést. Az újraindexelés után a teszt 0 szivárgást mutat. A
halasztás két hét — a PM tűréshatárán belül, ezért ő dönt róla Nagy Péterrel. Élesítés: július 19.

> **Mit mutat ez a kapu?** A szivárgás oka nem az asszisztensben, hanem egy régi SharePoint-
> beállításban volt — de az asszisztens tette **láthatóvá és kereshetővé**. A G2 jogosultsági
> tesztje nélkül ez egy éles felhasználónál derült volna ki.

## 4.7. Az elutasított változáskérés (2027. június)

Az 1. hullám után egy osztályvezető a „hasznos volt?” visszajelzésben és a Service Desken azt
kéri, hogy az asszisztens **„foglalja össze a beosztottaim teljesítményét az éves értékelések
alapján”**, mert a félévi beszélgetésekre így gyorsabban készülhetne fel.

**A kérés útja** (a [kapuk dokumentum](01-kapuk-es-kill-criteria.md) 1.5. pontja szerint):

1. Kiss Réka (PO) felismeri, hogy a kérés **nem backlog-elem**: egy rögzített kizárást lépne át
   (G0-2), ezért továbbítja Tóth Gergőnek.
2. Tóth Gergő hatáselemzést kér Varga Esztertől (HR) és dr. Fekete Zsolttól (DPO). Az eredmény: a
   funkció egyének teljesítményének értékelését támogatná, ami az AI Act III. melléklet 4(b) pontja
   szerint **magas kockázatú** felhasználás — a szabályok 2027. december 2-tól alkalmazandók
   (kockázatkezelés, dokumentáció, emberi felügyelet, megfelelőségértékelés) — és új DPIA-t igényelne.
3. **Az irányító bizottság döntése: elutasítás ebben a projektben.** Ha az üzlet ilyen funkciót
   akar, az **új projekt** saját üzleti esettel, besorolással, DPIA-val és költségkerettel. Horváth
   Júlia úgy dönt, hogy most nem indítják; a vezetők a félévi beszélgetésekhez a meglévő
   HR-folyamatot használják.

A döntést az osztályvezető írásban, indoklással kapja meg. Varga Eszter a következő vezetői
értekezleten röviden elmondja, mire **nem** való az asszisztens.

> **Mit mutat ez az eset?** A HR-anyagok az indexben sincsenek, tehát a funkció technikailag sem
> működne. A döntés mégsem technikai, hanem **célról** szól: ha a kérést „csak” egy backlog-elemként
> kezelték volna (pl. „töltsük be az értékeléseket is”), a projekt észrevétlenül magas kockázatúvá
> vált volna. A scope-határ a keretnél marad — ez a hibrid modell egyik fő haszna.

## 4.8. T1-mérés és zárás

**Pilot T1 (május 3., a pilot élesítése után 4 héttel)** — ugyanaz a tíz feladat, ugyanaz a tíz fő:

| Mutató | T0 | T1 | Cél | Sáv |
|---|---|---|---|---|
| Medián feladatidő | 6 perc 30 mp | **3 perc 50 mp** (−41%) | ≥ 30% csökkenés | zöld |
| Hibás eredmény a feladatokban | 4 / 100 | 3 / 100 | ne nőjön | zöld |
| Heti aktív felhasználók, 8. hét (május 31.) | — | **58%** | ≥ 50% | zöld |

**Zárás: 2027. november 30.** A 3. hullám 8. hetes mérése után Tóth Gergő lezárja a projektet. A
termékágat Nagy Péter veszi át üzemeltetésre: felelős (Kiss Réka mint product owner), futási
keret, mérési ritmus (a mérési rendszer 2.7-es táblája szerint) és beavatkozási szabályok. A
„hol találom?” jegyek csökkenését és a teljes körű megtakarítást a zárás utáni haszonmérés követi
— a `PROJ_pm_all` hatodik fázisának mintájára.

## 4.9. Mit mutatott a példa?

| Kapu / esemény | Mit mutatott |
|---|---|
| **G0 hiánypótlás** | a névvel ellátott kérdőív-export csak az adatleltárban derült ki — ezért nem indulhat a kísérleti szakasz a G0 előtt |
| **0–1. iteráció** | alacsony recall mellett a faithfulness nem értelmezhető jól: előbb a keresést kell javítani |
| **2. iteráció** | az elutasítás javulása a téves elutasítás romlásával járt — a mutatókat párban kell olvasni |
| **3. iteráció** | két változtatás csak külön futtatással mérhető; a kis minta küszöbe 8/8-at jelent |
| **G1 pivot** | „majdnem jó” eredménynél se a küszöb lazítása, se a cél nélküli iteráció — azonosított hibahely, egy esély, kimondott no-go |
| **Szakaszos keret** | a bevezetésre csak a G1' után költöttek; egy no-go legfeljebb 6,5 M Ft lett volna |
| **G2-halasztás** | a jogosultsági teszt egy régi SharePoint-hibát talált meg, mielőtt éles felhasználó találta volna meg |
| **HR-változáskérés** | a scope-határ a célról szól, nem a technikáról — és a keretnél marad, nem a backlogban |
| **Kettéválás** | a bevezetési ág a felhő-kiterjesztéshez igazodott, a termékág saját ritmusban fejlődött; a kettőt a verzió- és a hullámdöntés kapcsolta össze |
