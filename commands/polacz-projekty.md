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

Dla wielu par naraz możesz też wpisać je w `${CLAUDE_PLUGIN_ROOT}/bin/przelot-linkera.py` (lista EDGES) i uruchomić ten skrypt.
