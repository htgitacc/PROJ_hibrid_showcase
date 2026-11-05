# Koncepció — hibrid projektmenedzsment egy AI-projekten

A [kutatás](../kutatas/00-osszefoglalo.md) eredményéből felépített működési modell, a Xyo
Tudásasszisztens példáján. A modell nem a prediktív és az agilis módszer keveréke, hanem **három
különböző bizonytalanság szétválasztása**: az üzleti és jogi kérdéseket a **keret** dönti el előre, a
megvalósíthatóságot a **kísérleti szakasz** méri ki, a használatot a **kettéválás** utáni bevezetési ág és termékág
kezeli.

## Olvasási sorrend

| # | Dokumentum | Mit ad |
|---|---|---|
| 0 | [Működési modell](00-mukodesi-modell.md) | a váz: keret, kísérleti szakasz, kettéválás; ábra; szakaszos finanszírozás |
| 1 | [Kapuk és leállítási feltételek](01-kapuk-es-kill-criteria.md) | G0, G1 (go / pivot / no-go), G2, a változáskérés útja |
| 2 | [Mérési rendszer](02-meresi-rendszer.md) | mérési térkép, golden set, nyolc kitöltött mérőszámkártya |
| 3 | [Szerepek](03-szerepek.md) | ki mit csinál, RACI, a PM és a product owner határa |
| 4 | [Xyo-példa](04-xyo-pelda.md) | a modell próbája: minden kapu működésbe lép |
| — | [Sablonok](sablonok/README.md) | öt letölthető, üres minta kitöltési útmutatóval |
| — | Kitöltött Xyo-minták: [célkártyák](xyo-mintak/celkartyak.md), [adatleltár](xyo-mintak/adatleltar.md), [AI Act-besorolási lap](xyo-mintak/ai-act-besorolasi-lap.md), [kapudöntések](xyo-mintak/kapudontesek.md) | a sablonok kitöltve, a Xyo-példa adataival |

Gyors út: a [Xyo-példa](04-xyo-pelda.md) 4.9-es táblája egy oldalon mutatja, mit tanít a modell.

## Három dolog, amit ez a modell másképp csinál

1. **Szakaszos finanszírozás.** A bevezetésre csak akkor költünk, ha a mérés igazolta a
   megvalósíthatóságot; egy no-go így legfeljebb a PoC-keretbe kerül.
2. **A küszöbök a mérés előtt rögzítettek.** A kapun a számok döntenek, nem a demó benyomása, és a
   küszöb nem lazítható „mert majdnem elértük”.
3. **A scope-határ a keretnél marad.** A termékág nem bővítheti a rendszert olyan irányba, amely a
   jogi besorolást megváltoztatná — az új projekt.

A szakszavak magyarázata, olvasási útmutatóval: [tudasbazis.md](../kutatas/tudasbazis.md).
