# ADR 0001 — Harmadik modell: hibrid PM egy vállalati RAG-projekten (Xyo Tudásasszisztens), kicsi méretben

**Állapot:** elfogadva (Tibor jóváhagyta, 2026-11-05).

## Kontextus

A `smpm` portfólióban két modell él: a `PROJ_pm_all` (prediktív, waterfall) és a `PROJ_sm_all`
(agilis, AI-ügynökös Scrum). Tibor egy harmadik, IT/AI témájú modellt szeretne, amely mindkét
megközelítést használja, és amelyből tanulni lehet. Az előzetes kutatás (2026-11-05) szerint:

- a hibrid megközelítés az IT-ban már fősodor (PMI Pulse 2024), a PMBOK 8 eleve szabásra épül;
- az AI-projektek többsége nem technikai okból bukik el (homályos sikerkritérium, adat,
  governance, adopció) — ezek prediktív és agilis kérdések egyszerre;
- az AI-ban új bizonytalanság is van: megoldható-e a feladat a kért minőségben; erre a mérés
  (értékelőkészlet, mérőszám-kapu) a válasz — ezt egyik meglévő modell sem mutatja;
- a PMI saját AI-módszertana (CPMAI) iteratív, adatközpontú, és nem waterfall, nem Scrum.

A részletek és források a `kutatas/` mappában kerülnek rögzítésre.

## Döntés

- **Téma:** vállalati RAG tudásasszisztens a Xyo Kft. SharePoint-tárára — a `PROJ_pm_all`
  Cloud Pilotjának folytatása, így a három modell egy cég történetét meséli el.
- **Szerkezet:** egy projekt, amely szétválik:
  1. prediktív indítás (üzleti eset, adatleltár, DPIA, AI Act-besorolás, beszerzés);
  2. időkeretes kísérleti szakasz, az első héten elkészülő értékelőkészlettel;
  3. go/no-go kapu a PoC végén, mérőszám-küszöbökkel — a no-go valós kimenet;
  4. kettéválás: prediktív bevezetés + agilis termékfolyamat.
- **Méret:** szándékosan kicsi (15–20 dokumentum, egy jellegzetes interaktív nézet), nem a
  másik kettő mérete.
- **Minden újrahasznosítható dokumentumhoz letölthető üres minta** tartozik, kitöltési
  útmutatóval; a mérőszámkártyák egységes szerkezetet követnek.
- **Mini tudásbázis:** a szakszavak angolul maradnak, magyarázattal és olvasási útmutatóval.
- **Elvetett:** ML-előrejelzés (hiteles adatot nehéz kitalálni), automatikus marketing (gyenge
  governance-tét), harmadik app nélküli összehasonlító oldal (az AI-specifikus tanulság hiányzik).

## Következmények

- Új repó: `PROJ_hibrid`. A port, a `/hibrid/` útvonal és a harmadik kártya a `PROJ_smpm`-ben
  később, Tibor kezével.
- A Xyo-adatokat a `PROJ_pm_all`-ból vesszük át; ha ott változnak, itt is igazítani kell.
- Rövid, egyenként pusholt iterációkban dolgozunk; a `docs/HANDOFF.md` minden commitban friss.
