#!/bin/bash
# memory-lint.sh — wrapper wokół memory-lint.py.
#   memory-lint.sh            — raport w konsoli
#   memory-lint.sh --report <plik>  — raport do pliku
#   memory-lint.sh --hook     — tryb hook (cicho; cooldown 30 min; zwraca kod wyjścia)
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINT_PY="$SCRIPT_DIR/memory-lint.py"
LOG_DIR="$HOME/.claude/pamiec/.logs"
mkdir -p "$LOG_DIR"
find "$LOG_DIR" -name "raport-*.txt" -mtime +14 -delete 2>/dev/null

MODE="${1:-console}"
TS=$(date +%Y-%m-%d_%H-%M-%S)
REPORT="$LOG_DIR/raport-$TS.txt"
# Wybór interpretera testem funkcjonalnym, nie samym `command -v`:
# na Windowsie `python3` bywa zaślepką Microsoft Store (alias wykonania),
# która przechodzi `command -v`, ale nie uruchamia Pythona. Sprawdzamy realnie.
PY=""
for c in python3 python py; do
  if "$c" -c "import sys" >/dev/null 2>&1; then PY="$c"; break; fi
done
[[ -z "$PY" ]] && exit 0   # brak Pythona → strażnik cichy (reszta pluginu działa)

if [[ "$MODE" == "--hook" ]]; then
  COOLDOWN="$LOG_DIR/.last-hook-run"
  if [[ -f "$COOLDOWN" ]]; then
    LAST=$(cat "$COOLDOWN" 2>/dev/null || echo 0); NOW=$(date +%s)
    (( NOW - LAST < 1800 )) && exit 0
  fi
  date +%s > "$COOLDOWN"
  "$PY" "$LINT_PY" > "$REPORT" 2>&1
  exit $?
elif [[ "$MODE" == "--report" ]]; then
  TARGET="${2:-$REPORT}"
  "$PY" "$LINT_PY" > "$TARGET" 2>&1
  echo "Raport: $TARGET"
  exit $?
else
  "$PY" "$LINT_PY"
  exit $?
fi
