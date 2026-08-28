# Katalog projektów — system pamięci dla Twojego agenta AI (plugin Claude Code)

[![licencja MIT](https://img.shields.io/github/license/studiogo/katalog-projektow?style=flat-square)](LICENSE)
[![ostatnia zmiana](https://img.shields.io/github/last-commit/studiogo/katalog-projektow?style=flat-square)](https://github.com/studiogo/katalog-projektow/commits/main)
![Claude Code](https://img.shields.io/badge/Claude%20Code-wtyczka-D97757?style=flat-square)

Porządek na wszystkie Twoje projekty w zwykłych plikach `.md`: mapa wszystkiego, katalog
projektów, graf, który zobaczysz w Obsidianie, i strażnik, który pilnuje porządku. Dla osób
nietechnicznych. Bez kluczy API, bez kosztów zewnętrznych. Wszystko na Twoim dysku.

## Po co to — na liczbach

Gdy pracujesz na kilku projektach naraz i pytasz agenta „czy projekt X jest gotowy do
wysłania klientowi", on szuka po omacku i czyta kupę plików — a każdy plik to spalone tokeny.
Ten system łączy projekty **po znaczeniu** (newsletter ↔ klient, dla którego coś robisz — nie
„wszystkie strony www do jednej szuflady"), więc agent od razu wie, gdzie zajrzeć.

Zmierzone u autora, na **51 projektach**, na pytaniu „z czym łączy się ten projekt":

| | Bez systemu | Z systemem |
|---|---|---|
| **Zużycie tokenów** | 86 tys. | **54 tys. (−37%)** |
| **Błądzenie po plikach** | 13 zajrzeń | **1 zajrzenie (−92%)** |
| **Trafił we właściwe projekty** | 4 z 8 (50%) | **8 z 8 (100%)** |

To wynik u autora — Twój zależy od tego, ile masz projektów i jak gęsto się przeplatają. Ale
kierunek jest zawsze ten sam: mniej szukania, mniej tokenów, celniej.

## Co dostajesz
- **Struktura projektów** — każdy projekt to katalog: bieżący stan (`HANDOFF.md`), ustalenia, plan.
- **Cienka mapa** (`MEMORY.md`) — same drogowskazy: nazwa + jedno zdanie + link.
- **Powiązania po znaczeniu** — skaner czyta Twoje notatki i łączy projekty tam, gdzie jeden
  naprawdę odwołuje się do drugiego (z dowodem: plik i linia). Agent czyta gotową listę
  powiązań z jednego pliku, zamiast przeszukiwać wszystko. To stąd bierze się oszczędność wyżej.
- **Graf projektów** — otwierasz folder w Obsidianie i widzisz, co z czym się łączy.
- **Strażnik porządku** — pilnuje formatu mapy i ostrzega, jeśli hasło trafi do pliku.
- **Kreator** — przeprowadzi Cię przez pierwszy setup krok po kroku.

## Czego potrzebujesz
- **Claude Code** (sprawdź `/version`).
- **Python** — opcjonalnie, tylko do strażnika porządku. Bez niego reszta działa. (Windows: `winget install Python.Python.3.12`.)
- **Obsidian** — opcjonalnie, darmowy, do oglądania grafu.

## Instalacja
Komendy z `/` wpisujesz w **Claude Code**.

1. `/plugin marketplace add studiogo/katalog-projektow`
2. `/plugin install`
3. **Zrestartuj Claude Code** (zamknij i otwórz albo wpisz `/reload-plugins`). Bez tego strażnik porządku się nie włączy — hooki wczytują się dopiero po restarcie.
4. `/zainstaluj-katalog` — kreator zrobi resztę: założy strukturę i zapyta o Twoje projekty. Masz już bałagan na dysku? Wybierzesz w nim „mam już pliki", a kreator je zeskanuje i ułoży za Ciebie.

## Komendy
| Komenda | Do czego |
|---|---|
| `/zainstaluj-katalog` | Pierwszy setup (kreator) — raz na start |
| `/importuj-projekty` | Zeskanuj istniejące katalogi i zrób z nich projekty (mapa + huby + linki). Plików nie przenosi |
| `/nowy-projekt` | Dodaj nowy projekt (katalog + węzeł grafu + wpis w mapie) |
| `/polacz-projekty` | Połącz pokrewne projekty w graf |
| `/koniec` | Zapisz stan projektu na koniec pracy (teczka + ustalenia + mapa) |
| `/sprawdz-pamiec` | Sprawdź porządek (format, martwe linki, hasła w plikach) |

## Graf w Obsidianie
Otwórz folder `~/.claude/pamiec/` (Windows: `%USERPROFILE%\.claude\pamiec`) w Obsidianie:
**Open folder as vault** → włącz **Graph View**. W ustawieniach grafu wyłącz **„Show orphans"**,
żeby widzieć tylko połączone projekty (bez luźnych plików-kropek).

## Twarde zasady pracy (opcjonalnie)
Jeśli chcesz, żeby agent trzymał się Twoich reguł w każdej wiadomości, jest osobny, publiczny
plugin **`studiogo/kaganiec`**. Kreator zapyta, czy go dołożyć. Uwaga: wstrzykuje reguły do każdej
wiadomości, więc nieco szybciej zużywa limity (szczegóły w `KOSZT.md` tamtego pluginu).

## Gdzie co leży
- Twoja pamięć: `~/.claude/pamiec/` — `MEMORY.md`, `projects/`, `rules/schemat-mapy.md`.
- Mechanizmy (nie ruszasz): ten plugin — `hooks/`, `bin/`, `commands/`, `templates/`.

## Windows

Instalację na Windowsie sprawdzisz listą kontrolną w [WINDOWS-TEST.md](WINDOWS-TEST.md) — przechodzi przez kreator krok po kroku i mówi, które katalogi mają powstać.

## Coś nie działa albo masz pomysł

[Załóż zgłoszenie](https://github.com/studiogo/katalog-projektow/issues/new/choose) — są trzy szablony: błąd, kłopot na Windowsie i pomysł. Podaj system, terminal i wersję Pythona; bez tego trudno cokolwiek odtworzyć.

Nie wklejaj treści swoich plików pamięci — trzymają nazwy klientów i stan projektów. Zasady zgłaszania: [CONTRIBUTING.md](CONTRIBUTING.md).

## Licencja

MIT — [LICENSE](LICENSE).
