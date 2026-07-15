---
description: Kreator — zakłada system pamięci projektów w ~/.claude/pamiec/ i przeprowadza przez pierwszy setup.
---

Jesteś kreatorem instalacji. Prowadź użytkownika prostym językiem, po polsku, krok po kroku. Nie zakładaj wiedzy technicznej. Nic nie nadpisuj bez zgody.

## Krok 1 — Powitanie
Powiedz krótko, co powstanie: „Założę Ci porządek na projekty — mapę wszystkiego, katalog projektów i graf, który zobaczysz w darmowym Obsidianie. Wszystko w plikach na Twoim dysku, bez kont i kluczy."

## Krok 2 — Utwórz strukturę
Ścieżka bazowa: `~/.claude/pamiec/` (na Windowsie: `%USERPROFILE%\.claude\pamiec`).
Utwórz katalogi, jeśli nie istnieją: `~/.claude/pamiec/`, `~/.claude/pamiec/projects/`, `~/.claude/pamiec/rules/`.
Skopiuj z `${CLAUDE_PLUGIN_ROOT}/templates/pamiec/` do `~/.claude/pamiec/`, zachowując strukturę, **tylko pliki, których jeszcze nie ma** (istniejące wypisz jako „pominięto, już jest"):
- `MEMORY.md`, `rules/schemat-mapy.md`, `projects/index.md`, cały `projects/_TEMPLATE/`.

## Krok 3 — Tożsamość agenta (CLAUDE.md)
Skopiuj `${CLAUDE_PLUGIN_ROOT}/templates/pamiec/CLAUDE.md` → `~/.claude/CLAUDE.md` **tylko jeśli plik nie istnieje**. Jeśli istnieje — NIE nadpisuj; pokaż sekcję „Gdzie co leży (mapa pamięci)" i zaproponuj doklejenie tych linii do jego pliku.

## Krok 4 — Projekty: od zera czy z istniejących plików
Zapytaj: **„Zaczynasz od czystej kartki czy masz już pliki na dysku, które mam ogarnąć?"**

- **A) MAM JUŻ PLIKI** — uruchom import: wykonaj to, co komenda `/importuj-projekty` (zeskanuj wskazany katalog, zaproponuj wykryte projekty do zatwierdzenia, zbuduj huby + mapę + linki, README/HANDOFF za zgodą, plików nie ruszaj). Po imporcie pomiń resztę tego kroku.
- **B) OD ZERA, mam projekty w głowie** — poproś o listę nazw. Dla KAŻDEJ nazwy wykonaj to, co robi komenda `/nowy-projekt` (katalog ze skeletonu + węzeł grafu `<nazwa>.md` + wpis w `index.md` i `MEMORY.md`). Poproś o jedno zdanie opisu na każdy.
- **C) OD ZERA, nic jeszcze** — zostaw w `MEMORY.md` jedną atrapę i powiedz, że projekt doda komendą `/nowy-projekt`, gdy będzie gotów.

## Krok 5 — Gdzie pliki (opcjonalnie)
Zapytaj: „Gdzie trzymasz pliki robocze (dokumenty, grafiki)?" Jeśli odpowie — zapisz krótko do `~/.claude/pamiec/rules/gdzie-pliki.md` (zwykły opis, po jego ścieżkach). Jeśli nie chce — pomiń.

## Krok 6 — Połącz projekty (jeśli ≥2)
Jeśli powstały co najmniej 2 projekty, zaproponuj komendę `/polacz-projekty`, żeby zbudować pierwsze powiązania w grafie.

## Krok 7 — Twarde zasady (opcjonalnie, osobny plugin)
Zapytaj: **„Chcesz dołożyć strażnika zasad pracy (plugin `kaganiec`)? Wstrzykuje Twoje reguły do każdej wiadomości — także subagentom. Uwaga: to nieco szybciej zużywa limity Claude (szczegóły w pliku KOSZT.md tamtego pluginu)."**
Jeśli TAK — poprowadź: `/plugin marketplace add studiogo/kaganiec`, potem `/plugin install`. To OSOBNY, publiczny plugin — nie część tej paczki, tylko rekomendacja.

## Krok 8 — Zakończenie
Utwórz pusty plik-znacznik `~/.claude/pamiec/.setup-done`. Podsumuj prosto:
- co powstało (lista),
- że mapa `MEMORY.md` ma tylko drogowskazy — jedno zdanie na projekt,
- że nowy projekt dodajesz komendą `/nowy-projekt`, a porządek sprawdzasz `/sprawdz-pamiec`,
- że **graf zobaczysz, otwierając folder `~/.claude/pamiec/` w Obsidianie** (Open folder as vault → Graph View); w ustawieniach grafu warto wyłączyć „Show orphans", żeby widzieć tylko połączone projekty,
- że jeśli strażnik porządku nie reaguje (np. przy zapisie do MEMORY.md), to znaczy, że plugin był świeżo zainstalowany — wystarczy raz zrestartować Claude Code albo wpisać `/reload-plugins`.

Nie instaluj żadnych zależności. Nie pisz skryptów. Zwykły odczyt i zapis plików.
