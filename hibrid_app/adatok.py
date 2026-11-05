"""A Xyo-példa számai egy helyen.

Forrás: `koncepcio/04-xyo-pelda.md` és `koncepcio/02-meresi-rendszer.md`. Minden szám
**feltevés** (kitalált, de valószerű projekt). A `tests/test_adatok.py` ellenőrzi, hogy az itteni
értékek egyeznek a dokumentumok szövegével, ezért a számot csak a dokumentumban és itt együtt
szabad módosítani.
"""

from dataclasses import dataclass
from datetime import date

HONAPOK = (
    "január", "február", "március", "április", "május", "június",
    "július", "augusztus", "szeptember", "október", "november", "december",
)  # fmt: skip


# --- formázás (magyar írásmód, mint a dokumentumokban) -------------------------------------


def szam(x: float, tizedes: int = 2) -> str:
    """Tizedesvessző: 0,84."""
    return f"{x:.{tizedes}f}".replace(".", ",")


def ezres(n: int) -> str:
    """Szóközös ezres tagolás: 77 280."""
    return f"{n:,}".replace(",", " ")


def ft(n: int) -> str:
    return f"{ezres(n)} Ft"


def ido(mp: int) -> str:
    """Másodpercből „6 perc 30 mp”."""
    perc, mp = divmod(mp, 60)
    return f"{perc} perc {mp} mp"


def datum(d: date, evvel: bool = True) -> str:
    """„2027. január 8.” (évvel) vagy „január 8.” (anélkül)."""
    nap = f"{HONAPOK[d.month - 1]} {d.day}."
    return f"{d.year}. {nap}" if evvel else nap


# --- a cég és a baseline -------------------------------------------------------------------

LETSZAM = 240
PILOT_FO = 50
KITERJESZTES_FO = 190  # a három hullám együtt
KERESES_HETENTE = 7  # egy főre (kérdőív)
MUNKAHETEK = 46
KERESES_EVENTE = LETSZAM * KERESES_HETENTE * MUNKAHETEK  # 77 280

T0_MEDIAN_MP = 6 * 60 + 30  # 6 perc 30 mp (MK-08, december 7–11.)
T1_MEDIAN_MP = 3 * 60 + 50  # 3 perc 50 mp (a pilot T1-mérése)
CEL_CSOKKENES = 0.30  # sikerkritérium: a medián feladatidő ≥ 30%-os csökkenése
JEGY_HAVONTA = 85  # „hol találom?” jegyek a Service Desken
WAU_CEL = 0.50  # heti aktív felhasználók a 8. héten
WAU_T1 = 0.58

# --- költségkeretek (Ft) -------------------------------------------------------------------

POC_KERET = 6_500_000
POC_TARTALEK = 900_000
BEVEZETESI_KERET = 9_800_000  # csak G1 go esetén szabadul fel
FUTASI_KERET_EVES = 3_600_000
KOLTSEG_KERDESENKENT_HATAR = 46  # Ft; a futási keret / éves kérdésszám egész része
PIVOT_KOLTSEG = 850_000  # a PoC-keret tartalékából
KISERLETI_TELJES_KOLTSEG = 6_300_000

# --- a golden set (02, 2.2) ----------------------------------------------------------------

GOLDEN_MEGVALASZOLHATO = 24
GOLDEN_ELUTASITANDO = 8
GOLDEN_NEHEZ = 8
GOLDEN_OSSZESEN = GOLDEN_MEGVALASZOLHATO + GOLDEN_ELUTASITANDO + GOLDEN_NEHEZ  # 40
JOGOSULTSAGI_ESETEK = 12  # 3 tesztfelhasználó × 4 kérdés
OCR_PDF_DB = 112  # a pivotban feldolgozott szkennelt PDF-ek
ARCHIVALT_DOKUMENTUM = 37  # a 3. iterációban archivált elavult dokumentumok
KISERLETI_DOKUMENTUM = 1_900  # a kísérleti szakasz négy tárában, kb.

# --- a kísérleti szakasz mérései -------------------------------------------------------------------------


@dataclass(frozen=True)
class Meres:
    """Egy mérés a golden seten. A mutatók értelmezése: `kutatas/tudasbazis.md`."""

    faithfulness: float
    context_recall: float
    context_precision: float | None  # diagnosztika; a pivot utáni mérésben nem szerepel
    helyes_elutasitas: int  # az 8 elutasítandóból
    teves_elutasitas: int  # a 24 megválaszolhatóból
    szivargas: int  # a 12 jogosultsági esetből
    latency_p95_s: float
    koltseg_ft: int  # kérdésenként


ITERACIOK = (
    Meres(0.78, 0.66, 0.58, 5, 1, 0, 11.2, 52),  # 0. iteráció: baseline
    Meres(0.84, 0.81, 0.71, 5, 1, 0, 9.6, 48),  # 1. darabolás
    Meres(0.92, 0.81, 0.71, 7, 3, 0, 9.8, 49),  # 2. „csak a forrásból”
    Meres(0.92, 0.84, 0.79, 8, 2, 0, 7.4, 41),  # 3. elavult változatok, kevesebb találat
)
PIVOT_UTAN = Meres(0.91, 0.88, None, 8, 2, 0, 7.8, 42)

# --- a bevezetési ág hullámai (04, 4.6) ----------------------------------------------------


@dataclass(frozen=True)
class Hullam:
    nev: str
    fo: int
    tervezett: date
    tenyleges: date


HULLAMOK = (
    Hullam("Pilot", PILOT_FO, date(2027, 4, 5), date(2027, 4, 5)),
    Hullam("1. hullám", 60, date(2027, 5, 3), date(2027, 5, 3)),
    Hullam("2. hullám", 65, date(2027, 7, 5), date(2027, 7, 19)),  # G2-halasztás
    Hullam("3. hullám", 65, date(2027, 10, 4), date(2027, 10, 4)),
)

# --- kapudátumok ---------------------------------------------------------------------------

G0_ELSO = date(2026, 12, 18)  # hiánypótlás
G0_MASODIK = date(2027, 1, 8)  # go
KISERLETI_KEZDET = date(2027, 1, 11)
KISERLETI_VEG = date(2027, 2, 26)
G1 = date(2027, 3, 3)  # pivot
G1_MASODIK = date(2027, 3, 19)  # go
ZARAS = date(2027, 11, 30)
