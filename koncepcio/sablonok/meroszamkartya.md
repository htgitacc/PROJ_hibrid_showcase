# Mérőszámkártya — [MK-nn] [a mutató neve]

> **Használat.** Minden mutatóhoz, amelyre döntést alapozunk, egy kártya. A kártya akkor jó, ha
> egy idegen is el tudja dönteni belőle, hogy a mért érték zöld, sárga vagy piros, és mi a teendő.
> A „Mi számít jónak” mező **a mérés előtt** lezárul (a G0-n), a kapunál már nem módosítható.
>
> Kitöltött példák: [mérési rendszer](../02-meresi-rendszer.md), MK-01 – MK-08. A szakszavak:
> [tudasbazis.md](../../kutatas/tudasbazis.md).

---

**Kártya azonosító:** [MK-nn]\
**Mutató:** [név, angolul, ha szakszó — pl. Faithfulness]\
**Kártya gazdája:** [név, szerep]\
**Típus:** [kizáró / kritikus / támogató / diagnosztika]\
**Jóváhagyva:** [dátum, ki — a G0-n]\
**Verzió:** [1.0]

| Szakasz | Tartalom |
|---|---|
| **Mit mér, és miért** | [Mit mér egy mondatban. Melyik célhoz, kockázathoz vagy kötelezettséghez kötődik.] |
| **Kiválasztás szempontjai** | [Miért ez a mutató, és nem más. **Mit nem mér** — a korlátai. Mivel kell együtt olvasni.] |
| **Hol és mikor** | [Melyik részben (keret / kísérleti szakasz / bevezetési ág / termékág), milyen gyakran, melyik kapunál dönt.] |
| **Ki és mivel** | [Ki méri, ki ellenőrzi. Adatforrás, tesztkészlet és verziója, módszer, eszköz.] |
| **Kiértékelés** | [Képlet. Mintanagyság — és hogy egy eset hány százalékpont. Hogyan olvasd: összesítve és esetszinten.] |
| **Mi számít jónak** | Zöld: [≥ / ≤ érték] · Sárga: [tartomány] · Piros: [érték] · Kapuhatár: [pl. G1-en piros = kill criterion] |
| **Hosszú távú követés** | [Mérési ritmus élesítés után. Trend: hol látszik, ki nézi, kinek jelenti.] |
| **Beavatkozási feltétel** | [Mi indít újra munkát (pl. két egymást követő sárga mérés), milyen munkát, ki dönt róla.] |

**Változásnapló:** [dátum — mi változott — ki hagyta jóvá]

---

## Kitöltési útmutató

| Mező | Mit írj bele | Példa (Xyo, MK-03) | Tipikus hiba |
|---|---|---|---|
| Típus | **kizáró**: egyetlen rossz érték leállít; **kritikus**: a go feltétele; **támogató**: sárgán is mehet; **diagnosztika**: hibahely-keresésre, döntés nélkül | kritikus | mindent kritikusnak jelölni — akkor egyik sem az |
| Mit mér, és miért | egy mondat a mérésről + a cél vagy kockázat, amelyhez kötődik | „a nem megválaszolható kérdésekre hányszor mondja, hogy nem talált forrást” — a magabiztos téves válasz kockázata | a mutató nevét megismételni magyarázat helyett |
| Kiválasztás szempontjai | miért ez; **mit nem mér**; melyik másik mutatóval párban olvasandó | párban a téves elutasítással, mert egymás rovására javíthatók | kihagyni a korlátokat — ettől lesz félreolvasható |
| Hol és mikor | rész, ritmus, kapu | a kísérleti szakasz minden iterációja; G1 kritikus; élesben heti | csak a projektre gondolni, az élesítés utáni életre nem |
| Ki és mivel | mérő, ellenőrző, adatforrás **verzióval** | Cloudia Solutions, golden set v1.0, 8 elem; Kiss Réka átnézi | verzió nélküli tesztkészlet — két mérés nem lesz összevethető |
| Kiértékelés | képlet; mintanagyság; egy eset hány pont | helyes elutasítás / 8; **egy eset 12,5 pont** | kis mintán százaléktizedekre figyelni |
| Mi számít jónak | három sáv + a kapuhatár; ha példaérték, jelöld *(feltevés)* | ≥ 90% · 80–89% · < 80%; és téves elutasítás ≤ 10% | a küszöböt a mérés után igazítani |
| Hosszú távú követés | ritmus, trend, címzett | élesben a „nem találtam” válaszok heti aránya | „folyamatosan figyeljük” — ritmus és felelős nélkül |
| Beavatkozási feltétel | eldönthető esemény → konkrét munka → döntéshozó | gyakran visszatérő, el nem utasítható kérdés → új golden set-elem és döntés: hiányzó dokumentum vagy rendszerhiba | „ha romlik, javítjuk” — mi számít romlásnak, és ki dönt? |
