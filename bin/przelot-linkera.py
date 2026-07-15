#!/usr/bin/env python3
"""Łącznik projektów — wstawia dwukierunkowe [[Powiązane]] do plików-hubów projektów.

Jak używać: wpisz własne pary do EDGES (po sensie — wspólny temat, klient, obszar),
uruchom skrypt. Symetria domknie się sama (jeśli A-B, to i B-A).

  przelot-linkera.py            — wykonaj (zapisuje huby)
  przelot-linkera.py --dry-run  — pokaż, nic nie zapisuj
"""
import re, pathlib, sys, argparse

BASE = pathlib.Path.home() / ".claude" / "pamiec" / "projects"

# Pary projektów do połączenia. Wpisz WŁASNE po sensie, np. ("sklep-ania", "kampania-wiosna").
# Zostaw pustą listę, jeśli wolisz łączyć projekty pojedynczo komendą /polacz-projekty.
EDGES = [
    # ("nazwa-projektu-1", "nazwa-projektu-2"),
]


def build_adjacency():
    adj = {}
    for a, b in EDGES:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    return adj


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="pokaż, nic nie zapisuj")
    args = ap.parse_args()

    adj = build_adjacency()
    if not adj:
        print("Lista par (EDGES) jest pusta — nic do połączenia.")
        print("Wpisz własne pary w tym pliku albo użyj komendy /polacz-projekty.")
        return

    missing = [n for n in adj if not (BASE / n / f"{n}.md").exists()]
    if missing:
        print("BŁĄD — brak projektów (hubów) dla:", ", ".join(missing)); sys.exit(1)

    if not args.dry_run:
        for name, neighbors in adj.items():
            hub = BASE / name / f"{name}.md"
            text = hub.read_text()
            links = " · ".join(f"[[{n}]]" for n in sorted(neighbors))
            text = re.sub(r'## Powiązane.*$', f"## Powiązane\n{links}\n", text, flags=re.DOTALL)
            hub.write_text(text)

    degs = {n: len(v) for n, v in adj.items()}
    print(f"{'[podgląd] ' if args.dry_run else ''}Połączono projektów: {len(adj)}")
    print(f"Powiązań (par): {sum(len(v) for v in adj.values()) // 2}")


if __name__ == "__main__":
    main()
