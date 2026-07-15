---
name: schemat-mapy
description: Format wpisu w MEMORY.md i projects/index.md. Czytany przez agenta i pilnowany przez strażnika porządku. Definiuje format wpisu, limity znaków, wymóg [[link]] i sekcje statusów.
type: schema
priority: high
---

# Format mapy pamięci

> Ten plik mówi, jak wygląda dobry wpis w mapie. Agent go czyta, a strażnik (hooki pluginu) pilnuje.

## Zasada główna
`MEMORY.md` to cienka **mapa wskaźników**, nie magazyn. Mówi tylko: co istnieje + jedno zdanie + `[[link]]`. Szczegóły (daty, liczby, ustalenia) trzymaj w `projects/<nazwa>/HANDOFF.md`.

## Wpis w MEMORY.md
```
- [[nazwa-projektu]] — jedno zdanie: czym projekt jest.
```
- **≤ 140 znaków** cała linia.
- **musi mieć** dokładnie jeden `[[link]]` (nazwa katalogu projektu).
- **bez emoji** — status wynika z sekcji.
- **bez** długich numerów, dat, ścieżek plikowych (te → HANDOFF projektu).
- jedno zdanie, bez akapitów.

## Status = sekcja (nie emoji)
- `## Priorytet` — najważniejsze teraz.
- `## Aktywne` — w toku.
- `## Czeka` — czeka na kogoś / decyzję.
- `## Zamknięte` — skończone / odłożone.

## Wpis w projects/index.md (pełny katalog)
```
- [[nazwa]]: opis do 150 znaków. `nazwa/nazwa.md`
```
`page_type: index`, sekcje po tematach. To źródło, z którego czyta łącznik projektów.

## Limity
- wpis MEMORY.md: ≤ 140 znaków
- wpis index.md: ≤ 150 znaków
- całość MEMORY.md: cel ≤ 18 KB, twardy limit ~24 KB

## Czego unikać
| Źle | Popraw |
|---|---|
| wpis bez `[[link]]` | dodaj `[[nazwa-projektu]]` |
| emoji we wpisie | usuń; status → sekcja |
| numer / data / ścieżka we wpisie | przenieś do HANDOFF |
| wpis dłuższy niż 140 znaków | zwiń do jednego zdania |
| martwy `[[link]]` (cel nie istnieje) | popraw nazwę albo utwórz projekt |

## Węzeł grafu
Każdy projekt ma plik-hub `projects/<nazwa>/<nazwa>.md` — to węzeł, który widać w grafie Obsidiana. Powiązania `[[Powiązane]]` między projektami buduje komenda `/polacz-projekty`.
