# Test na Windowsie

Krótka lista kontrolna, że plugin działa na Windowsie (Git Bash zalecany).

## Przed testem
- Claude Code zainstalowany, `/version` pokazuje wersję.
- (Opcjonalnie) Python: `winget install Python.Python.3.12` — do strażnika porządku.

## Kroki
1. `/plugin marketplace add studiogo/katalog-projektow` → `/plugin install`.
2. `/zainstaluj-katalog` — kreator zakłada `%USERPROFILE%\.claude\pamiec\`.
3. Sprawdź, że powstały: `pamiec\MEMORY.md`, `pamiec\projects\index.md`, `pamiec\projects\_TEMPLATE\`, `pamiec\rules\schemat-mapy.md`.
4. `/nowy-projekt` — dodaj testowy projekt; sprawdź, że powstał katalog + plik-węzeł `<nazwa>.md` + wpis w `MEMORY.md`.
5. `/sprawdz-pamiec` — jeśli masz Pythona, pokaże raport; jeśli nie, komenda to powie (reszta działa).
6. Otwórz `%USERPROFILE%\.claude\pamiec\` w Obsidianie → Graph View.

## Na co uważać (Windows)
- **Ścieżki**: plugin używa `$HOME` / `Path.home()` i stałego folderu `pamiec` — działa niezależnie od nazwy konta.
- **Znaki końca linii (CRLF)**: skrypty pluginu są tolerancyjne; jeśli edytujesz pliki, zapisuj jako UTF-8.
- **Python**: bez niego strażnik (`/sprawdz-pamiec`, hook porządku) jest cichy — reszta (projekty, mapa, graf) działa normalnie.
- **Polskie znaki**: pliki są w UTF-8; upewnij się, że terminal też.
