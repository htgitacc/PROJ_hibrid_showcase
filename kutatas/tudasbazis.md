# Tudásbázis — szakszavak, rövidítések, mérési módszerek, mutatók

A szakszavak **angol alakjukban maradnak**: így szerepelnek a szakirodalomban, az eszközökben és
az álláshirdetésekben, és így lehet rájuk keresni. Fordítás helyett minden szócikk megmondja, mit
jelent a kifejezés, hol találkozol vele ebben a modellben, és — mutatóknál, módszereknél — **hogyan
kell olvasni**.

## Hogyan használd

- A szócikkek **kategóriánként**, azon belül betűrendben állnak.
- A dokumentumokban az első előfordulásnál a kifejezés ide mutat.
- A **mutatóknál** a „Hogyan olvasd” és a „Tipikus félreolvasás” mező a lényeg: egy szám önmagában
  semmit nem mond, csak a mérés módjával, a mintával és a küszöbbel együtt.

## A szócikk szerkezete

Minden szócikk saját alcím (`### Kifejezés`), hogy a dokumentumokból közvetlenül linkelhető
legyen (`tudasbazis.md#kifejezes`).

> **Kifejezés** (*kibontás, ha rövidítés*)\
> **Mit jelent:** egy-két mondat, köznyelven.\
> **Hol fordul elő:** melyik fázisban, melyik dokumentumban, melyik kapunál.\
> **Hogyan olvasd:** mutatónál a skála, az irány (nagyobb jobb / kisebb jobb), mi a jó és mi a gyanús;
> módszernél, hogy mit ad és mit nem.\
> **Tipikus félreolvasás:** a leggyakoribb hiba, amit a számmal vagy a fogalommal elkövetnek.\
> **Lásd:** kapcsolódó szócikk, minta (`koncepcio/sablonok/`), kutatási dokumentum, forrás (`F-nn`).

A nem mutató jellegű fogalmaknál a „Hogyan olvasd” mező elmarad, ha nincs mit olvasni rajta.

---

## Rövidítések

### AI Act
**Mit jelent:** az EU mesterséges intelligenciáról szóló rendelete (2024/1689). Kockázati szintek szerint szabályoz: tiltott gyakorlatok, magas kockázatú rendszerek, átláthatósági kötelezettségek, minimális kockázat.\
**Hol fordul elő:** a prediktív keretben: az AI Act-besorolás az indítás egyik kötelező dokumentuma; részletesen a [04](04-szabalyozas.md) fejezetben.\
**Tipikus félreolvasás:** „minden AI-rendszer magas kockázatú”. A legtöbb belső asszisztens nem az; a besorolás a felhasználási célon múlik, nem a technológián.\
**Lásd:** [DPIA](#dpia), [Responsible AI](#responsible-ai).

### CPMAI
**Mit jelent:** *Cognitive Project Management for AI* — AI-projektekre szabott, adatközpontú, iteratív módszertan hat fázissal (business understanding → data understanding → data preparation → model development → model evaluation → model operationalization); a PMI minősítésként kínálja (PMI-CPMAI).\
**Hol fordul elő:** a [03](03-ai-projektmodszertanok.md) fejezetben; a kísérleti szakasz fázisainak mintája.\
**Tipikus félreolvasás:** teljes PM-keretrendszernek tekinteni. A PMI szerint a hagyományos PM-et kiegészíti: költségkeretre, beszerzésre, megfelelésre nem ad választ.\
**Lásd:** [CRISP-DM](#crisp-dm), F-09.

### CRISP-DM
**Mit jelent:** *Cross-Industry Standard Process for Data Mining* — 2000-es iparági folyamatmodell adatbányászati (ma: ML-) projektekre, hat fázissal; a CPMAI és sok mai ML-módszertan őse.\
**Hol fordul elő:** a [03](03-ai-projektmodszertanok.md) fejezetben.\
**Tipikus félreolvasás:** vízesésként olvasni a hat fázist. Az eredeti szöveg szerint a sorrend nem merev, és az oda-vissza lépés mindig szükséges.\
**Lásd:** [CPMAI](#cpmai), [Stage gate](#stage-gate), F-08.

### DPIA
**Mit jelent:** *Data Protection Impact Assessment* — a GDPR szerinti adatvédelmi hatásvizsgálat: kötelező, ha az adatkezelés valószínűleg magas kockázattal jár az érintettek jogaira.\
**Hol fordul elő:** a prediktív keretben, az indításkor; a kísérleti szakasz előtt el kell dőlnie, milyen adat kerülhet a rendszerbe.\
**Tipikus félreolvasás:** „csak a jogászok dolga”. A DPIA-hoz tudni kell, milyen dokumentumok, kinek a jogosultságával kerülnek a rendszerbe — ez az adatleltár, tehát projektfeladat.\
**Lásd:** [AI Act](#ai-act), [02](02-miert-buknak-el-az-ai-projektek.md).

### GDPR
**Mit jelent:** *General Data Protection Regulation* — az EU általános adatvédelmi rendelete (2016/679). Minden személyes adatot érintő kezelésre vonatkozik, AI-tól függetlenül.\
**Hol fordul elő:** a prediktív keretben: adatleltár, DPIA, jogosultságok.\
**Tipikus félreolvasás:** „belső rendszer, ezért nem vonatkozik rá”. A munkatársak adatai is személyes adatok.\
**Lásd:** [DPIA](#dpia), [04](04-szabalyozas.md), F-15.

### GenAI
**Mit jelent:** *Generative AI* — olyan AI, amely új tartalmat (szöveget, képet, kódot) állít elő, jellemzően [LLM](#llm)-re épülve.\
**Hol fordul elő:** a bukási statisztikákban (F-04, F-05) és a modell tárgyában.\
**Tipikus félreolvasás:** a GenAI-statisztikákat a klasszikus (előrejelző) ML-projektekre is érvényesnek tekinteni, vagy fordítva — a két projekttípus másként bukik el.\
**Lásd:** [LLM](#llm), [RAG](#rag).

### GPAI
**Mit jelent:** *General-Purpose AI* — általános célú AI-modell (pl. a nagy nyelvi modellek), amely sokféle feladatra használható. Az AI Act külön kötelezettségeket ír elő a GPAI-modellek szolgáltatóinak (2025. augusztus 2-tól).\
**Hol fordul elő:** a szolgáltató-kiválasztásnál: a modellt adó cég kötelezettségei, nem a Xyóé.\
**Tipikus félreolvasás:** a GPAI-szolgáltató kötelezettségeit a saját projekt kötelezettségének tekinteni — vagy fordítva, azt hinni, hogy a szolgáltató megfelelése a mi felhasználásunkat is lefedi.\
**Lásd:** [AI Act](#ai-act), F-11.

### LLM
**Mit jelent:** *Large Language Model* — nagy nyelvi modell: hatalmas szövegmennyiségen tanított modell, amely szöveget ért és állít elő.\
**Hol fordul elő:** a Xyo Tudásasszisztens válaszadó része; a modellt nem mi tanítjuk, hanem szolgáltatótól vesszük.\
**Tipikus félreolvasás:** „az LLM tudja a cég adatait”. Nem tudja — csak azt, amit a kérdéssel együtt megkap. Ezért kell a [RAG](#rag).\
**Lásd:** [GenAI](#genai), [RAG](#rag).

### MLOps
**Mit jelent:** *Machine Learning Operations* — a gépi tanulási modellek élesítésének, monitorozásának, újratanításának és visszaállításának gyakorlata és eszközei (a DevOps ML-re alkalmazva). LLM-alkalmazásoknál gyakran *LLMOps* néven.\
**Hol fordul elő:** a PoC utáni üzemeltetésben és az agilis termékfolyamatban.\
**Tipikus félreolvasás:** „majd az élesítés után foglalkozunk vele”. A monitorozás és a visszaállítás terve a bevezetés feltétele.\
**Lásd:** [03](03-ai-projektmodszertanok.md).

### P&L
**Mit jelent:** *Profit and Loss* — eredménykimutatás; „P&L-hatás” = a bevételben vagy a költségben ténylegesen megjelenő pénzügyi hatás.\
**Hol fordul elő:** az MIT-jelentés sikerdefiníciójában (F-04); a mi üzleti esetünk haszonmutatóinál.\
**Tipikus félreolvasás:** a megtakarított munkaidőt automatikusan P&L-hatásnak venni. Csak akkor az, ha a felszabaduló idő máshol értéket termel, vagy költség marad el.\
**Lásd:** [02](02-miert-buknak-el-az-ai-projektek.md).

### PMBOK
**Mit jelent:** *Project Management Body of Knowledge* — a PMI projektmenedzsment-szabványa
(*PMBOK Guide*). A 8. kiadás 2025 novemberében jelent meg.\
**Hol fordul elő:** a `PROJ_pm_all` gerince; itt a prediktív keret hivatkozási alapja.\
**Tipikus félreolvasás:** „a PMBOK = waterfall”. A 7. kiadás óta elvekre és performance
domainekre épül, és kifejezetten prediktív, agilis és hibrid megközelítésre is alkalmazható.\
**Lásd:** [Tailoring](#tailoring), [Performance domain](#performance-domain), [01](01-hibrid-a-piacon.md), F-02.

### PMI
**Mit jelent:** *Project Management Institute* — a legnagyobb nemzetközi projektmenedzsment-szakmai
szervezet; a PMBOK és a PMP, PMI-ACP, PMI-CPMAI minősítések gazdája.\
**Hol fordul elő:** a forrásokban (Pulse of the Profession felmérések, szabványok).\
**Tipikus félreolvasás:** a PMI-felméréseket független kutatásnak tekinteni. Nagy mintásak, de a
szakma érdekelt szervezetétől származnak — ezért B szintűek.\
**Lásd:** [01](01-hibrid-a-piacon.md), F-01, F-02.

### PoC
**Mit jelent:** *Proof of Concept* — megvalósíthatósági próba: rövid, korlátozott kísérlet annak eldöntésére, hogy az ötlet működik-e a kért minőségben.\
**Hol fordul elő:** a kísérleti szakasz; a végén a go/no-go kapu dönt.\
**Tipikus félreolvasás:** a PoC-t „kis éles rendszernek” tekinteni, amelyből automatikusan bevezetés lesz. A PoC célja a döntés — a leállítás is érvényes kimenet.\
**Lásd:** [Pilot](#pilot), [Kill criteria](#kill-criteria), F-05, F-07.

### RAG
**Mit jelent:** *Retrieval-Augmented Generation* — a kérdéshez először megkeresi a releváns dokumentumrészleteket (retrieval), majd ezekkel együtt adja át az [LLM](#llm)-nek, hogy azokra alapozva válaszoljon (generation).\
**Hol fordul elő:** a Xyo Tudásasszisztens működési elve: a SharePoint-dokumentumokból válaszol, forrásmegjelöléssel.\
**Tipikus félreolvasás:** „a RAG kiküszöböli a hallucinációt”. Csökkenti, de nem szünteti meg: a modell tévesen is összefoglalhatja a megtalált szöveget, vagy rossz részletet találhat. Ezt mérni kell.\
**Lásd:** [LLM](#llm), [02](02-miert-buknak-el-az-ai-projektek.md).

### TCO
**Mit jelent:** *Total Cost of Ownership* — teljes bekerülési költség: nemcsak a fejlesztés, hanem a licenc, a futási (használatarányos) díj, az üzemeltetés, a támogatás és a továbbfejlesztés is, a teljes élettartamra.\
**Hol fordul elő:** az üzleti esetben és a szolgáltató-kiválasztásnál; a Gartner egyik bukási oka (F-05).\
**Tipikus félreolvasás:** a PoC költségéből következtetni az éles költségre. A használatarányos díj a felhasználók és a kérdések számával nő.\
**Lásd:** [02](02-miert-buknak-el-az-ai-projektek.md).

## Folyamatfogalmak

### Agile approach
**Mit jelent:** rövid, időkeretes iterációkban dolgozó megközelítés, amely a változó igényekre
gyakori visszajelzéssel reagál (pl. Scrum). A scope mozog, az idő és a csapat rögzített.\
**Hol fordul elő:** a `PROJ_sm_all` modellje; itt a kísérleti szakasz és a PoC utáni termékfolyamat.\
**Tipikus félreolvasás:** „agilis = nincs terv”. Van terv, csak rövid távra részletes, és
iterációnként újra eldől.\
**Lásd:** [Predictive approach](#predictive-approach), [Hybrid approach](#hybrid-approach).

### AI literacy
**Mit jelent:** AI-jártasság: az AI Act 4. cikke szerint a szolgáltatóknak és alkalmazóknak intézkedéseket kell tenniük, hogy a munkatársaik és az érintett személyek értsék az általuk használt AI-rendszerek lehetőségeit és kockázatait. 2025. február 2. óta alkalmazandó; az Omnibus szerint nem kell egyéni jártassági szintet garantálni.\
**Hol fordul elő:** a bevezetési ágban: képzés, felhasználói útmutató, „mire figyelj” kártya.\
**Tipikus félreolvasás:** egyszeri e-learningnek tekinteni. A cél, hogy a felhasználó tudja: a válasz hibás lehet, és ellenőrizni kell a forrást.\
**Lásd:** [04](04-szabalyozas.md), F-11, F-12.

### AI-ready data
**Mit jelent:** a Gartner fogalma: olyan adat, amely az adott AI-felhasználási esetre reprezentatív — tartalmazza a mintázatokat, hibákat, kiugró és váratlan eseteket —, és metaadatokkal igazolhatóan minősíthető és kormányozható. Nem egyszeri állapot, hanem folyamatos gyakorlat.\
**Hol fordul elő:** az adatleltárban (prediktív keret) és az adatminőség mérésében (kísérleti szakasz).\
**Tipikus félreolvasás:** „jó minőségű adat = AI-ready”. Egy riportnak megfelelő adat nem feltétlenül jó egy AI-esetre; a mérce mindig a konkrét felhasználás.\
**Lásd:** F-06, [02](02-miert-buknak-el-az-ai-projektek.md).

### Annex III
**Mit jelent:** az AI Act III. melléklete: azoknak a felhasználási területeknek a listája, ahol az AI-rendszer magas kockázatúnak minősül (biometria, kritikus infrastruktúra, oktatás, **foglalkoztatás**, alapvető szolgáltatások, bűnüldözés, migráció, igazságszolgáltatás). Szabályai 2027. december 2-tól alkalmazandók.\
**Hol fordul elő:** a prediktív keretben, az AI Act-besorolásnál; a scope-határ kijelölésénél.\
**Tipikus félreolvasás:** a technológiából kiindulni („chatbot, tehát nem magas kockázatú”). A besorolás a **felhasználási célon** múlik: ugyanaz a chatbot egyéni HR-döntésekhez használva magas kockázatú lehet.\
**Lásd:** [High-risk AI system](#high-risk-ai-system), [04](04-szabalyozas.md), F-14.

### Article 50
**Mit jelent:** az AI Act 50. cikke: átláthatósági kötelezettségek. Az (1) bekezdés szerint a természetes személyekkel közvetlenül kommunikáló AI-rendszernél az érintettnek tudnia kell, hogy AI-val áll kapcsolatban, legkésőbb az első interakciókor. 2026. augusztus 2. óta alkalmazandó.\
**Hol fordul elő:** a PoC-kapu elfogadási feltételei között: AI-jelzés a felületen.\
**Tipikus félreolvasás:** az ÁSZF-be vagy egy súgóoldalra eldugni. A szöveg szerint „világosan és megkülönböztethetően” kell közölni.\
**Lásd:** [Provider and deployer](#provider-and-deployer), [04](04-szabalyozas.md), F-13.

### Change management
**Mit jelent:** változáskezelés: annak megtervezése és végrehajtása, hogy az érintettek ténylegesen átvegyék az új eszközt vagy működést — kommunikáció, képzés, támogatás, ellenállás kezelése.\
**Hol fordul elő:** a PoC-kapu utáni prediktív bevezetési ágban.\
**Tipikus félreolvasás:** a változáskezelést a bevezetés utolsó hetére hagyni. A Gartner szerint a GenAI-projektek egyik bukási pontja (F-05).\
**Lásd:** [02](02-miert-buknak-el-az-ai-projektek.md).

### Chunk
**Mit jelent:** darab, szövegrész: a RAG-rendszer a dokumentumokat kisebb részekre vágja (*chunking*), és a keresés ezeket a részeket adja vissza a kérdéshez.\
**Hol fordul elő:** a kísérleti szakasz adatelőkészítésében; a darabolás módja a keresés minőségének egyik fő változója.\
**Tipikus félreolvasás:** „minél kisebb, annál pontosabb”. A túl kicsi darabból hiányzik a szövegkörnyezet, a túl nagy sok zajt hoz — mérni kell (context recall és precision).\
**Lásd:** [Context recall](#context-recall), [Context precision](#context-precision).

### Dataset drift
**Mit jelent:** a tesztkészlet „elöregedése”: már nem hasonlít arra, amit a felhasználók valójában kérdeznek, ezért a jó tesztereményből nem következik jó éles működés.\
**Hol fordul elő:** élesítés után, az agilis termékfolyamatban.\
**Tipikus félreolvasás:** a romló éles visszajelzést a modellnek tulajdonítani, miközben a teszt zöld. A forrás szerint épp ez a drift legtisztább tünete — a készletet kell frissíteni.\
**Lásd:** [Golden set](#golden-set), F-16.

### Fit-for-purpose
**Mit jelent:** „a célra alkalmas” — az a szemlélet, hogy a módszert a projekt (vagy a
projektrész) jellegéhez választjuk, nem megszokásból vagy divatból.\
**Hol fordul elő:** a PMI 2024-es jelentésének kulcsszava; a modell alapelve.\
**Lásd:** [Tailoring](#tailoring), [01](01-hibrid-a-piacon.md), F-01.

### High-risk AI system
**Mit jelent:** magas kockázatú AI-rendszer az AI Act szerint: szabályozott termék biztonsági eleme (Annex I) vagy a III. mellékletben felsorolt területen használt rendszer. Kockázatkezelést, adatkormányzást, dokumentációt, emberi felügyeletet, naplózást és megfelelőségértékelést követel.\
**Hol fordul elő:** a besorolásnál; a Xyo-asszisztens célja szerint nem az, és a scope-határ ezt őrzi.\
**Tipikus félreolvasás:** azt hinni, hogy a besorolás egyszer eldől. Ha a felhasználás bővül (pl. HR-funkció), újra kell vizsgálni.\
**Lásd:** [Annex III](#annex-iii), F-14.

### Hybrid approach
**Mit jelent:** egy projekten belül prediktív és agilis elemek együttes használata — tipikusan
rögzített keret (költségvetés, mérföldkövek, jóváhagyások) és benne iteratív munka.\
**Hol fordul elő:** ennek a modellnek a tárgya.\
**Tipikus félreolvasás:** „a hibrid jobb, mert mindkettő előnyét hozza”. A PMI adatai szerint
nincs szignifikáns teljesítménykülönbség a megközelítések között; a hibrid attól jó, ha a részek
valóban más-más bizonytalanságot kezelnek, nem attól, hogy kevert.\
**Lásd:** [Fit-for-purpose](#fit-for-purpose), [01](01-hibrid-a-piacon.md), F-01.

### Kill criteria
**Mit jelent:** előre, írásban rögzített leállítási feltételek: ha a mérés ezeket nem éri el (vagy átlépi), a projekt — vagy egy ága — leáll, vita nélkül.\
**Hol fordul elő:** a PoC-kapunál; a modell kulcseleme.\
**Tipikus félreolvasás:** a leállítást kudarcnak tekinteni. A korai, olcsó leállítás jó kimenet; a rossz kimenet a hónapokig vonszolt, értéket nem hozó projekt.\
**Lásd:** [PoC](#poc), [02](02-miert-buknak-el-az-ai-projektek.md).

### Learning gap
**Mit jelent:** az MIT NANDA-jelentés fogalma: a bevezetett AI-eszközök nem tanulnak a felhasználói visszajelzésből, nem őrzik a kontextust és nem illeszkednek a munkafolyamatba — ezért a használat elhal.\
**Hol fordul elő:** a PoC utáni agilis termékfolyamatban: a visszajelzés gyűjtése és az értékelőkészlet bővítése erre a válasz.\
**Tipikus félreolvasás:** „jobb modell kell”. A jelentés szerint nem a modell minősége, hanem az illesztés és a tanulási hurok hiányzik.\
**Lásd:** F-04, [02](02-miert-buknak-el-az-ai-projektek.md).

### Performance domain
**Mit jelent:** a PMBOK 7. és 8. kiadásának szervezőegysége: a projektmunka egy-egy területe
(pl. érintettek, tervezés, bizonytalanság), amelyben bizonyos eredményeket kell elérni —
folyamatok helyett célok szerint.\
**Hol fordul elő:** a PMBOK-hivatkozásoknál.\
**Lásd:** [PMBOK](#pmbok), F-02.

### Pilot
**Mit jelent:** próbaüzem: a megoldás korlátozott körben, valós felhasználókkal és valós munkával. A [PoC](#poc) után jön: a PoC azt dönti el, megoldható-e a feladat, a pilot azt, hogy beválik-e a munkában.\
**Hol fordul elő:** a PoC-kapu után, a bevezetés első lépéseként.\
**Tipikus félreolvasás:** a PoC-t és a pilotot összemosni — a statisztikák is gyakran keverik.\
**Lásd:** [PoC](#poc), [Pilot-to-production rate](#pilot-to-production-rate).

### Pivot
**Mit jelent:** ebben a modellben a PoC-kapun hozott szűk értelmű döntés: a mérés alapján nem go, de a hiba helye azonosított, ezért egyetlen, időkorlátos (legfeljebb 2 hét) korrekciós kör következik, konkrét hipotézissel. A köznyelvi „irányváltásnál” szigorúbb: nem új cél, hanem egy azonosított hiba javítása.\
**Hol fordul elő:** a PoC-kapu döntési szabályai között (`koncepcio/01`, 1.3); a modell saját szabálya, nem külső szabvány.\
**Hogyan olvasd:** csak akkor jöhet szóba, ha a kizáró mutató zöld, legfeljebb egy kritikus mutató sárga, és a hiba helye azonosított. **Egyszer** van: a pivot utáni mérésen minden kritikus mutatónak zöldnek kell lennie, különben no-go ([Kill criteria](#kill-criteria), 3. pont).\
**Tipikus félreolvasás:** „még egy iteráció” pivot-indoklás nélkül. Azonosított hibahely és hipotézis nélkül ez nem pivot, hanem cél nélküli iteráció.\
**Lásd:** [Kill criteria](#kill-criteria), [Stage gate](#stage-gate), [Context recall](#context-recall).

### Predictive approach
**Mit jelent:** a „waterfall” szakszerű neve: a scope-ot, az ütemtervet és a költséget az elején
tervezik meg részletesen, és ehhez képest követik az eltérést.\
**Hol fordul elő:** a `PROJ_pm_all` modellje; itt a prediktív keret (indítás, megfelelés,
bevezetés).\
**Tipikus félreolvasás:** „elavult”. Ahol a követelmény stabil és a hibának nagy az ára
(építőipar, szabályozott határidő), ma is ez a fő megközelítés — az építőiparban 76% (F-01).\
**Lásd:** [Agile approach](#agile-approach), F-01.

### Product owner
**Mit jelent:** termékfelelős: az agilis termékág gazdája, aki a backlog sorrendjéről dönt, és képviseli a felhasználók és az üzlet érdekét.\
**Hol fordul elő:** a kettéválás után a termékágban; a kísérleti szakasz iterációinak bemutatóin már részt vesz.\
**Tipikus félreolvasás:** a projektmenedzserrel azonosítani. A hibrid modellben a PM a keretet és a bevezetési ágat vezeti, a product owner a termékágat — a két szerep együttműködik, de más döntésekért felel.\
**Lásd:** [Agile approach](#agile-approach).

### Prompt
**Mit jelent:** az LLM-nek adott utasítás és bemenet. Egy RAG-asszisztensnél a rendszerprompt (szabályok, stílus, mit tegyen, ha nem tudja a választ) és a felhasználó kérdése a megtalált dokumentumrészletekkel együtt.\
**Hol fordul elő:** a kísérleti szakaszban: a prompt beállítása az iterációk egyik fő változója.\
**Tipikus félreolvasás:** a promptot ártalmatlan szövegnek tekinteni, amelyet bárki szabadon javíthat. Az F-10 szerint egy „jó tanács” hozzáadása is ronthat — a prompt kódként kezelendő: verziózva és tesztelve.\
**Lásd:** [Regression testing](#regression-testing), [Eval-driven development](#eval-driven-development), F-10.

### Provider and deployer
**Mit jelent:** az AI Act két fő szereplője. *Provider* (szolgáltató): aki az AI-rendszert kifejleszti vagy kifejleszteti, és a saját neve alatt forgalomba hozza vagy üzembe helyezi. *Deployer* (alkalmazó): aki a rendszert a saját felelősségére használja. A kötelezettségek a szereptől függnek.\
**Hol fordul elő:** az AI Act-besorolásnál; a szolgáltatói szerződésben.\
**Tipikus félreolvasás:** „mi csak használjuk, ezért semmi dolgunk”. Ha a cég maga állítja össze a rendszert kész modellből, akár szolgáltatónak is minősülhet — ezt jogásznak kell eldöntenie.\
**Lásd:** [Article 50](#article-50), [04](04-szabalyozas.md).

### Responsible AI
**Mit jelent:** felelős AI: az a gyakorlat, hogy az AI-rendszer biztonságát, adatvédelmét, elszámoltathatóságát és méltányosságát a tervezéstől kezdve kezeljük, nem utólag.\
**Hol fordul elő:** a prediktív keret kockázatkezelésében (DPIA, AI Act, jogosultságok) és a kísérleti szakasz mérőszámaiban (pl. jogosultság-szivárgás).\
**Tipikus félreolvasás:** egy utolsó jóváhagyási lépésnek tekinteni. A Gartner szerint a GenAI-projektek egyik bukási pontja, ha utólagos gondolat (F-05).\
**Lásd:** [AI Act](#ai-act), [DPIA](#dpia).

### Stage gate
**Mit jelent:** döntési kapu a projekt két szakasza között: előre rögzített kritériumok alapján eldől, hogy a projekt továbbmegy, módosul vagy leáll (go / no-go).\
**Hol fordul elő:** a modellben a PoC-kapu; a prediktív keretben a fázislezárások.\
**Tipikus félreolvasás:** adminisztratív aláírásnak tekinteni. Akkor ér valamit, ha a kritériumok előre, számokkal rögzítettek, és a „no-go” valóban lehetséges kimenet.\
**Lásd:** [Kill criteria](#kill-criteria), [CRISP-DM](#crisp-dm).

### Tailoring
**Mit jelent:** a módszer, a folyamatok, az eszközök és a dokumentumok tudatos hozzáigazítása a
projekthez, a csapathoz és a környezethez — mit veszünk át, mit hagyunk el, mit módosítunk.\
**Hol fordul elő:** a PMBOK 8 központi témája; ennek a modellnek a módszere.\
**Tipikus félreolvasás:** „azt hagyjuk ki, amihez nincs kedvünk”. A tailoring indokolt és
dokumentált döntés (ADR-ben), nem kihagyás.\
**Lásd:** [Fit-for-purpose](#fit-for-purpose), F-02.

### Timebox
**Mit jelent:** rögzített időkeret: a munka hossza előre meghatározott és nem nyújtható; ami belefér, az a kimenet. Az agilis módszerek alapeleme (sprint), itt a kísérleti szakasz szabálya.\
**Hol fordul elő:** a kísérleti szakaszban (a Xyo-példában 7 hét) és a termékág sprintjeiben.\
**Tipikus félreolvasás:** a timeboxot „becsült határidőnek” tekinteni, amelyet szükség esetén kitolunk. A kísérleti szakasz hosszabbítása csak kapudöntéssel lehetséges — különben a PoC észrevétlenül projektté nő.\
**Lásd:** [Stage gate](#stage-gate), [PoC](#poc).

## Mérési módszerek

### Baseline
**Mit jelent:** kiindulási érték: az a mérés, amelyhez képest a változást olvassuk. Lehet a mai gyakorlat (pl. mennyi ideig tart ma egy szabályzat megtalálása), vagy a rendszer előző verziója ugyanazon a tesztkészleten.\
**Hol fordul elő:** az üzleti esetben (a haszon mihez képest), a kísérleti szakasz 0. iterációjában (a kiinduló beállítás mérése) és minden regressziós mérésnél.\
**Hogyan olvasd:** egy eredmény mindig „baseline-hoz képest +/−” formában értelmes; ugyanazon a mérési módon és készletverzión kell mérni.\
**Tipikus félreolvasás:** a baseline-t utólag, emlékezetből becsülni. Ha nincs előre rögzítve, a javulás nem bizonyítható — a `PROJ_pm_all` T0-mérése ugyanezért készült a projekt elején.\
**Lásd:** [Golden set](#golden-set), F-16.

### Eval-driven development
**Mit jelent:** olyan fejlesztési mód, amelyben a munka a mérés köré szerveződik: előbb elkészül a feladatspecifikus értékelőkészlet és a mérőszámok, és minden változtatás (prompt, keresés, modell) csak akkor kerül be, ha a mérés szerint nem ront.\
**Hol fordul elő:** a kísérleti szakasz munkamódja; a PoC-kapu ebből a mérésből dönt.\
**Hogyan olvasd:** a kérdés mindig „mennyit változott a mérőszám a változtatás után, ugyanazon a készleten” — nem „jobbnak tűnik-e”.\
**Tipikus félreolvasás:** egy-két kézzel kipróbált kérdés alapján dönteni. Az F-10 kísérletében egy általános javítás a RAG-esetek helyes válaszait 26/30-ról 9/30-ra rontotta.\
**Lásd:** [Regression testing](#regression-testing), [Prompt](#prompt), F-10.

### Golden set
**Mit jelent:** *golden dataset*, *gold set*, *reference set* — válogatott tesztkészlet: minden eleme egy bemenet (pl. kérdés) és egy **szakértő által átnézett** helyes válasz vagy megfelelési feltétel. A „golden” jelző a bizalomra utal, nem a méretre.\
**Hol fordul elő:** a kísérleti szakasz első hetének terméke; minden iteráció és a PoC-kapu ebből mér; élesítés után a hibákból bővül.\
**Hogyan olvasd:** egy golden set-eredmény csak a **készlet verziójával** együtt értelmes (melyik verzión futott). Nézd meg az összetételt is: hány elem fedi a nehéz eseteket (kétértelmű, többrészes, rossz nyelvű, támadó kérdés).\
**Tipikus félreolvasás:** a nagy elemszámot minőségnek tekinteni. A forrás szerint 100 változatos elem többet ér 1000 majdnem egyformánál, és a könnyű készlet „örökké 95%-ot ad”.\
**Lásd:** [Regression testing](#regression-testing), [Dataset drift](#dataset-drift), [05](05-meres-es-ertekeles.md), F-16.

### Human evaluation
**Mit jelent:** emberi értékelés: szakterületi átnéző ítéli meg a válaszokat (helyes-e, hiánytalan-e, megfelel-e a szabályzatnak). Drága és lassú, de ez a mérce, amelyhez az automatikus pontozást igazítjuk.\
**Hol fordul elő:** a golden set referenciaválaszainak jóváhagyásánál, és szúrópróbaként minden nagyobb mérésnél az LLM-bíró kalibrálására.\
**Hogyan olvasd:** jelöld, hány ember és hány elemen értékelt; két átnéző egyezése (mennyire értenek egyet) maga is információ — ha ők sem egyeznek, a kérdés vagy a szabály kétértelmű.\
**Tipikus félreolvasás:** egyetlen ember benyomását „emberi értékelésnek” nevezni. Mintavétel, rögzített szempontok és jegyzőkönyv kell.\
**Lásd:** [LLM-as-a-judge](#llm-as-a-judge), F-16, F-18.

### LLM-as-a-judge
**Mit jelent:** egy (erős) LLM pontozza egy másik rendszer válaszait előre megadott szempontok szerint. Olcsóvá és gyorssá teszi a sok esetes mérést; a Ragas-mutatók egy része (pl. faithfulness) is így számol.\
**Hol fordul elő:** a kísérleti szakasz minden iterációjában, a regressziós mérésnél.\
**Hogyan olvasd:** a bíró ítélete becslés, nem tény. Egy NeurIPS 2023-as tanulmány szerint az erős bírák 80% felett egyeznek az emberekkel — ennyire egyeznek az emberek is egymással —, de kimutatható torzításaik vannak.\
**Tipikus félreolvasás:** a bírót ellenőrizetlenül elfogadni. Ismert torzításai: az elsőként látott válaszra (*position bias*), a hosszabb válaszra (*verbosity bias*) és a saját válaszára (*self-enhancement bias*) hajlik — ezért emberi szúrópróbával kell kalibrálni.\
**Lásd:** [Human evaluation](#human-evaluation), [Faithfulness](#faithfulness), F-18.

### Regression testing
**Mit jelent:** regressziós tesztelés: minden változtatás után ugyanazt a tesztkészletet újrafuttatjuk, hogy kiderüljön, nem romlott-e el valami, ami korábban működött.\
**Hol fordul elő:** a kísérleti szakaszban minden iteráció végén, és élesítés után minden prompt-, modell- vagy adatváltozásnál.\
**Hogyan olvasd:** az összpontszám mellett mindig nézd az **esetenkénti** változást: egy javuló átlag mögött is lehet néhány korábban jó, most rossz eset.\
**Tipikus félreolvasás:** csak az új funkciót tesztelni. LLM-nél egy apró promptváltozás a nem érintett feladatokat is elrontja.\
**Lásd:** [Eval-driven development](#eval-driven-development), F-10.

## Mutatók

### Answer relevancy
**Mit jelent:** *response relevancy* — mennyire a feltett kérdésre felel a válasz. A Ragas a válaszból visszafelé generált kérdések és az eredeti kérdés hasonlóságából számolja.\
**Hol fordul elő:** a kísérleti szakaszban, a válaszadás diagnosztikájához.\
**Hogyan olvasd:** jellemzően 0–1, nagyobb jobb (a skála matematikailag nem garantált). Alacsony érték: a válasz kitér, mellébeszél vagy túl általános.\
**Tipikus félreolvasás:** **pontosságmutatónak** tekinteni. A Ragas dokumentációja kifejezetten rögzíti, hogy a tényszerű pontosságot nem méri — egy magabiztos, a kérdésre pontosan illeszkedő, de hamis válasz is magas pontot kaphat.\
**Lásd:** [Faithfulness](#faithfulness), F-17.

### Context precision
**Mit jelent:** a keresés a releváns szövegrészeket rangsorolja-e a lista elejére. A Ragas a rangsor egyes pozícióira számolt pontosság (*precision@k*) átlagaként számolja, referenciaválasz alapján.\
**Hol fordul elő:** a kísérleti szakasz keresés-diagnosztikájában.\
**Hogyan olvasd:** 0–1, nagyobb jobb. Alacsony érték jó recall mellett: a lényeg megvan, de sok a zaj, és hátul van — ez rontja a válaszadást.\
**Tipikus félreolvasás:** a recall-lal összekeverni. A precision a zajról és a sorrendről szól, a recall a hiányról.\
**Lásd:** [Context recall](#context-recall), [Chunk](#chunk), F-17.

### Context recall
**Mit jelent:** a helyes válaszhoz szükséges információból mennyit talált meg a keresés: a referenciaválasz állításai közül hány vezethető vissza a megtalált szövegre / összes állítás. Ragas-definíció; referenciaválasz kell hozzá.\
**Hol fordul elő:** a kísérleti szakasz keresés-diagnosztikájában; ha alacsony, a hiba a keresésben van, nem a modellben.\
**Hogyan olvasd:** 0–1, nagyobb jobb. Ez az első mutató, amit nézni kell: ha a szükséges információ nincs a találatok közt, a válaszadás nem javítható promptolással.\
**Tipikus félreolvasás:** alacsony recallnál a promptot vagy a modellt cserélni. A javítás helye a dokumentum-előkészítés, a darabolás vagy a keresés beállítása.\
**Lásd:** [Context precision](#context-precision), [Faithfulness](#faithfulness), F-17.

### Correct refusal rate
**Mit jelent:** helyes elutasítás aránya: azokból a kérdésekből, amelyekre a dokumentumtár **nem** tartalmaz választ, hányra mondja a rendszer, hogy „erre nem találtam forrást”. Saját mutató, a golden set erre szánt elemein mérve.\
**Hol fordul elő:** a PoC-kapu kritériumai között.\
**Hogyan olvasd:** 0–100%, nagyobb jobb — de mindig a **téves elutasítással** együtt nézd (amikor lenne válasz, mégis elutasít): a kettő egymás rovására javítható.\
**Tipikus félreolvasás:** csak ezt optimalizálni: egy mindenre „nem tudom”-ot mondó rendszer 100%-os, és használhatatlan.\
**Lásd:** [Faithfulness](#faithfulness), [05](05-meres-es-ertekeles.md).

### Faithfulness
**Mit jelent:** a válasz állításai közül hány támasztható alá a **megtalált** szövegrészekkel: alátámasztott állítások száma / összes állítás. Ragas-definíció.\
**Hol fordul elő:** a kísérleti szakasz fő minőségi mutatója; a PoC-kapu egyik kritériuma.\
**Hogyan olvasd:** 0–1, nagyobb jobb. A 0,9 azt jelenti, hogy a válasz állításainak 90%-a visszavezethető a megtalált forrásra — a maradék 10% a modell „kiegészítése”, vagyis potenciális hallucináció. Gyanús, ha a faithfulness kiugróan magas, miközben a context recall alacsony: a válasz hű, csak rossz forráshoz.\
**Tipikus félreolvasás:** a magas faithfulnesst helyes válasznak olvasni. Csak a **megtalált** szöveghez mért hűséget méri; ha a keresés rossz dokumentumot hozott, a válasz hű és mégis hibás lehet.\
**Lásd:** [Context recall](#context-recall), [LLM-as-a-judge](#llm-as-a-judge), F-17.

### Latency
**Mit jelent:** válaszidő: a kérdés elküldésétől a válasz megérkezéséig eltelt idő. Jellemzően percentilisben adják meg: a **p95** az az érték, amelynél a válaszok 95%-a gyorsabb.\
**Hol fordul elő:** a PoC-kapunál és élesítés után a monitorozásban.\
**Hogyan olvasd:** kisebb jobb. A p95 a „rossz napot” mutatja: ha az átlag 3 s, de a p95 15 s, minden huszadik kérdés frusztráló.\
**Tipikus félreolvasás:** az átlagot nézni. Az átlag elrejti a lassú eseteket, amelyek miatt a felhasználók elhagyják az eszközt.\
**Lásd:** [05](05-meres-es-ertekeles.md).

### Permission leakage
**Mit jelent:** jogosultság-szivárgás: hány esetben kap a felhasználó választ (vagy forrásmegjelölést) olyan dokumentumból, amelyet a SharePointban nem láthatna. Saját mutató, célzott tesztesetekkel mérve (különböző jogosultságú tesztfelhasználók).\
**Hol fordul elő:** a PoC-kapu **kizáró** kritériuma; élesítés után minden jogosultsági vagy indexelési változásnál újramérve.\
**Hogyan olvasd:** darabszám, a cél **0**. Itt nincs zöld/sárga sáv: egyetlen eset is leállítja az élesítést, és azonnali beavatkozást indít.\
**Tipikus félreolvasás:** százalékban kifejezni és „elég alacsonynak” tekinteni. Egy szivárgás is adatvédelmi incidens lehet.\
**Lásd:** [Kill criteria](#kill-criteria), [GDPR](#gdpr), F-15.

### Pilot-to-production rate
**Mit jelent:** a pilotok (vagy PoC-k) közül élesbe jutók aránya. Az MIT szerint a feladatspecifikus GenAI-eszközöknél 20% pilot mellett 5% sikeres bevezetés; az S&P szerint a PoC-k átlagosan 46%-a áll le élesítés előtt.\
**Hol fordul elő:** a [02](02-miert-buknak-el-az-ai-projektek.md) fejezetben; portfólió-szinten a kapuk működésének mérésére.\
**Hogyan olvasd:** önmagában se nem jó, se nem rossz: a 100% azt jelentheti, hogy a kapu nem szűr. A kérdés az, hogy a leállítás **mikor és mennyi költség után** történik.\
**Tipikus félreolvasás:** az alacsony arányt kudarcnak olvasni. Ha a leállítások korán, olcsón és mérés alapján születnek, az egészséges portfólió jele.\
**Lásd:** [PoC](#poc), [Kill criteria](#kill-criteria), F-04, F-07.

### Project performance rate
**Mit jelent:** a PMI Pulse-jelentések összesített mutatója: a projektek hány százaléka érte el
az üzleti céljait. 2024-ben a válaszadók átlaga 73,8% (F-01).\
**Hol fordul elő:** a [01](01-hibrid-a-piacon.md) fejezetben, a megközelítések összevetésénél.\
**Hogyan olvasd:** nagyobb jobb, de **önbevallás**: a válaszadó ítéli meg a saját projektjét.
Összehasonlításra (szervezetek, évek, megközelítések között) alkalmas, abszolút sikerarányként nem.\
**Tipikus félreolvasás:** „a projektek 74%-a sikeres”. Pontosabban: a válaszadók átlagosan úgy
ítélik meg, hogy a projektjeik ennyi része érte el a céljait.\
**Lásd:** F-01.
