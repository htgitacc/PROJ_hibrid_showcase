"""A G1 (PoC-kapu) döntési szabályai tiszta függvényekként.

Forrás: `koncepcio/01-kapuk-es-kill-criteria.md`, 1.3 (sávok, döntési szabályok, kill criteria) és
`koncepcio/02-meresi-rendszer.md`, MK-03 (a téves elutasítás feltétele). A küszöbök a Xyo-példa
**feltevései**; a `tests/test_kapu.py` ellenőrzi, hogy egyeznek a 01 táblájával.

Értelmezési döntések, ahol a dokumentum nem mond ki mindent:

* **Leakage:** a végső mérésben mért szivárgás (≥ 1) a kizáró mutatót pirosra állítja. Pivot csak
  zöld kizáró mutatónál van, ezért ez mindig no-go (kill criterion 1). A javítható szivárgás
  kezelése nem a G1 dolga: javítás után új végső mérés kell.
* **Correct refusal:** a sáv a helyes elutasítás arányából jön; ha a téves elutasítás > 10%
  (MK-03), a sáv nem lehet zöld, ezért legfeljebb sárga.
* **Hibahely és adatminőség:** hogy a hiba helye azonosított-e, és hogy a recall tartós hibájának
  oka az adat minősége-e, emberi ítélet (iterációs napló): a hívó adja meg.
* **Pivot csak egyszer:** ha a pivot már megvolt, a pivot kimenet nem választható.
"""

from dataclasses import dataclass

from hibrid_app import adatok

ZOLD, SARGA, PIROS = "zöld", "sárga", "piros"

KIZARO, KRITIKUS, TAMOGATO, DIAGNOSZTIKA = "kizáró", "kritikus", "támogató", "csak diagnosztika"

GO, PIVOT, NO_GO = "go", "pivot", "no-go"

# --- küszöbök (01, 1.3) --------------------------------------------------------------------

FAITHFULNESS_ZOLD, FAITHFULNESS_SARGA = 0.90, 0.80  # zöld ≥ 0,90 · sárga ≥ 0,80 · alatta piros
RECALL_ZOLD, RECALL_SARGA = 0.85, 0.70
REFUSAL_ZOLD, REFUSAL_SARGA = 0.90, 0.80  # arány (90%, 80%)
TEVES_ELUTASITAS_MAX = 0.10  # MK-03: zöldhöz legfeljebb 10% téves elutasítás
LATENCY_ZOLD_S, LATENCY_SARGA_S = 8, 15  # zöld ≤ 8 s · sárga ≤ 15 s · fölötte piros
KOLTSEG_ZOLD_SZAZALEK, KOLTSEG_SARGA_SZAZALEK = 100, 120  # a futási keret %-ában


@dataclass(frozen=True)
class Mutato:
    kulcs: str
    nev: str
    szerep: str


MUTATOK = (
    Mutato("leakage", "Permission leakage", KIZARO),
    Mutato("faithfulness", "Faithfulness", KRITIKUS),
    Mutato("recall", "Context recall", KRITIKUS),
    Mutato("refusal", "Correct refusal rate", KRITIKUS),
    Mutato("latency", "Latency p95", TAMOGATO),
    Mutato("koltseg", "Éves futási költség", TAMOGATO),
)
SZEREP = {m.kulcs: m.szerep for m in MUTATOK}
NEV = {m.kulcs: m.nev for m in MUTATOK}
KRITIKUS_KULCSOK = tuple(m.kulcs for m in MUTATOK if m.szerep == KRITIKUS)
TAMOGATO_KULCSOK = tuple(m.kulcs for m in MUTATOK if m.szerep == TAMOGATO)

KILL_CRITERIA = {
    1: "jogosultság-szivárgás a végső mérésben",
    2: "bármelyik kritikus mutató piros a végső mérésben",
    3: "a pivot után is van nem zöld kritikus mutató",
    4: "az éves futási költség a keret 120%-a fölött van, és nincs olcsóbb változat",
    5: "a context recall tartósan nem zöld, és az ok az adat minősége",
}


# --- sávok ---------------------------------------------------------------------------------


def sav_leakage(esetek: int) -> str:
    return ZOLD if esetek == 0 else PIROS  # nincs sárga sáv


def sav_faithfulness(x: float) -> str:
    return ZOLD if x >= FAITHFULNESS_ZOLD else SARGA if x >= FAITHFULNESS_SARGA else PIROS


def sav_recall(x: float) -> str:
    return ZOLD if x >= RECALL_ZOLD else SARGA if x >= RECALL_SARGA else PIROS


def sav_refusal(
    helyes: int,
    teves: int,
    elutasitando: int = adatok.GOLDEN_ELUTASITANDO,
    megvalaszolhato: int = adatok.GOLDEN_MEGVALASZOLHATO,
) -> str:
    arany = helyes / elutasitando
    sav = ZOLD if arany >= REFUSAL_ZOLD else SARGA if arany >= REFUSAL_SARGA else PIROS
    if sav == ZOLD and teves / megvalaszolhato > TEVES_ELUTASITAS_MAX:
        return SARGA  # a téves elutasítás miatt nem lehet zöld
    return sav


def sav_latency(masodperc: float) -> str:
    return ZOLD if masodperc <= LATENCY_ZOLD_S else SARGA if masodperc <= LATENCY_SARGA_S else PIROS


def sav_koltseg(eves_koltseg: int, keret: int = adatok.FUTASI_KERET_EVES) -> str:
    """Egész számokkal, hogy a határérték (100%, 120%) pontos legyen."""
    if eves_koltseg * 100 <= keret * KOLTSEG_ZOLD_SZAZALEK:
        return ZOLD
    return SARGA if eves_koltseg * 100 <= keret * KOLTSEG_SARGA_SZAZALEK else PIROS


def savok(
    m: adatok.Meres,
    eves_koltseg: int,
    keret: int = adatok.FUTASI_KERET_EVES,
    elutasitando: int = adatok.GOLDEN_ELUTASITANDO,
    megvalaszolhato: int = adatok.GOLDEN_MEGVALASZOLHATO,
) -> dict[str, str]:
    """Mutatónként a sáv (a `MUTATOK` kulcsaival)."""
    return {
        "leakage": sav_leakage(m.szivargas),
        "faithfulness": sav_faithfulness(m.faithfulness),
        "recall": sav_recall(m.context_recall),
        "refusal": sav_refusal(m.helyes_elutasitas, m.teves_elutasitas, elutasitando, megvalaszolhato),
        "latency": sav_latency(m.latency_p95_s),
        "koltseg": sav_koltseg(eves_koltseg, keret),
    }


# --- döntés --------------------------------------------------------------------------------


@dataclass(frozen=True)
class Dontes:
    kimenet: str  # GO / PIVOT / NO_GO
    savok: dict[str, str]
    kill: tuple[int, ...]  # a teljesülő kill criteriák száma (01, 1.3)
    indoklas: tuple[str, ...]


def eves_koltseg(m: adatok.Meres, kerdes_evente: int = adatok.KERESES_EVENTE) -> int:
    """Becsült éves futási költség: a kérdésenkénti költség × az éves kérdésszám."""
    return m.koltseg_ft * kerdes_evente


def g1_dontes(
    m: adatok.Meres,
    *,
    eves_koltseg: int,
    keret: int = adatok.FUTASI_KERET_EVES,
    pivot_volt: bool = False,
    hiba_helye_azonositott: bool = False,
    van_olcsobb_valtozat: bool = False,
    adatminoseg_a_recall_oka: bool = False,
    elutasitando: int = adatok.GOLDEN_ELUTASITANDO,
    megvalaszolhato: int = adatok.GOLDEN_MEGVALASZOLHATO,
) -> Dontes:
    """A G1-kapu döntése a mutatókból, a 01 szabályai szerint: go, pivot vagy no-go."""
    s = savok(m, eves_koltseg, keret, elutasitando, megvalaszolhato)
    kritikus = [s[k] for k in KRITIKUS_KULCSOK]

    kill = []
    if s["leakage"] != ZOLD:
        kill.append(1)
    if PIROS in kritikus:
        kill.append(2)
    if pivot_volt and any(x != ZOLD for x in kritikus):
        kill.append(3)
    if s["koltseg"] == PIROS and not van_olcsobb_valtozat:
        kill.append(4)
    if s["recall"] != ZOLD and adatminoseg_a_recall_oka:
        kill.append(5)

    def nev_lista(kulcsok):
        return ", ".join(NEV[k] for k in kulcsok)

    def kesz(kimenet, *indoklas, kill_lista=()):
        return Dontes(kimenet, s, tuple(kill_lista), tuple(indoklas))

    if kill:
        return kesz(NO_GO, *(f"Kill criterion {n}: {KILL_CRITERIA[n]}." for n in kill), kill_lista=kill)

    nem_zold_kritikus = [k for k in KRITIKUS_KULCSOK if s[k] != ZOLD]
    piros_tamogato = [k for k in TAMOGATO_KULCSOK if s[k] == PIROS]

    if not nem_zold_kritikus and not piros_tamogato:
        return kesz(GO, "A kizáró mutató zöld, minden kritikus mutató zöld, a támogatók legalább sárgák.")

    # Innen nem go. Pivot: egyszer, a kizáró zöld (itt már igaz), legfeljebb egy sárga kritikus,
    # és a hiba helye azonosított.
    gondok = []
    if nem_zold_kritikus:
        gondok.append(f"nem zöld kritikus mutató: {nev_lista(nem_zold_kritikus)}")
    if piros_tamogato:
        gondok.append(f"piros támogató mutató: {nev_lista(piros_tamogato)}")
    gond = "; ".join(gondok)

    if pivot_volt:
        return kesz(NO_GO, f"Nem go ({gond}), és a pivot már megvolt: pivot csak egyszer van.")
    if len(nem_zold_kritikus) > 1:
        return kesz(
            NO_GO,
            f"Nem go, és nem pivot: {len(nem_zold_kritikus)} kritikus mutató nem zöld ({gond}); "
            "pivot legfeljebb egy sárga kritikus mutatónál van.",
        )
    if not hiba_helye_azonositott:
        return kesz(NO_GO, f"Nem go ({gond}), és a hiba helye nem azonosított: pivot csak konkrét hipotézissel van.")
    return kesz(
        PIVOT,
        f"{gond[0].upper() + gond[1:]}; a hiba helye azonosított. Pivot: egyszer, legfeljebb 2 hét; "
        "ha utána nem zöld minden kritikus mutató, a döntés no-go (kill criterion 3).",
    )
