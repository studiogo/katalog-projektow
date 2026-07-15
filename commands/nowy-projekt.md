---
description: Tworzy nowy projekt w pamięci — katalog ze skeletonu, węzeł grafu, wpis w mapie i katalogu.
---

Utwórz nowy projekt w pamięci użytkownika. Ścieżka bazowa: `~/.claude/pamiec/`.

Wykonaj DOKŁADNIE:
1. Ustal z użytkownikiem: **nazwę** projektu (krótka, bez spacji — myślniki, np. `sklep-ania`) i **jedno zdanie** opisu.
2. Sprawdź, czy `projects/<nazwa>/` już istnieje. Jeśli tak — nie twórz drugi raz, powiedz o tym.
3. Skopiuj szablon `projects/_TEMPLATE/` → `projects/<nazwa>/`. W plikach zamień `{NAZWA PROJEKTU}` na tytuł i `{DATA}` na dzisiejszą datę.
4. Utwórz węzeł grafu `projects/<nazwa>/<nazwa>.md` z `_TEMPLATE/HUB.md`: zamień `NAZWA_PROJEKTU`→`<nazwa>`, `DATA_UTWORZENIA`→dzisiejsza data, `TYTUL_PROJEKTU`→tytuł. Zapisz przez terminal (`>`), nie edytorem.
5. Dodaj wpis do `projects/index.md` (sekcja „Moje projekty"): `- [[<nazwa>]]: <opis ≤150 znaków>. \`<nazwa>/<nazwa>.md\``
6. Dodaj wpis do `MEMORY.md` (sekcja `## Aktywne`) wg `rules/schemat-mapy.md`: `- [[<nazwa>]] — <jedno zdanie ≤140 znaków, bez emoji, bez dat i numerów>`
7. Powiedz prosto: co powstało; że szczegóły (daty, numery) wpisujesz do `HANDOFF.md` projektu, a mapa ma tylko jedno zdanie; że graf zobaczysz w Obsidianie.
