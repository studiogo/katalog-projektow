#!/usr/bin/env sh
# Odpala podany skrypt Pythona — python3 (Mac/Linux) lub python/py (Windows).
# Przekazuje stdin (hook dostaje JSON na stdin) i argumenty dalej.
# Wybór testem funkcjonalnym: na Windowsie `python3` bywa zaślepką Microsoft
# Store (alias wykonania), która przechodzi `command -v`, ale nie uruchamia
# Pythona. Dlatego sprawdzamy, który interpreter realnie działa.
for c in python3 python py; do
  if "$c" -c "import sys" >/dev/null 2>&1; then
    exec "$c" "$@"
  fi
done
# brak działającego Pythona — nic nie rób (reszta pluginu działa bez niego)
exit 0
