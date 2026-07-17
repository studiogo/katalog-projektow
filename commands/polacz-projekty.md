---
description: Łączy projekty w graf — dodaje dwukierunkowe [[Powiązane]] między pokrewnymi projektami.
---

Połącz projekty powiązane po SENSIE (wspólny klient, temat, obszar). Ścieżka: `~/.claude/pamiec/`.

Wykonaj:
1. Przeczytaj `projects/index.md` — to spis wszystkich projektów.
2. Jeśli użytkownik wskazał projekt: znajdź dla niego 3–8 kandydatów z **realnym** pokryciem tematu (nie samo podobne słowo — realny wspólny sens). Jeśli nie wskazał: zaproponuj pary, które widzisz.
3. Potwierdź z użytkownikiem, zanim zapiszesz.
4. Dla każdej pary dodaj `[[link]]` w OBIE strony — w sekcji `## Powiązane` obu węzłów (`projects/<A>/<A>.md` i `projects/<B>/<B>.md`). Nie zmieniaj innej treści.
5. Pokaż, co połączyłeś.

Zasada: łącz po sensie, nie po przypadkowym wspólnym słowie. Graf zobaczysz, otwierając `~/.claude/pamiec/` w Obsidianie (Graph View).

Dla wielu projektów naraz uruchom skaner, który sam znajdzie powiązania z treści notatek (bez ręcznego wpisywania):
- `python3 "${CLAUDE_PLUGIN_ROOT}/bin/przelot-linkera.py" --dry-run` — pokaże, co znalazł i skąd (plik:linia), nic nie zapisze.
- `python3 "${CLAUDE_PLUGIN_ROOT}/bin/przelot-linkera.py"` — wpisze powiązania do hubów.
- `python3 "${CLAUDE_PLUGIN_ROOT}/bin/przelot-linkera.py" --pokaz-dowody NAZWA` — pokaże, skąd wzięło się każde powiązanie danego projektu.
Skaner łączy tylko tam, gdzie jeden projekt naprawdę odwołuje się do drugiego w treści — nie zgaduje.
