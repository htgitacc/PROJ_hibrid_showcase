# Adatleltár — [projekt neve]

> **Használat.** Minden adatforrásról (SharePoint-tár, mappa, adatbázis), amely a rendszerbe
> kerülhet, egy sor. A leltár a DPIA és az AI Act-besorolás alapja (G0-4, G0-5), és minden új
> forrás előtt bővül (G2-1). A leltár akkor jó, ha minden sorról eldönthető: **be**, **ki**, vagy
> **tisztítás után be** — és mindhez van felelős.
>
> **A leggyakoribb meglepetés** a „vegyes” tár: egy alapvetően rendben lévő tárban egy mappa,
> amelyben személyes vagy kizárt adat van. A Xyo-példában ez a G0-n derült ki ([4.3.](../04-xyo-pelda.md)).

---

**Verzió:** [1.0]\
**Állapot:** [tervezet / a DPO átnézte / jóváhagyva]\
**Készítette:** [név]\
**Átnézte (DPO):** [név, dátum]

## 1. Források

| # | Forrás (tár / mappa) | Adatgazda | Tartalom | Dokumentumok száma | Frissesség | Jogosultsági modell | Személyes adat? | Döntés |
|---|---|---|---|---|---|---|---|---|
| D-01 | [SharePoint-tár neve] | [név] | [mit tartalmaz] | [db] | [legutóbbi módosítás; elavult változatok?] | [ki láthatja; öröklődés rendben?] | [nincs / nevek, elérhetőségek / különleges adat] | [be / ki / tisztítás után be] |
| [...] | | | | | | | | |

## 2. Kizárási szabályok

| # | Szabály | Indok | Hogyan ellenőrizzük |
|---|---|---|---|
| X-01 | [mi nem kerülhet be] | [cél, jog, kockázat] | [teszt, szúrópróba, mappaszabály] |
| [...] | | | |

## 3. Tisztítási teendők

| # | Forrás | Teendő | Felelős | Határidő | Kész? |
|---|---|---|---|---|---|
| T-01 | [D-nn] | [pl. elavult változatok archiválása, szkennelt PDF-ek OCR-je] | [név] | [dátum] | [ ] |

## 4. Jogosultsági elv

[Egy mondat: a rendszer csak azt használhatja, amit a kérdező felhasználó a forrásban lát — vagy
ha ettől eltérünk, miért és milyen kontrollal.]

---

## Kitöltési útmutató

| Mező | Mit írj bele | Példa (Xyo) | Tipikus hiba |
|---|---|---|---|
| Forrás | tár vagy mappa szintjén, ha a tár vegyes | Cloud Pilot projekttár — és külön sorban a „Kérdőívek/nyers” mappa | csak társzinten nézni — a vegyes mappák rejtve maradnak |
| Adatgazda | aki dönthet a tartalomról | Molnár Katalin (Beszerzés) | az IT-t megadni gazdának — ő üzemelteti, nem ő dönt a tartalomról |
| Frissesség | utolsó módosítás + vannak-e elavult változatok | utazási szabályzat: két változat él (2024, 2026) | kihagyni — a keresés a régit hozza ([3. iteráció](../04-xyo-pelda.md)) |
| Jogosultsági modell | ki láthatja, és rendben van-e az öröklődés | Pénzügy tár: egy almappán megszakadt öröklődés | „a SharePoint kezeli” — a régi hibákat az asszisztens kereshetővé teszi |
| Személyes adat | milyen fajta, mennyi | nyers kérdőív-export névvel | „belső dokumentum, nincs benne személyes adat” — nevek, e-mailek szinte mindenhol vannak |
| Döntés | be / ki / tisztítás után be | „Kérdőívek/nyers”: **ki**; az összesítő riport: be | döntés nélküli sor — a G0 nem zárható le |
| Kizárási szabályok | a cél és a jog szerinti tiltások, ellenőrzési móddal | X-01: egyéni HR-anyagok (értékelések, bérek, fegyelmik) — mappaszabály + szúrópróba | szabály ellenőrzési mód nélkül |
| Tisztítási teendők | ami a minőséghez kell, felelőssel | 37 elavult dokumentum archiválása; 112 szkennelt PDF OCR-je | a tisztítást a megvalósítóra bízni — a tartalomról az adatgazda dönt |
| Jogosultsági elv | egy eldönthető mondat | „az asszisztens csak azt használja, amit a kérdező a SharePointban lát” (G0-6) | szolgáltatásfiókkal mindent indexelni, „majd a felület szűr” |
