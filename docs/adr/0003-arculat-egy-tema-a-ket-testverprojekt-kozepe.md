# ADR 0003 — Arculat: egyetlen világos téma, a pm_all és az sm_all színeinek közepe

**Állapot:** elfogadva (Tibor, 2026-11-05).

## Kontextus

A `PROJ_pm_all` meleg, terrakotta kiemelésű arculatot használ, a `PROJ_sm_all` zöldes, jáde
kiemelésűt (ADR 0008 ott), mindkettő egyetlen világos témával. A harmadik modell a kettő
közé esik, ezért saját arculatot kap. A `~/CLAUDE.md` világos és sötét ellenőrzést kér; a két
testvérprojekt egyetlen szemkímélő, nem vakító háttérrel elégséges, sötét mód nélkül.

## Döntés

- **Egyetlen világos téma** (`.streamlit/config.toml`, nincs `[theme.dark]`).
- **A színek a két testvérarculat csatornánkénti számtani közepe** (`hibrid_app/szinek.py`):
  kiemelés `#606243` (olajzöld-khaki), szöveg `#242722`, háttér `#f0f1eb`, második háttér
  `#e4e5dc`, keret `#d1d4c8`, oldalsáv `#e7e8de`, info-doboz `#265862` / `#ddeae6`.
- **A jelentést hordozó színek** (piros, narancs) nem a közép, hanem a pm_all jelentésszínei.
- **Az ábrák** a palettából készülnek (az élek a szöveg és a kiemelés közepe, a kapuk háttere
  a kiemelés fehérrel kevert változata), vastagabb vonallal.
- **Kontraszt számolva** (WCAG 2.1, `tests/test_szinek.py`): a kiemelés legalább 4,5:1 minden
  felületen (a legkisebb érték 4,97:1), a szöveg legalább 7:1.

## Következmények

- A színek egy helyen vannak; a `config.toml` és a teszt ezt követi, a régi terrakotta nem maradhat
  a kódban (teszt őrzi).
- A **Xyo-mintadokumentumok** (később) és a minták arculatát ehhez a palettához igazítjuk.
- Ha a paletta változik, a `test_a_rogzitett_ertekek` jelzi; az ADR-t is frissíteni kell.
- A közép halványabb, mint a két forrásarculat; ha a kiemelés túl visszafogott, csak a
  `kiemeles` értéke hangolandó (a kontrasztkorlát: legalább 4,5:1).
