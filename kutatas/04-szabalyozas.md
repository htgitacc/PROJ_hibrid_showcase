# 4. Szabályozás: AI Act és GDPR egy belső tudásasszisztensnél

> **Kérdés:** milyen jogi kötelezettség vonatkozik egy belső, dokumentumokból válaszoló
> AI-asszisztensre, és mi ebből a projekt számára fix, nem alkuképes elem?
>
> **Rövid válasz:** egy jól körülhatárolt belső tudásasszisztens **valószínűleg nem magas
> kockázatú** az [AI Act](tudasbazis.md#ai-act) szerint, de két kötelezettség **már ma hatályos**
> (AI literacy, átláthatóság), és **egy rossz felhasználási cél — egyéni HR-döntések támogatása —
> magas kockázatúvá teheti**. A [GDPR](tudasbazis.md#gdpr) szerinti hatásvizsgálat ([DPIA](tudasbazis.md#dpia))
> kérdését a feldolgozás előtt el kell dönteni. Ezek a prediktív keret fix mérföldkövei: nem
> iterálhatók, határidejük és felelősük van.
>
> **Ez nem jogi tanács.** A fejezet a projekt tervezéséhez gyűjti össze a kötelezettségeket; a
> tényleges besorolás a projekt jogászának vagy adatvédelmi tisztviselőjének a dolga.

A szakszavak magyarázata: [tudasbazis.md](tudasbazis.md).

---

## 4.1. Az AI Act idővonala az Omnibus után

Az EU AI Act Service Desk hivatalos idővonala már a *Digital Omnibus on AI* módosításait
tartalmazza (F-11); egy jogi összefoglaló szerint a módosítás a magas kockázatú szabályok
alkalmazását elválasztotta a szabványok elkészültétől, és rögzített dátumokat adott (F-12).

| Dátum | Mi lép életbe (F-11, F-12) | Érinti-e a Xyo-asszisztenst? |
|---|---|---|
| 2024. augusztus 1. | hatálybalépés | — |
| 2025. február 2. | általános rendelkezések (fogalmak, **[AI literacy](tudasbazis.md#ai-literacy)**) és a tiltott gyakorlatok | **igen**: a munkatársak AI-jártasságát támogatni kell |
| 2025. augusztus 2. | általános célú AI-modellek ([GPAI](tudasbazis.md#gpai)) szolgáltatóinak kötelezettségei, irányítási rendszer | közvetve: a modell szolgáltatójára vonatkozik, nem a Xyóra |
| 2026. augusztus 2. | a szabályok többsége; **átláthatósági szabályok ([Article 50](tudasbazis.md#article-50))** | **igen**: a felhasználónak tudnia kell, hogy AI-val beszél |
| 2026. december 2. | új tiltások; az 50. cikk (2) bekezdésének (szintetikus tartalom jelölése) átmeneti határideje a már forgalomban lévő rendszereknek | nem jellemzően |
| 2027. december 2. | **magas kockázatú rendszerek ([Annex III](tudasbazis.md#annex-iii))** szabályai | **csak akkor, ha** a felhasználás magas kockázatú esetbe esik (4.3) |
| 2028. augusztus 2. | szabályozott termékekbe épített magas kockázatú AI (Annex I) | nem |

**Hogyan olvasd.** A mai dátumon (2026. november) az AI literacy és az 50. cikk **már
alkalmazandó**: egy most induló projektnek nem „felkészülnie” kell rájuk, hanem az első naptól
teljesítenie. Az AI literacy kötelezettséget az Omnibus enyhítette: a szolgáltatóknak és az
alkalmazóknak intézkedéseket kell tenniük a munkatársak jártasságának támogatására, de **nem kell
garantálniuk** egyetlen személy meghatározott jártassági szintjét sem (F-12).

## 4.2. Átláthatóság: a felhasználó tudja, hogy géppel beszél

Az 50. cikk (1) bekezdése szerint a **szolgáltatónak** úgy kell kialakítania a természetes
személyekkel közvetlenül kommunikáló AI-rendszert, hogy az érintettek tudják: AI-rendszerrel
állnak kapcsolatban — kivéve, ha ez egy észszerűen tájékozott, figyelmes és körültekintő személy
számára a körülményekből nyilvánvaló. Az (5) bekezdés szerint ezt **világosan és
megkülönböztethetően, legkésőbb az első interakciókor** kell közölni (F-13).

**Mi következik a projektre:**

- a felületen az első használatkor egyértelmű jelzés (pl. „AI-asszisztens — a válaszok hibásak
  lehetnek, ellenőrizd a megjelölt forrást”); ez **elfogadási feltétel**, nem kozmetika;
- hogy a Xyo ebben a felállásban **[provider](tudasbazis.md#provider-and-deployer)** vagy csak
  **deployer** (alkalmazó), az attól függ, ki állítja össze és kínálja a rendszert — ezt a
  jogásznak kell eldöntenie; a projekt szempontjából a jelzés mindkét esetben kell.

## 4.3. A scope-határ: mikor válna magas kockázatúvá?

A III. melléklet 4. pontja (foglalkoztatás) szerint magas kockázatú az AI-rendszer, ha (F-14):

- (a) munkaerő-felvételre vagy kiválasztásra szánják (álláshirdetés célzása, pályázatok
  szűrése, jelöltek értékelése);
- (b) a munkaviszony feltételeit, **előléptetést vagy megszüntetést érintő döntésekre**, egyéni
  viselkedésen vagy személyes jellemzőkön alapuló **feladatkiosztásra**, illetve a munkavállalók
  **teljesítményének és viselkedésének figyelésére és értékelésére** szánják.

**Ez a fejezet legfontosabb gyakorlati következménye.** Egy belső tudásasszisztens, amely a
szabályzatokból és útmutatókból válaszol, nem esik ide. Ugyanaz a rendszer viszont ide eshet — **[high-risk AI system](tudasbazis.md#high-risk-ai-system)** lenne —, ha
például vezetők arra használják, hogy „foglald össze X teljesítményét az értékelések alapján”.
Ezért a modellben:

- a **cél és a kizárás írásban rögzített** (projektalapító dokumentum): a rendszer nem támogat
  egyénekről szóló munkaügyi döntést;
- az **egyéni HR-anyagok (értékelések, fegyelmi, bérek) nem kerülnek az indexbe** — ez az
  adatleltár egyik kizárási szabálya;
- ha az üzlet később mégis ilyen funkciót kér, az **új projekt új besorolással**, nem
  változáskérés a meglévőben.

Ez a fajta döntés — rögzített cél, rögzített kizárás, jóváhagyással — tipikusan **prediktív**
elem: a kísérleti szakaszban nem lehet „kipróbálni”.

## 4.4. GDPR: kell-e adatvédelmi hatásvizsgálat?

A GDPR 35. cikke szerint az adatkezelőnek **az adatkezelés előtt** hatásvizsgálatot kell
végeznie, ha az adatkezelés — különösen **új technológiák** alkalmazásával — valószínűleg magas
kockázattal jár a természetes személyek jogaira és szabadságaira. Kifejezetten kötelező többek
között, ha automatizált értékelésen (profilozáson is) alapuló döntések születnek, amelyek joghatással
vagy hasonlóan jelentős hatással vannak a személyre (F-15).

**Mi következik a projektre:**

- a céges dokumentumtár személyes adatot tartalmaz (nevek, elérhetőségek, levelezés,
  jegyzőkönyvek); az LLM-alapú feldolgozás új technológia — **a DPIA szükségességét a kísérleti
  kísérleti szakasz előtt, írásban el kell dönteni**, és ha kell, el kell végezni;
- a nemzeti adatvédelmi hatóság (Magyarországon a NAIH) listája arról, mely adatkezelésekhez
  kötelező a DPIA, **itt nincs feldolgozva** — a projektben meg kell nézni;
- a 4.3 kizárási szabálya (nincs egyéni HR-döntés, nincs HR-anyag az indexben) a DPIA-t is
  egyszerűsíti.

## 4.5. A prediktív keret fix elemei — összegyűjtve

Saját összeállítás a fenti kötelezettségekből:

| Elem | Mikor | Ki dönt / felel | Forrás |
|---|---|---|---|
| Cél és kizárások rögzítése (nincs egyéni HR-döntés) | indítás | szponzor + jogász | F-14 |
| AI Act-besorolás (nem magas kockázatú? provider vagy deployer?) | indítás | jogász / adatvédelmi tisztviselő | F-11, F-13, F-14 |
| DPIA szükségességének döntése, szükség esetén elvégzése | a kísérleti szakasz előtt | adatkezelő (Xyo), adatvédelmi tisztviselő | F-15 |
| Adatleltár kizárási szabályokkal (HR-anyagok ki) | a kísérleti szakasz előtt | projektmenedzser + adatgazdák | F-14, F-15 |
| AI-jelzés a felületen, első interakciókor | a PoC-kapu elfogadási feltétele | termékfelelős | F-13 |
| AI literacy intézkedések (képzés, útmutató) | a bevezetési ágban, élesítés előtt | projektmenedzser + HR | F-11, F-12 |

**A tanulság a modellnek:** ezek nem iterálhatók és nem „mérhetők jobbra” — vagy teljesülnek,
vagy nem. Ezért kerülnek a prediktív keretbe, kapukhoz kötve. A kísérleti szakasz csak ezek
teljesülése után kezdhet valós adattal dolgozni.

---

## Összegzés

| Állítás | Bizonyíték | Erősség |
|---|---|---|
| Az AI literacy (2025. február) és az 50. cikk (2026. augusztus) már alkalmazandó | F-11, F-12 | A, C |
| A magas kockázatú (Annex III) szabályok 2027. december 2-tól alkalmazandók | F-11, F-12 | A, C |
| A felhasználónak legkésőbb az első interakciókor tudnia kell, hogy AI-val beszél | F-13 | A |
| Egyéni munkaügyi döntések támogatása magas kockázatúvá teszi a rendszert | F-14 | A |
| Új technológiával, magas kockázat valószínűségénél a feldolgozás előtt DPIA kell | F-15 | A |
| A szabályozási elemek a prediktív keret fix, kapukhoz kötött mérföldkövei | saját értelmezés | — |

**Ami nincs benne:** a NAIH DPIA-listája, a GPAI-szolgáltatói kötelezettségek részletei, a
szerzői jogi kérdések, és a munkajogi (üzemi tanácsi) egyeztetési kötelezettség — ezeket a
koncepció kockázati részében kell felvenni.
