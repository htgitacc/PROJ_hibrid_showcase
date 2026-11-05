# 1. Kapuk és leállítási feltételek

> **Mit ad ez a dokumentum?** A modell döntési pontjait: mi a bemenetük, ki dönt, milyen
> kimenetek lehetségesek, és milyen szabályok szerint. A kapuk kötik össze a prediktív és a
> kísérleti munkát: **a keret a kapukon keresztül irányítja a kísérleti szakaszt**, nem a napi munkán át.
>
> **A legfontosabb szabály:** a küszöbértékeket és a leállítási feltételeket ([kill
> criteria](../kutatas/tudasbazis.md#kill-criteria)) **a mérés előtt** rögzítjük, és a kapunál már
> nem módosíthatók. Ha a kapunál derül ki, hogy „a 0,9 túl szigorú volt”, az nem a küszöb
> lazítását jelenti, hanem egy dokumentált tanulságot.

A szakszavak magyarázata: [tudasbazis.md](../kutatas/tudasbazis.md). A kapudöntés letölthető
mintája: [`sablonok/`](sablonok/) (a 2. fázis végén készül).

---

## 1.1. A kapuk áttekintése

| Kapu | Hol | Kérdés | Döntéshozó (Xyo) | Lehetséges kimenetek |
|---|---|---|---|---|
| **G0** | a keret végén | Indulhat-e a kísérleti szakasz valós adattal? | irányító bizottság (Horváth Júlia), előterjesztő a PM (Tóth Gergő) | **go** · **hiánypótlás** · **leállítás** |
| **G1 — PoC-kapu** | a kísérleti szakasz végén | Megoldható-e a feladat a kért minőségben, észszerű költséggel? | irányító bizottság, a szponzor (Kovács Anita) jóváhagyásával a bevezetési keretre | **go** · **pivot** (egyszer) · **no-go** |
| **G2** | minden bevezetési hullám előtt | Kaphatja-e ez a hullám az asszisztenst? | PM (Tóth Gergő) és IT (Nagy Péter), tűréshatáron belül | **élesítés** · **halasztás** |
| **Változáskérés** | bármikor | Belefér-e a kérés a keretbe? | a hatástól függően: product owner, irányító bizottság, vagy új projekt | **backlog** · **jóváhagyott változás** · **elutasítás / új projekt** |

Minden kapudöntés írásos, a bemeneteket és az indoklást rögzíti — ez a `PROJ_pm_all`
fáziskapuinak mintája.

## 1.2. G0 — Indulhat-e a kísérleti szakasz?

**Miért kell:** a kísérleti szakasz valós céges dokumentumokkal dolgozik. A [04-es kutatás](../kutatas/04-szabalyozas.md)
szerint a DPIA kérdését **az adatkezelés előtt** el kell dönteni, és a scope-kizárást írásban kell
rögzíteni. A G0 ezt kényszeríti ki.

**Belépési feltételek** — mindnek teljesülnie kell:

| # | Feltétel | Bizonyíték | Felelős (Xyo) |
|---|---|---|---|
| G0-1 | Üzleti eset jóváhagyva: mérhető sikerkritériumok, [baseline](../kutatas/tudasbazis.md#baseline)-mérés terve | aláírt üzleti eset | Kovács Anita (szponzor) |
| G0-2 | Cél és kizárások rögzítve, köztük: **nem támogat egyénekről szóló munkaügyi döntést** | projektalapító dokumentum | Horváth Júlia |
| G0-3 | [AI Act](../kutatas/tudasbazis.md#ai-act)-besorolás: nem magas kockázatú; [provider vagy deployer](../kutatas/tudasbazis.md#provider-and-deployer) | besorolási lap | dr. Fekete Zsolt (DPO) + jogász |
| G0-4 | [DPIA](../kutatas/tudasbazis.md#dpia)-döntés: kell-e, és ha igen, elkészült-e a kísérleti szakasz adatkörére | DPO-állásfoglalás | dr. Fekete Zsolt |
| G0-5 | Adatleltár a kísérleti szakasz tárairól, **kizárási szabályokkal** (egyéni HR-anyagok ki) | adatleltár | Tóth Gergő + adatgazdák |
| G0-6 | Jogosultsági elv: az asszisztens **csak azt** használhatja, amit a kérdező felhasználó a SharePointban lát | architektúra-döntés | Nagy Péter |
| G0-7 | Szolgáltató kiválasztva, PoC-szerződés (adatkezelés helye, futási díj, adatfelhasználás) | szerződés | Molnár Katalin |
| G0-8 | [Golden set](../kutatas/tudasbazis.md#golden-set)-gazda és szakterületi átnézők kijelölve, idejük lekötve | erőforrásterv | Tóth Gergő |
| G0-9 | **G1-küszöbök és kill criteria jóváhagyva** (1.3) | mérési terv | irányító bizottság |
| G0-10 | PoC-keret jóváhagyva (csak a kísérleti szakaszra, a bevezetésre nem) | költségterv | Kovács Anita, Balogh Tamás |

**Kimenetek:**

- **go** — minden feltétel teljesült; a kísérleti szakasz elindulhat, a PoC-keret felszabadul;
- **hiánypótlás** — egy vagy több feltétel hiányzik, de pótolható; új G0-időpont;
- **leállítás** — a keret munkája során kiderült, hogy a projekt nem indokolt (pl. a DPIA
  elfogadhatatlan kockázatot mutat, vagy az üzleti eset nem áll meg).

**Tipikus hiba:** a kísérleti szakaszt „párhuzamosan” elindítani, amíg a G0 feltételei készülnek, „hogy ne
veszítsünk időt”. Ilyenkor valós adat kerül a rendszerbe DPIA-döntés és kizárási szabály nélkül —
pontosan az, amit a G0 meg akar előzni. Ami a G0 előtt indulhat: a golden set **kérdéseinek**
gyűjtése (adat nélkül) és a szolgáltatók szintetikus adaton végzett próbája.

## 1.3. G1 — a PoC-kapu

**Miért kell:** ez a modell szíve. Itt dől el **méréssel**, hogy a feladat megoldható-e. A
[02-es kutatás](../kutatas/02-miert-buknak-el-az-ai-projektek.md) szerint a projektek jelentős része
a PoC után leáll — a cél, hogy ez a döntés **időben, olcsón és számok alapján** szülessen.

**Bemenetek:**

1. **mérési jelentés**: a golden set verziója, mutatónként az eredmény a baseline-hoz és a
   küszöbökhöz képest, és az **esetenkénti** lista a hibás esetekről (lásd [05](../kutatas/05-meres-es-ertekeles.md));
2. **jogosultsági teszt** eredménye (célzott tesztfelhasználókkal);
3. **költségbecslés** éles használatra ([TCO](../kutatas/tudasbazis.md#tco): futási díj a várható
   kérdésszámmal, üzemeltetés, továbbfejlesztés);
4. **iterációs napló**: milyen hipotéziseket próbáltunk, mi mozdította a mérést, mi nem;
5. frissített **kockázatnapló**.

**Mutatók és sávok — példaértékek, feltevésként.** A [05-ös kutatás](../kutatas/05-meres-es-ertekeles.md)
szerint nincs szakmai szabvány a küszöbökre: ezek üzleti döntések. Az alábbi számok a Xyo-példa
**feltevései**; a valós projektben az üzleti eset rögzíti őket a G0-n.

| Mutató | Szerepe a kapun | Zöld | Sárga | Piros |
|---|---|---|---|---|
| [Permission leakage](../kutatas/tudasbazis.md#permission-leakage) | **kizáró** | 0 | — | ≥ 1 |
| [Faithfulness](../kutatas/tudasbazis.md#faithfulness) | kritikus | ≥ 0,90 | 0,80–0,89 | < 0,80 |
| [Context recall](../kutatas/tudasbazis.md#context-recall) | kritikus | ≥ 0,85 | 0,70–0,84 | < 0,70 |
| [Correct refusal rate](../kutatas/tudasbazis.md#correct-refusal-rate) | kritikus | ≥ 90% | 80–89% | < 80% |
| [Latency](../kutatas/tudasbazis.md#latency) p95 | támogató | ≤ 8 s | 8–15 s | > 15 s |
| Becsült éves futási költség | támogató | a keretben | a keret 100–120%-a | > 120% |
| [Answer relevancy](../kutatas/tudasbazis.md#answer-relevancy) | **csak diagnosztika** | — | — | — |

Az answer relevancy szándékosan nem kapukritérium: a pontosságot nem méri, ezért döntést nem
alapozunk rá ([tudásbázis](../kutatas/tudasbazis.md#answer-relevancy)).

**Döntési szabályok:**

| Kimenet | Mikor |
|---|---|
| **go** | a kizáró mutató zöld, **minden kritikus mutató zöld**, a támogatók legalább sárgák |
| **pivot** — legfeljebb egyszer, legfeljebb 2 hét | a kizáró mutató zöld; **legfeljebb egy** kritikus mutató sárga; és a hiba **helye azonosított** (pl. alacsony recall → a keresésben), konkrét hipotézissel |
| **no-go** | bármelyik kill criterion teljesül (lent) — **és minden más eset**, amely nem go és nem pivot (pl. két kritikus mutató sárga) |

A **támogató mutatók** (latency, költség) piros értéke go-t nem enged, de önmagában nem kill: ha a hiba
helye azonosított, pivot lehet; ha nem, no-go. Kivétel a 4. kill criterion (piros költség olcsóbb
változat nélkül).

**Kill criteria** — ha bármelyik teljesül, a döntés no-go, vita nélkül:

1. **jogosultság-szivárgás** a végső mérésben, amely nem javítható a jogosultsági elv (G0-6)
   megváltoztatása nélkül. A G1 a végső mérés alapján dönt, ezért **bármely mért szivárgás no-go**
   (pivot csak zöld kizáró mutatónál van); a szivárgás javítása után új végső mérés kell;
2. **bármelyik kritikus mutató piros** a végső mérésben;
3. a **pivot után** is van nem zöld kritikus mutató;
4. a **becsült éves futási költség** meghaladja a keret 120%-át, és nincs olcsóbb változat, amely
   a kritikus mutatókat tartja;
5. a context recall tartósan sárga vagy piros, és az iterációs napló szerint az ok az **adat
   minősége** (hiányzó, elavult, ellentmondó dokumentumok) — ez nem a kísérleti szakasz, hanem egy
   adatrendezési projekt feladata.

**Mit jelent a no-go?** Nem kudarcot. A no-go-jelentés rögzíti, mit tanultunk (melyik mutató,
miért), mennyibe került (csak a PoC-keret), és mi lenne a feltétele egy későbbi újrapróbálásnak
(pl. adatrendezés). A golden set és a mérési eszközök megmaradnak.

**Tipikus hibák:**

- a küszöböt a kapunál lazítani, mert „majdnem elértük” — ezt a „mérés előtt rögzítjük” szabály
  zárja ki;
- „még egy iteráció” kérése pivot-indoklás nélkül — a pivot csak azonosított hibahellyel és
  hipotézissel jár, és csak egyszer;
- a demó benyomására dönteni a mérési jelentés helyett — a kapunál számok és esetek vannak, nem
  bemutató.

## 1.4. G2 — hullámonkénti élesítési kapu

**Miért kell:** a bevezetési ág a `PROJ_pm_all` felhő-kiterjesztésének hullámait követi. Egy hullám
csak akkor kaphatja meg az asszisztenst, ha a feltételei teljesülnek — különben a felhasználók egy
rossz első élményből ítélnek.

| # | Feltétel |
|---|---|
| G2-1 | a hullám SharePoint-tárai élnek, a jogosultságaik a kiterjesztési projekt szerint beállítva |
| G2-2 | a hullám tárainak indexelése után a **jogosultsági regressziós teszt** zöld (leakage = 0) |
| G2-3 | a rögzített termékverzió regressziós mérése zöld a teljes golden seten |
| G2-4 | a képzés ([AI literacy](../kutatas/tudasbazis.md#ai-literacy)) megtartva, az AI-jelzés a felületen él |
| G2-5 | a Service Desk (Kiss Réka) felkészült: hibabejelentési út, ismert hibák listája |
| G2-6 | az előző hullám mutatói (adopció, hibajegyek, elégedettség) nem pirosak |

**Kimenetek:** **élesítés**, vagy **halasztás** a következő lehetséges időpontra. A PM a
tűréshatáron belül (pl. legfeljebb két hét halasztás) maga dönt; afelett az irányító bizottság.

## 1.5. A változáskérés útja

A termékágba folyamatosan érkeznek kérések. A kérdés mindig az, hogy a kérés **a keret határain
belül** van-e:

| Ha a kérés… | akkor | döntéshozó |
|---|---|---|
| a rögzített célon és kizárásokon belül van, nem érinti a keretköltséget és az ütemtervet | **backlog-elem** a termékágban | product owner |
| a költséget, az ütemtervet vagy egy rögzített sikerkritériumot érinti | **változáskérés** a keretnek, hatáselemzéssel | irányító bizottság |
| egy rögzített **kizárást** lépne át, vagy **megváltoztatná az AI Act-besorolást** | **elutasítás** ebben a projektben; ha az üzlet akarja, **új projekt** saját kerettel, besorolással és DPIA-val | irányító bizottság, DPO |

**Példa a Xyo-projektből** (a [kitöltött példa](04-xyo-pelda.md) részletezi): egy vezető azt kéri,
hogy az asszisztens „foglalja össze egy munkatárs teljesítményét az értékelések alapján”. Ez a
III. melléklet 4(b) pontja szerint magas kockázatú felhasználás lenne ([04](../kutatas/04-szabalyozas.md)),
és a G0-2 kizárásába ütközik — ezért **nem backlog-elem és nem változáskérés, hanem elutasítás**,
új projekt lehetőségével.

## 1.6. Élesítés után: beavatkozási szabályok

A kapuk a projekt végével nem szűnnek meg teljesen: az üzemeltetésbe adott termékágnak is vannak
**beavatkozási szabályai** — ezek a mérőszámkártyák „beavatkozási feltétel” mezőiben élnek (lásd
a [mérési rendszert](02-meresi-rendszer.md)). A két legfontosabb:

- **egyetlen jogosultság-szivárgás** → az érintett tár azonnali kivétele az indexből, incidenskezelés,
  DPO értesítése;
- **két egymást követő sárga mérés** egy kritikus mutatón → a következő sprint célja ennek
  javítása, a product owner döntése szerint.
