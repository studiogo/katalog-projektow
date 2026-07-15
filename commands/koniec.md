---
description: Zapisuje bieżący stan projektu na koniec pracy — teczkę, ustalenia i mapę — żebyś nie musiał o tym pamiętać. Wywołaj, gdy kończysz pracę nad projektem.
---

Zamykasz pracę — utrwal stan, żeby następnym razem wszystko było pod ręką. Prosty język, po polsku, na ty. Ścieżka pamięci: `~/.claude/pamiec/` (Windows: `%USERPROFILE%\.claude\pamiec`).

## Krok 1 — Który projekt
Ustal z rozmowy, nad którym projektem pracowaliście.
- Jasne → działaj na nim.
- Kilka projektów → wypisz i zapytaj, który zamykasz (albo „wszystkie").
- Niejasne → zapytaj wprost, zanim cokolwiek zapiszesz.

## Krok 2 — HANDOFF.md (bieżący stan)
W `projects/<nazwa>/HANDOFF.md` zapisz stan: co zrobione, co dalej, ważne numery/terminy/linki.
- To miejsce na **stan**, nie na wyjaśnienia „dlaczego" — te idą do `decyzje.md`.
- Popraw istniejące sekcje, nie doklejaj drugiej kopii stanu.

## Krok 3 — decyzje.md (co ustalone i dlaczego)
Jeśli zapadły jakieś ustalenia (wybór kierunku, ceny, terminu), dopisz je do `projects/<nazwa>/decyzje.md`:
- Format: `## D-RRRR-MM-DD-NN — tytuł`, pod spodem „Co:" i „Dlaczego:".
- Numer kolejny w danym dniu (zerknij na ostatni w pliku).
- Datę weź z dzisiejszego dnia.

## Krok 4 — MEMORY.md (mapa — tylko gdy zmienił się status)
Jeśli projekt zmienił status (np. skończony albo czeka na kogoś):
- Popraw jedno zdanie wpisu wg `rules/schemat-mapy.md` i przenieś go do właściwej sekcji (`Priorytet` / `Aktywne` / `Czeka` / `Zamknięte`).
- Jeśli status bez zmian — mapy nie ruszaj.

## Krok 5 — Powiedz krótko
Napisz prosto: co zapisałeś i w którym pliku. Bez streszczania całej rozmowy.

Nie kasuj żadnych plików. Nie publikuj niczego. Zwykły zapis w `~/.claude/pamiec/`.
