# 3. Szerepek

> **Mit ad ez a dokumentum?** Ki mit csinál a keretben, a kísérleti szakaszban és a két ágban, ki dönt a
> kapuknál, és hol húzódik a projektmenedzser és a termékfelelős határa a kettéválás után. A
> szereplők a `PROJ_pm_all` Xyo-csapatából jönnek — ugyanaz a cég, egy új projekt.
>
> **A hibrid legkényesebb szerephatára** a PM és a product owner között van: a PM a keretet és a
> bevezetési ágat vezeti, a product owner a termékágat. Ha ez nincs kimondva, a két ág egymás
> prioritásait írja felül.

A szakszavak magyarázata: [tudasbazis.md](../kutatas/tudasbazis.md).

---

## 3.1. Szerepek és szereplők

| Szerep | Szereplő (Xyo) | Fő felelőssége | Melyik részben |
|---|---|---|---|
| **Irányító bizottság elnöke** | Horváth Júlia, ügyvezető | G0, G1 döntés; a cél és a kizárások jóváhagyása; változáskérések | keret, kapuk |
| **Szponzor** | Kovács Anita, gazdasági igazgató | üzleti eset; a PoC-keret és a bevezetési keret; a haszon gazdája | keret, G1 |
| **Projektmenedzser** | Tóth Gergő | a keret munkája, a kapuk előkészítése, a bevezetési ág ütemterve, kockázatok, függőség a felhő-kiterjesztéssel | keret, bevezetési ág |
| **Product owner** | Kiss Réka, Service Desk vezető | a golden set gazdája már a kísérleti szakaszban; a G1 után a termékág backlogja és sprintcéljai | kísérleti szakasz, termékág |
| **Szakterületi átnézők** | Varga Eszter (HR-szabályzatok), Nagy Péter (IT-útmutatók), Molnár Katalin (beszerzés) | a golden set referenciaválaszainak jóváhagyása; emberi szúrópróba | kísérleti szakasz, termékág |
| **Adatvédelmi tisztviselő** | dr. Fekete Zsolt | AI Act-besorolás (jogásszal), DPIA-döntés, jogosultsági eredmények, incidensek | keret, G1, G2 |
| **IT szakmai vezető** | Nagy Péter | jogosultsági elv, architektúra, üzemeltetésbe vétel, válaszidő-riport | keret, G2, zárás |
| **M365 / Entra ID rendszergazda** | Szabó Márk | tesztfelhasználók, a SharePoint-jogosultságok átvételének ellenőrzése | kísérleti szakasz, G2 |
| **Megvalósító partner** | Cloudia Solutions Kft. | a RAG-rendszer építése és hangolása, a mérések futtatása, költségbecslés | kísérleti szakasz, termékág |
| **Beszerzés** | Molnár Katalin | szolgáltató-kiválasztás, PoC- és üzemeltetési szerződés | keret |
| **Pénzügyi kontroller** | Balogh Tamás | költségkövetés, futási díj havi ellenőrzése | keret, termékág |
| **HR** | Varga Eszter | AI literacy képzés a bevezetési ágban; a HR-kizárás tartalmi gazdája | keret, bevezetési ág |

**Miért külső partner építi?** Az MIT-jelentés szerint a külső partnerrel épített pilotok kétszer
akkora eséllyel jutottak teljes bevezetésig, mint a belső fejlesztésűek (F-04, C szint). A Xyo
már ismeri a Cloudia Solutionst a Cloud Pilotból. **A mérés gazdája viszont a Xyo marad:** a
golden setet és a küszöböket nem a megvalósító állítja össze, mert akkor a saját munkáját
mérné.

**Miért Kiss Réka a product owner?** A Service Desk látja, mit kérdeznek a kollégák — a golden
set első kérdései a jegyekből jönnek, és a bevezetés után a hibabejelentések is hozzá futnak be.
Így a kísérleti szakasz tanulsága és a termékág backlogja egy kézben marad. **Kockázat:** a G2-5 feltételt
(Service Desk felkészültsége) is ő igazolja; ezt a PM ellenjegyzi.

## 3.2. Ki dönt, ki felel — a kapukra és a fő termékekre

**R** = elvégzi · **A** = jóváhagyja, felel érte · **C** = véleményezi · **I** = tájékoztatják

| | Horváth J. | Kovács A. | Tóth G. (PM) | Kiss R. (PO) | Átnézők | DPO | Nagy P. | Cloudia |
|---|---|---|---|---|---|---|---|---|
| Üzleti eset, baseline | C | **A** | R | C | | | C | |
| Cél és kizárások (HR-kizárás) | **A** | C | R | C | C (Varga E.) | C | | |
| AI Act-besorolás, DPIA-döntés | I | I | C | | | **A/R** | C | C |
| Adatleltár, kizárási szabályok | | | **A/R** | C | C | C | C | |
| G1-küszöbök, kill criteria | **A** | C | R | C | | C | C | C |
| **G0** | **A** | C | R | I | | C | C | I |
| Golden set | | | I | **A** | R | | | C |
| Iterációk a kísérleti szakaszban | I | I | C | C | C | | | **R** |
| Mérési jelentés | I | I | C | **A** | C | | | R |
| **G1** | **A** | **A** (bevezetési keret) | R | C | | C | C | C |
| Bevezetési ütemterv, hullámok | I | I | **A/R** | C | | | C | |
| **G2** (hullámonként) | I | | **A** | C | | C | **A** | C |
| Termékág backlog, sprintcélok | | | C | **A/R** | C | | | R |
| Változáskérés a keretnek | **A** | C | R | R (kezdeményez) | | C | | |
| Üzemeltetésbe adás (zárás) | I | C | R | C | | | **A** | R |

## 3.3. A PM és a product owner határa a kettéválás után

| Kérdés | Ki dönt | Indok |
|---|---|---|
| Melyik hullám mikor kapja meg az asszisztenst? | **PM** (G2, Nagy Péterrel) | ütemterv, külső függőség a felhő-kiterjesztéssel |
| Melyik termékverzió kerül a következő hullámba? | **PM**, a PO javaslatára | egy hullám közben nincs verziócsere, csak hibajavítás |
| Mi kerül a következő sprintbe? | **PO** | a termékág backlogja az övé |
| Egy hibajavítás sürgős-e egy hullám miatt? | **PO**, a PM kérésére | a PM kérhet, a sorrendet a PO állítja |
| Átlépi-e egy kérés a keret határait? | **PM** vizsgálja, **irányító bizottság** dönt | a scope-határ a keretnél marad (lásd [kapuk](01-kapuk-es-kill-criteria.md)) |
| Mikor ér véget a projekt? | **PM**, az irányító bizottság jóváhagyásával | a termékág nem ér véget — üzemeltetésbe kerül |

**Tipikus hiba:** a PM a bevezetési határidő miatt „belenyúl” a sprintbe, vagy a PO egy fontosnak
érzett funkció miatt verziót cserél egy futó hullám közben. Mindkettő a másik ág tervezhetőségét
rontja. A fenti tábla ezt a két esetet zárja ki.
