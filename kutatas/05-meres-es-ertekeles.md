# 5. Mérés és értékelés egy RAG-asszisztensnél

> **Kérdés:** mivel és hogyan mérjük, hogy a tudásasszisztens „elég jó”-e — úgy, hogy a mérésből
> döntés (go/no-go) születhessen?
>
> **Rövid válasz:** egy **szakértő által átnézett tesztkészlettel** ([golden
> set](tudasbazis.md#golden-set)), amelyet minden változtatás után ugyanúgy lefuttatunk; a keresést
> és a válaszadást **külön mutatókkal** mérjük, mert másként romlanak el; a pontozást részben LLM
> végezheti, de **emberi szúrópróbával kalibrálva**. A szabványos RAG-mutatók mellé kell néhány
> **saját, üzleti és biztonsági mutató** (helyes elutasítás, jogosultság-szivárgás, költség,
> használat) — ezeket egyetlen eszköz sem adja készen.

A szakszavak magyarázata: [tudasbazis.md](tudasbazis.md). A fejezet a koncepció
**mérőszámkártyáinak** alapja.

---

## 5.1. A golden set: mi, mekkora, hogyan tartjuk karban

A Langfuse mérnöki útmutatója szerint (F-16) a golden set olyan **válogatott** tesztkészlet,
amelynek minden eleme egy bemenetet és — általában — egy **átnézett** helyes választ vagy kifejezett
megfelelési feltételt tartalmaz. „Golden” attól lesz, hogy **szakértő megerősítette**: „ez a
bizalom az egész értéke”.

**Mekkora legyen (F-16):**

| Cél | Jellemző méret |
|---|---|
| Kiindulás: a legfontosabb viselkedések | **20–50** átnézett elem — a durva visszaeséseket már elkapja |
| Egy konkrét hiba feltárása | ~10 elem |
| Teljes regressziós készlet, a valós használat eloszlásában | **100–1000** elem |
| Minden változtatásnál futó gyors kapu | a teljes készlet néhány tíz–néhány száz elemes részhalmaza |

A forrás két figyelmeztetése: „**100 változatos elem többet ér 1000 majdnem egyformánál**”, és „egy
könnyű esetekből álló készlet örökké 95%-ot ad, és semmit nem mond” — minden ismert hibatípusnak
(kétértelmű kérdés, többrészes kérés, rossz nyelvű bemenet, prompt-injection kísérlet) legyen
néhány eleme.

**Honnan jönnek az elemek (F-16):** elsőként **valós használatból** (a kérdés és a rendszer
válasza, amelyet szakértő javít), másodsorban importból és **szintetikus generálásból** — ez
utóbbit ugyanolyan szigorral kell átnézni, és a valós alapot csak kiegészítheti.

**Karbantartás (F-16):**

- minden élesben előjött hibából **jelölt** elem lesz, de csak szakértői átnézés után „golden”;
- a készlet **verziózott**: két mérés csak akkor vethető össze, ha ugyanazon a verzión futott;
- elavult elemet (megszűnt funkció, megváltozott szabályzat) **archiválunk**, nem törlünk;
  javasolt negyedéves átnézés a fél évnél régebbi elemekre;
- **[dataset drift](tudasbazis.md#dataset-drift)**: ha a tesztkészlet eredménye jó, de az éles
  visszajelzés romlik, a készlet már nem hasonlít a valós használatra.

**Mi következik a projektre:** a golden set a kísérleti szakasz **első hetének** terméke, és van
gazdája (szakterületi átnéző). Nélküle nincs mit iterálni és nincs miből dönteni a kapunál.

## 5.2. A négy szabványos RAG-mutató — és mit nem mérnek

A Ragas nyílt forrású értékelő könyvtár dokumentációja szerint (F-17):

| Mutató | Mit mér | Mi kell hozzá | Skála |
|---|---|---|---|
| **[Faithfulness](tudasbazis.md#faithfulness)** | a válasz állításai közül hány támasztható alá a **megtalált** szövegrészekkel | válasz + megtalált kontextus | 0–1, nagyobb jobb |
| **[Answer relevancy](tudasbazis.md#answer-relevancy)** | mennyire a kérdésre felel a válasz — **a tényszerű pontosságot nem méri** | kérdés + válasz | jellemzően 0–1 (nem garantált) |
| **[Context precision](tudasbazis.md#context-precision)** | a keresés a releváns részleteket rangsorolja-e előre | megtalált kontextus + referenciaválasz | 0–1 |
| **[Context recall](tudasbazis.md#context-recall)** | a helyes válaszhoz szükséges információból mennyit talált meg a keresés | megtalált kontextus + referenciaválasz | 0–1 |

**Hogyan olvasd együtt — saját értelmezés, a fenti definíciókból:**

| Ha… | akkor a hiba valószínűleg… | ott javíts |
|---|---|---|
| a context recall alacsony | a **keresésben** van: a szükséges részlet nincs a találatok közt | dokumentum-előkészítés, darabolás, keresési beállítás |
| a recall jó, de a precision alacsony | a keresés **sok zajt** hoz, a lényeg hátul van | rangsorolás, kevesebb találat |
| a recall jó, de a faithfulness alacsony | a **válaszadásban** van: a modell a megtalált szövegen túl „kiegészít” | prompt (pl. „csak a forrásból válaszolj”) |
| a faithfulness jó, de a relevancy alacsony | a válasz igaz, de **nem arra felel**, amit kérdeztek | prompt, kérdés-értelmezés |

**A legfontosabb korlát:** a faithfulness csak azt méri, hogy a válasz a **megtalált** szöveghez
hű-e — ha a keresés rossz dokumentumot hozott, a válasz lehet hű és **mégis hibás**. Ezért a
mutatókat együtt kell nézni, és a golden set referenciaválaszaival is össze kell vetni.

## 5.3. Ki pontoz? LLM-as-a-judge és emberi értékelés

A faithfulness és a relevancy számításához egy LLM bontja állításokra és ítéli meg a választ: ez
az **[LLM-as-a-judge](tudasbazis.md#llm-as-a-judge)** módszer. Egy NeurIPS 2023-as tanulmány
szerint (F-18) erős LLM-bírák **több mint 80%-ban** egyeztek az emberi preferenciákkal — ugyanannyira,
amennyire az emberek egymással —, de a szerzők **torzításokat** is kimutattak: a bíró kedvezhet az
elsőként bemutatott válasznak (*position bias*), a hosszabb válasznak (*verbosity bias*) és a saját
maga által írt válasznak (*self-enhancement bias*), és korlátozott a következtetési képessége.

**Mi következik a projektre:**

- az LLM-bíró **olcsóvá teszi** a sok esetes, minden változtatás utáni mérést;
- de a bírót **kalibrálni kell**: a Langfuse útmutatója szerint mielőtt egy összesített számban
  megbízunk, néhány soron ellenőrizni kell, hogy a bíró ítélete egyezik-e a válasz tényleges
  minőségével (F-16) — ez a **[human evaluation](tudasbazis.md#human-evaluation)** szerepe;
- a golden set referenciaválaszait **ember** (szakterületi átnéző) hagyja jóvá, nem a bíró.

## 5.4. Amit a szabványos mutatók nem fednek le

A fenti négy mutató a válasz minőségét méri. A projekt döntéseihez — a [02](02-miert-buknak-el-az-ai-projektek.md)
bukási okai és a [04](04-szabalyozas.md) kötelezettségei alapján — további mutatók kellenek. Ezek
**saját tervezési döntések**, nem forrásból átvett szabványok:

| Mutató | Miért kell | Melyik okhoz / kötelezettséghez |
|---|---|---|
| **[Correct refusal rate](tudasbazis.md#correct-refusal-rate)** — helyes „nem tudom” | ha a forrás nem tartalmazza a választ, a rendszer ne találjon ki egyet | megbízhatóság; a faithfulness ezt nem méri, ha nincs találat |
| **[Permission leakage](tudasbazis.md#permission-leakage)** — jogosultság-szivárgás | a felhasználó ne kapjon választ olyan dokumentumból, amelyet a SharePointban nem láthat | GDPR, responsible AI (F-15, F-05); **zéró tolerancia** |
| **[Latency](tudasbazis.md#latency)** (p95) | a lassú válasz miatt a használat elhal | adopció, learning gap (F-04) |
| **Cost per query** — kérdésenkénti költség | a PoC-ban olcsó, élesben a használattal nő | TCO (F-05) |
| **Weekly active users** — heti aktív felhasználók | a bevezetés sikerének legegyszerűbb jele | adopció, változáskezelés (F-05) |
| **Time saved** — megtakarított idő | az üzleti eset haszonoldala | P&L-hatás (F-04); csak felméréssel vagy mintavétellel mérhető |

## 5.5. A méréstől a döntésig

A mérés akkor ér valamit, ha **döntést** vált ki. Ehhez minden mutatónál előre rögzíteni kell
(a forrásokból és a fenti szerkezetből levezetve):

- **baseline**: mihez képest mérünk (az előző verzió, vagy a mai gyakorlat, pl. „megkérdezem a
  kollégát”) — a Langfuse szerint a változásokat mindig egy kijelölt alapváltozathoz képest, **ugyanazon
  a készletverzión** kell olvasni (F-16);
- **küszöbök**: zöld / sárga / piros sáv és a go/no-go határ — ezek **üzleti döntések**, az üzleti
  esetben rögzítve; a koncepció példaértékei feltevésként lesznek jelölve;
- **esetenkénti olvasás**: egy kis összesített változás mögött nagy, egymást kioltó elemszintű
  változások lehetnek — ez viselkedésváltozás, nem „semmi” (F-16);
- **követés és beavatkozás**: milyen ritmusban mérünk élesben, és mi indít újra munkát (pl. egy
  jogosultság-szivárgás azonnal; két egymást követő sárga mérés a következő iterációban).

Ezek a pontok adják a koncepcióban a **mérőszámkártya** szerkezetét: mit mér és miért · a
kiválasztás szempontjai és korlátai · hol és mikor · ki és mivel · kiértékelés · mi számít jónak ·
hosszú távú követés · beavatkozási feltétel.

---

## Összegzés

| Állítás | Bizonyíték | Erősség |
|---|---|---|
| A golden set értéke a szakértői átnézés; 20–50 elemmel indul, 100–1000-re nő | F-16 | C |
| A változatosság fontosabb az elemszámnál; a könnyű készlet semmit nem mond | F-16 | C |
| A keresés és a válaszadás külön mutatókkal mérhető (recall, precision, faithfulness, relevancy) | F-17 | C |
| Az answer relevancy nem méri a tényszerű pontosságot | F-17 | C |
| Az LLM-bíró 80% felett egyezik az emberekkel, de torzításai vannak | F-18 | A |
| A szabványos mutatók mellé saját üzleti és biztonsági mutatók kellenek | saját tervezés | — |

**Ami nincs benne:** statisztikai szignifikancia és konfidenciaintervallum kis mintán (a
koncepcióban egyszerű szabállyal kezeljük), online A/B-tesztelés, és a prompt-injection elleni
biztonsági tesztelés részletei.
