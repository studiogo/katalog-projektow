#!/usr/bin/env sh
# Odpala podany skrypt Pythona — python3 (Mac/Linux) lub python (Windows/Git Bash).
# Przekazuje stdin (hook dostaje JSON na stdin) i argumenty dalej.
if command -v python3 >/dev/null 2>&1; then
  exec python3 "$@"
fi
exec python "$@"
