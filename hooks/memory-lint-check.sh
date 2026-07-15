#!/bin/bash
# memory-lint-check.sh — hook Stop. Uruchamia memory-lint.sh po turze.
# Przy błędach (exit 2) pokazuje alarm WPROST W TERMINALU przez systemMessage,
#   żeby użytkownik nie musiał zaglądać do żadnego logu.
# Pole systemMessage: https://code.claude.com/docs/en/hooks („Warning message shown to the user").

# Wykryj własny katalog (działa niezależnie od miejsca instalacji pluginu)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINT="$SCRIPT_DIR/../bin/memory-lint.sh"

[[ -f "$LINT" ]] || exit 0
bash "$LINT" --hook > /dev/null 2>&1
CODE=$?

# exit 2 = realne błędy (rozmiar MEMORY.md nad limitem / możliwy wyciek hasła / zepsute odnośniki).
if [[ $CODE -eq 2 ]]; then
  MSG="🔴 Porządek pamięci: wykryto problem (rozmiar MEMORY.md, możliwe hasło w pliku lub zepsuty link). Wpisz /sprawdz-pamiec po szczegóły."
  if command -v jq >/dev/null 2>&1; then
    jq -n --arg m "$MSG" '{systemMessage:$m}'
  else
    printf '{"systemMessage":"%s"}\n' "$MSG"
  fi
fi

exit 0  # nigdy nie blokuj zakończenia sesji
