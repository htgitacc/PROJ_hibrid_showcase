# ADR 0002 — Működési modell: keret, kísérleti szakasz, kettéválás; a mérés gazdája a megrendelő

**Állapot:** elfogadva (a kutatás jóváhagyása után a koncepció része, 2026-11-05).

## Kontextus

A kutatás ([`kutatas/00-osszefoglalo.md`](../../kutatas/00-osszefoglalo.md)) szerint a hibrid
önmagában nem jobb; értéke abban van, hogy a projekt részei más-más bizonytalanságot kezelnek. Az
AI-projektek bukási okai részben tervezhetők (cél, jog, költség), részben csak méréssel dönthetők el
(megvalósíthatóság), részben a bevezetés után folyamatosak (használat, adatváltozás). Tibor döntései
(2026-11-05): az őszinte kiindulópont marad; a HR-kizárás éles scope-határ, és a példában egy
elutasított változáskérés mutatja be.

## Döntés

- **Három rész:** prediktív **keret** → G0 → időkeretes **kísérleti szakasz** → G1 PoC-kapu →
  **kettéválás** prediktív bevezetési ágra és agilis termékágra.
- **Szakaszos finanszírozás:** PoC-keret a G0-n, bevezetési és futási keret csak G1 go esetén.
- **A küszöbök és a kill criteria a mérés előtt rögzítettek** (G0-9); a G1-en nem módosíthatók. A
  pivot egyszer, legfeljebb két hétre, csak azonosított hibahellyel engedett; ami nem go és nem
  pivot, az no-go.
- **A mérés gazdája a megrendelő** (a golden set és a küszöbök a Xyóé), akkor is, ha a rendszert
  külső partner építi és méri — különben a megvalósító a saját munkáját értékelné.
- **A scope-határ a keretnél marad:** a kizárást vagy a besorolást érintő kérés nem backlog-elem,
  hanem elutasítás vagy új projekt.
- **Minden újrahasznosítható dokumentumhoz letölthető minta** (`koncepcio/sablonok/`).

## Következmények

- A Xyo-példa számai feltevések; a küszöbök példaértékként, *(feltevés)* jelöléssel szerepelnek.
- A bevezetési ág a `PROJ_pm_all` felhő-kiterjesztésének hullámaihoz kötött: ha az változik, a
  [Xyo-példát](../../koncepcio/04-xyo-pelda.md) igazítani kell.
- A felület (kapu-nézet, tudásbázis, mintatár, dokumentumok) erre a szerkezetre épül, és a tesztek a
  példa számainak összhangját őrzik (`tests/test_adatok.py`).
