#!/usr/bin/env python3
"""Łącznik projektów — buduje [[Powiązane]] na podstawie DOWODÓW w Twoich notatkach.

Nie musisz nic wpisywać ręcznie. Skrypt czyta treść wszystkich projektów i szuka
miejsc, gdzie jeden projekt naprawdę odwołuje się do drugiego (ścieżka, wikilink,
nazwa). Powiązanie powstaje tylko wtedy, gdy jest na nie dowód — plik i linia.

  przelot-linkera.py --dry-run   — pokaż, co znalazł i z jakiego dowodu (nic nie zapisuje)
  przelot-linkera.py             — zapisz sekcje ## Powiązane w hubach + dziennik
  przelot-linkera.py --pokaz-dowody nazwa-projektu   — skąd wzięło się każde powiązanie

Pojedyncze pary możesz nadal połączyć komendą /polacz-projekty.
"""
import re, pathlib, sys, argparse, datetime
from collections import defaultdict

BASE = pathlib.Path.home() / ".claude" / "pamiec" / "projects"
POMIN = {"_TEMPLATE", "archiwum", "dane", "archive"}


def projekty(base):
    return sorted(p.name for p in base.iterdir()
                  if p.is_dir() and p.name not in POMIN and not p.name.startswith("."))


def tytul_huba(base, nazwa):
    """Nagłówek H1 z huba — bywa czytelną nazwą ('Sklep Ani')."""
    for kand in (f"{nazwa}.md", "HUB.md", "README.md", "INDEX.md"):
        f = base / nazwa / kand
        if f.exists():
            for lin in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                if lin.startswith("# "):
                    t = re.sub(r'^(Projekt|Klient|Kurs)\s*[:—-]\s*', '', lin[2:].strip(), flags=re.I)
                    if len(t) > 4 and t.upper() != "TYTUL_PROJEKTU":
                        return t
    return None


def wzorce(nazwa, tytul):
    """Czego szukamy. Ścieżka i wikilink to mocny dowód, sama nazwa — słaby."""
    w = [(re.compile(rf'(?<![\w-]){re.escape(nazwa)}/'), 3),
         (re.compile(rf'\[\[{re.escape(nazwa)}\]\]'), 3),
         (re.compile(rf'(?<![\w-]){re.escape(nazwa)}(?![\w/-])'), 1)]
    if tytul:
        w.append((re.compile(re.escape(tytul), re.I), 2))
    return w


def bez_sekcji_powiazane(tekst):
    """Wycina sekcję ## Powiązane. Stare linki NIE są dowodem — inaczej skrypt
    powielałby własny poprzedni wynik zamiast czytać treść."""
    return re.sub(r'^##+ *[^\n]*Powiązane[^\n]*\n.*?(?=^##+ |\Z)', '\n', tekst, flags=re.S | re.M)


def skanuj(base, nazwy):
    tytuly = {n: tytul_huba(base, n) for n in nazwy}
    wz = {n: wzorce(n, tytuly[n]) for n in nazwy}
    dowody = defaultdict(list)
    for zrodlo in nazwy:
        for f in (base / zrodlo).rglob("*.md"):
            try:
                tekst = bez_sekcji_powiazane(f.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue
            for i, lin in enumerate(tekst.splitlines(), 1):
                if len(lin) > 2000:
                    continue
                for cel in nazwy:
                    if cel == zrodlo:
                        continue
                    for rx, waga in wz[cel]:
                        if rx.search(lin):
                            dowody[tuple(sorted((zrodlo, cel)))].append(
                                (waga, f"{zrodlo}/{f.name}", i, lin.strip()[:110]))
                            break
    return dowody


def sila(lista):
    najlepsze = {}
    for waga, plik, _, _ in lista:
        najlepsze[plik] = max(najlepsze.get(plik, 0), waga)
    return sum(najlepsze.values())


def zbuduj(base, prog, maks):
    nazwy = projekty(base)
    dowody = skanuj(base, nazwy)
    kand = defaultdict(list)
    for (a, b), lista in dowody.items():
        s = sila(lista)
        if s >= prog:
            kand[a].append((s, b, lista))
            kand[b].append((s, a, lista))
    adj = defaultdict(set)
    for n in nazwy:
        for s, inny, _ in sorted(kand.get(n, []), key=lambda x: -x[0])[:maks]:
            adj[n].add(inny)
            adj[inny].add(n)
    return nazwy, kand, adj


def zapisz_sekcje(hub, links):
    """Podmienia TYLKO sekcję ## Powiązane. Treść pod nią zostaje nietknięta."""
    tekst = hub.read_text(encoding="utf-8", errors="ignore")
    blok = f"## Powiązane\n{links}\n"
    if re.search(r'^## Powiązane', tekst, flags=re.M):
        # zatrzymaj się na następnym nagłówku — NIE kasuj reszty pliku
        tekst = re.sub(r'^## Powiązane.*?(?=^## |\Z)', blok + "\n", tekst, flags=re.S | re.M)
    else:
        tekst = tekst.rstrip() + "\n\n" + blok
    hub.write_text(tekst, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="pokaż, nic nie zapisuj")
    ap.add_argument("--base", default=str(BASE), help="katalog projektów")
    ap.add_argument("--pokaz-dowody", metavar="PROJEKT", help="skąd wzięło się każde powiązanie")
    ap.add_argument("--min", type=int, default=3, help="ostrzegaj poniżej tylu powiązań")
    ap.add_argument("--max", type=int, default=8, help="najwyżej tyle powiązań na projekt")
    args = ap.parse_args()

    base = pathlib.Path(args.base)
    if not base.is_dir():
        print(f"Nie znalazłem katalogu projektów: {base}")
        print("Uruchom najpierw /nowy-projekt albo wskaż katalog przez --base.")
        sys.exit(1)

    nazwy, kand, adj = zbuduj(base, 3, args.max)
    if not nazwy:
        print("Brak projektów — nie ma czego łączyć."); return

    if args.pokaz_dowody:
        cel = args.pokaz_dowody
        if cel not in nazwy:
            print(f"Nie ma projektu „{cel}”. Są: {', '.join(nazwy)}"); sys.exit(1)
        print(f"Dowody powiązań dla „{cel}”:\n")
        for s, inny, lista in sorted(kand.get(cel, []), key=lambda x: -x[0]):
            waga, plik, lin, frag = max(lista, key=lambda x: x[0])
            print(f"  [siła {s:3}] {inny}\n      dowód: {plik}, linia {lin}\n      „{frag}”\n")
        if not kand.get(cel):
            print("  Brak dowodów w treści. Jeśli powiązanie istnieje, dopisz je\n"
                  "  komendą /polacz-projekty — skrypt nie zgaduje.")
        return

    sieroty = [n for n in nazwy if not adj.get(n)]
    ponizej = [n for n in nazwy if 0 < len(adj.get(n, ())) < args.min]

    print(f"Projekty: {len(nazwy)} | z powiązaniami: {len([n for n in nazwy if adj.get(n)])}")
    print(f"Powiązań (par): {sum(len(v) for v in adj.values()) // 2}")
    if sieroty:
        print(f"\nBez powiązań: {', '.join(sieroty)}")
        print("  → To nie znaczy, że są niepowiązane — znaczy, że w notatkach nie ma na to")
        print("    dowodu. Oceń sam i połącz komendą /polacz-projekty.")
    if ponizej:
        print(f"\nMało powiązań (mniej niż {args.min}): {', '.join(ponizej)}")

    if args.dry_run:
        print("\n[podgląd — nic nie zapisano]")
        print("Sprawdź konkretny projekt:  przelot-linkera.py --pokaz-dowody NAZWA")
        return

    dziennik = [f"## [{datetime.date.today()}] przelot łącznika"]
    for n in nazwy:
        hub = base / n / f"{n}.md"
        if not hub.exists():
            hub = base / n / "HUB.md"
        if not hub.exists() or not adj.get(n):
            continue
        links = " · ".join(f"[[{x}]]" for x in sorted(adj[n]))
        zapisz_sekcje(hub, links)
        dziennik.append(f"- {n}: {links}")

    logf = base / "linker-log.md"
    stare = logf.read_text(encoding="utf-8") if logf.exists() else ""
    logf.write_text("\n".join(dziennik) + "\n\n" + stare, encoding="utf-8")
    print(f"\nZapisano. Dziennik: {logf}")
    print("Graf zobaczysz, otwierając ~/.claude/pamiec/ w Obsidianie (Graph View).")


if __name__ == "__main__":
    main()
