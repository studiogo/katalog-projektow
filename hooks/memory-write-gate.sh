#!/bin/bash
# memory-write-gate.sh — hook PreToolUse na Write/Edit/MultiEdit.
#
# Cel: zatrzymać zapis do MEMORY.md i ZAPYTAĆ, gdy treść wygląda na STATUS/DANE projektu
# — bo to powinno trafić do pliku projektu (projects/<nazwa>/HANDOFF.md), nie do mapy.
# Czyste wskaźniki (krótkie, bez ID/dat/statusu) przechodzą bez pytania.
#
# ⚠ Łapie tylko Write/Edit/MultiEdit. Zapis przez terminal omija hook —
#    backstop rozmiaru jest w memory-lint.py (hook Stop).
set -uo pipefail

# Stała ścieżka pamięci (działa u każdego użytkownika, niezależnie od nazwy konta)
MEMORY="$HOME/.claude/pamiec/MEMORY.md"
SIZE_WARN=24000   # B — twardy limit ~24400; ostrzegaj wcześniej

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""')
case "$TOOL" in Edit|Write|MultiEdit) ;; *) exit 0 ;; esac

FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')
# Gate dotyczy WYŁĄCZNIE mapy MEMORY.md (nie plików projektu — tam status MA być)
[[ "$FILE" != "$MEMORY" ]] && exit 0

# Treść wchodząca: Write=.content, Edit=.new_string, MultiEdit=.edits[].new_string
CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string // ([.tool_input.edits[]?.new_string] | join("\n")) // ""')
LEN=${#CONTENT}

# Sygnały, że to status/dane projektu (a nie wskaźnik)
TRIGGERS=""
echo "$CONTENT" | grep -qE '[0-9]{15,}'                              && TRIGGERS="${TRIGGERS}długie ID (≥15 cyfr); "
echo "$CONTENT" | grep -qE '[0-3][0-9]\.[01][0-9](\.20[0-9]{2})?'    && HAS_DATE=1 || HAS_DATE=0
echo "$CONTENT" | grep -qE '✅|⏳|🚨|🟢|🔴|❌|🥇|🥈|🥉'              && HAS_STATUS=1 || HAS_STATUS=0
if (( LEN > 400 )) && { [[ "$HAS_DATE" == 1 ]] || [[ "$HAS_STATUS" == 1 ]]; }; then
  TRIGGERS="${TRIGGERS}duży wpis (${LEN} zn.) ze statusem/datą; "
fi

# Rozmiar pliku po stronie progu
BYTES=$(wc -c < "$MEMORY" 2>/dev/null | tr -d ' ')
[[ -n "$BYTES" ]] && (( BYTES > SIZE_WARN )) && TRIGGERS="${TRIGGERS}MEMORY.md już ${BYTES} B (>${SIZE_WARN}); "

# --- Format wpisu mapy (rules/schemat-mapy.md): ≤140 znaków + [[link]] + bez emoji ---
HAS_EMOJI=$(printf '%s' "$CONTENT" | python3 -c "import sys,re; print(1 if re.search('[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002300-\U000023FF\U0001F1E6-\U0001F1FF]', sys.stdin.read()) else 0)" 2>/dev/null || echo 0)
[[ "$HAS_EMOJI" == 1 ]] && TRIGGERS="${TRIGGERS}emoji w treści (schemat: bez emoji, status→sekcja); "
LONG=$(printf '%s' "$CONTENT" | awk '/^[[:space:]]*-[[:space:]]/ { if (length($0) > 140) { print length($0); exit } }')
[[ -n "$LONG" ]] && TRIGGERS="${TRIGGERS}wpis listy ${LONG} zn. > 140 (zwiń; detale → HANDOFF); "
if printf '%s' "$CONTENT" | grep -qE '→[[:space:]]*`?projects/' && ! printf '%s' "$CONTENT" | grep -q '\[\['; then
  TRIGGERS="${TRIGGERS}wpis-pointer bez [[link]] (schemat wymaga [[nazwa]]); "
fi

# Brak sygnałów → przepuść (czysty wskaźnik)
[[ -z "$TRIGGERS" ]] && exit 0

REASON="STOP — zapis do MEMORY.md wygląda na STATUS/DANE projektu (wykryto: ${TRIGGERS%; }).

MEMORY.md = mapa wskaźników, NIE magazyn statusu. To prawie zawsze powinno trafić do pliku projektu:
  • status dnia, daty, liczniki, cytaty → projects/<nazwa>/HANDOFF.md
  • numery/identyfikatory → projects/<nazwa>/config.json
  • decyzje → projects/<nazwa>/decyzje.md

Format wpisu mapy: rules/schemat-mapy.md (jedno zdanie, [[link]], ≤140 znaków, bez emoji).

Jeśli to NAPRAWDĘ wskaźnik/mapa (krótki, bez surowych ID) — zatwierdź. W innym wypadku: odrzuć i zapisz do pliku projektu."

jq -n --arg reason "$REASON" '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "ask",
    permissionDecisionReason: $reason
  }
}'
mkdir -p "$HOME/.claude/pamiec/.logs"
echo "[$(date +"%Y-%m-%d %H:%M:%S")] ASK MEMORY write (tool=$TOOL len=$LEN bytes=${BYTES:-?}): ${TRIGGERS%; }" >> "$HOME/.claude/pamiec/.logs/write-gate.log"
exit 0
