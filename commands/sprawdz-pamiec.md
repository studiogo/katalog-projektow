---
description: Sprawdza porządek w pamięci — format mapy, martwe linki, rozmiar, ewentualne hasła w plikach.
---

Sprawdź kondycję pamięci projektów i wytłumacz wynik prosto.

Wykonaj:
1. Uruchom w terminalu: `bash "${CLAUDE_PLUGIN_ROOT}/bin/memory-lint.sh"`
   (jeśli bash niedostępny: `python3 "${CLAUDE_PLUGIN_ROOT}/bin/memory-lint.py"`).
2. Przełóż wynik na prosty język:
   - **BŁĘDY (czerwone)** = napraw od razu: możliwe hasło w pliku, MEMORY.md za duży, martwy link.
   - **OSTRZEŻENIA (żółte)** = drobiazgi: wpis w mapie za długi / z datą / bez `[[link]]`.
   - **„Pamięć w porządku"** = wszystko gra.
3. Dla każdego problemu zaproponuj konkretną naprawę — ale nie wykonuj jej bez zgody.
