#!/usr/bin/env python3
"""
memory-lint.py — strażnik porządku pamięci projektów (~/.claude/pamiec/).

Reguły (uniwersalne, bez zależności od konkretnego użytkownika):
  R1. Wyciek hasła/klucza — hardkodowane hasła/tokeny/klucze w plikach (ERROR).
  R7. Rozmiar MEMORY.md — mapa nie może rosnąć bez końca (ERROR nad limitem).
  R8. Format wpisu mapy — [[link]] + ≤140 znaków + bez emoji/ID/dat (WARN).
  R9. Martwe [[wikilinki]] — link do nieistniejącego projektu/pliku (WARN).
  R10. Huby-sieroty — projekt bez żadnego [[Powiązane]] (INFO).

Ścieżka pamięci: $HOME/.claude/pamiec/ — stała, działa u każdego użytkownika.
Exit: 0 = OK, 1 = ostrzeżenia, 2 = błędy (wyciek hasła lub MEMORY.md nad limitem).
"""

import re, sys, base64
from pathlib import Path
from datetime import datetime

HOME = Path.home()
MEMORY_DIR = HOME / ".claude" / "pamiec"
PROJECTS_DIR = MEMORY_DIR / "projects"
MEMORY_FILE = MEMORY_DIR / "MEMORY.md"
INDEX_FILE = PROJECTS_DIR / "index.md"
SCHEMA_FILE = MEMORY_DIR / "rules" / "schemat-mapy.md"

EXCLUDE_PATHS = ("/archiwum/", "/.logs/", "/materialy/")

COLOR = sys.stdout.isatty()
def c(txt, code): return f"\033[{code}m{txt}\033[0m" if COLOR else txt
RED = lambda s: c(s, 31); YEL = lambda s: c(s, 33); GRN = lambda s: c(s, 32); BLU = lambda s: c(s, 34); BOLD = lambda s: c(s, 1)

errors, warnings, infos = [], [], []
def report(kind, rule, detail):
    (errors if kind == "ERR" else warnings if kind == "WARN" else infos).append((rule, detail))

# ============================================================
# R1: Wyciek hasła / klucza
# ============================================================
SECRET_PATTERNS = [
    (r'sk-proj-[A-Za-z0-9_\-]{20,}', "klucz OpenAI (projekt)"),
    (r'sk-ant-api\d+-[A-Za-z0-9_\-]{30,}', "klucz Anthropic"),
    (r'AIza[0-9A-Za-z_\-]{30,}', "klucz Google"),
    (r'ghp_[A-Za-z0-9]{30,}', "token GitHub"),
    (r'xoxb-[A-Za-z0-9_\-]{20,}', "token Slack"),
    (r'Bearer\s+[A-Za-z0-9_\-\.]{30,}', "token Bearer"),
    (r'eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+', "token JWT"),
]
PLAIN_USER_PASS = re.compile(r'(?:admin|root|user):(?!\*|\{|<)[A-Za-z0-9_\-!@#$%^&*]{6,}')
BASE64_CANDIDATE = re.compile(r'[A-Za-z0-9+/]{16,200}={0,2}')

def is_basic_auth_base64(s):
    try:
        if len(s) < 16 or len(s) > 256: return False
        decoded = base64.b64decode(s + "=" * (-len(s) % 4), validate=False)
        if not all(32 <= b < 127 for b in decoded): return False
        if b":" not in decoded: return False
        parts = decoded.split(b":", 1)
        return len(parts) == 2 and len(parts[0]) >= 2 and len(parts[1]) >= 4
    except Exception:
        return False

def scan_file_for_secrets(path, rel):
    try:
        content = path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return
    for pat, kind in SECRET_PATTERNS:
        for m in re.finditer(pat, content):
            line = content[:m.start()].count('\n') + 1
            report("ERR", "WYCIEK_HASLA", f"{rel}:{line} — {kind}: {m.group(0)[:30]}...")
    for m in PLAIN_USER_PASS.finditer(content):
        line = content[:m.start()].count('\n') + 1
        report("ERR", "WYCIEK_HASLA", f"{rel}:{line} — login:hasło jawnie: {m.group(0)[:40]}")
    for m in BASE64_CANDIDATE.finditer(content):
        if is_basic_auth_base64(m.group(0)):
            line = content[:m.start()].count('\n') + 1
            report("ERR", "WYCIEK_HASLA", f"{rel}:{line} — zakodowane login:hasło (base64)")

def rule1_secrets():
    if not MEMORY_DIR.exists(): return
    for p in MEMORY_DIR.rglob("*.md"):
        rel = str(p.relative_to(MEMORY_DIR))
        if any(x in str(p) for x in EXCLUDE_PATHS): continue
        scan_file_for_secrets(p, rel)

# ============================================================
# R7: Rozmiar MEMORY.md
# ============================================================
def rule7_size():
    if not MEMORY_FILE.exists(): return
    size = MEMORY_FILE.stat().st_size
    HARD, WARN = 24400, 18000
    if size > HARD:
        report("ERR", "MAPA_ZA_DUZA", f"MEMORY.md = {size} B > {HARD} (ryzyko ucięcia). Zwiń najgrubszy wpis; szczegóły → HANDOFF projektu.")
    elif size > WARN:
        report("WARN", "MAPA_ROSNIE", f"MEMORY.md = {size} B > {WARN} (cel roboczy). Nie dopisuj statusu/ID do mapy.")

# ============================================================
# R8/R9/R10: format wpisu, martwe linki, sieroty
# ============================================================
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002300-\U000023FF\U0001F1E6-\U0001F1FF️]")
WIKILINK_RE = re.compile(r'\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]')
PROJECT_SECTION_RE = re.compile(r'(priorytet|aktywne|czeka|zamkni|active|pending|prio)', re.IGNORECASE)

def _strip_code(text):
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    return re.sub(r'`[^`]*`', '', text)

def rule8_map_format():
    if not MEMORY_FILE.exists(): return
    lines = MEMORY_FILE.read_text().split('\n')
    in_code = in_proj = False
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith('```'): in_code = not in_code; continue
        if in_code: continue
        if s.startswith('#'): in_proj = bool(PROJECT_SECTION_RE.search(s)); continue
        if re.match(r'^\s*-\s+\[\[', line):
            if len(s) > 140:
                report("WARN", "WPIS_ZA_DLUGI", f"MEMORY.md:{i} — {len(s)} zn. > 140 (zwiń; detale → HANDOFF)")
            if EMOJI_RE.search(s):
                report("WARN", "WPIS_EMOJI", f"MEMORY.md:{i} — emoji we wpisie (status → sekcja): {s[:44]}")
            stripped = _strip_code(s)
            if re.search(r'\d{8,}', stripped):
                report("WARN", "WPIS_ID", f"MEMORY.md:{i} — surowe ID we wpisie (→ config.json): {s[:44]}")
            if re.search(r'\b[0-3]\d\.[01]\d(?:\.20\d{2})?\b|\b20\d{2}-\d{2}-\d{2}\b', stripped):
                report("WARN", "WPIS_DATA", f"MEMORY.md:{i} — data we wpisie (→ HANDOFF): {s[:44]}")
        elif in_proj and re.match(r'^\s*-\s+\S', line) and '[[' not in line:
            report("WARN", "WPIS_BEZ_LINKU", f"MEMORY.md:{i} — wpis w sekcji projektów bez [[link]]: {s[:44]}")

def _valid_targets():
    targets = set()
    if PROJECTS_DIR.exists():
        for proj in PROJECTS_DIR.iterdir():
            if proj.is_dir() and (proj / f"{proj.name}.md").exists():
                targets.add(proj.name)
    for p in MEMORY_DIR.rglob("*.md"):
        targets.add(p.stem)
    return targets

def rule9_dead_links():
    valid = _valid_targets()
    scan = [MEMORY_FILE, INDEX_FILE]
    if PROJECTS_DIR.exists():
        for proj in PROJECTS_DIR.iterdir():
            hub = proj / f"{proj.name}.md" if proj.is_dir() else None
            if hub and hub.exists(): scan.append(hub)
    for f in scan:
        if not f or not f.exists(): continue
        text = _strip_code(f.read_text())
        rel = str(f.relative_to(MEMORY_DIR))
        for m in WIKILINK_RE.finditer(text):
            base = m.group(1).strip().split('/')[-1].split('#')[0].strip()
            if base and base not in valid:
                report("WARN", "MARTWY_LINK", f"{rel} — [[{m.group(1)}]] wskazuje na nieistniejący projekt/plik")

def rule10_orphan_hubs():
    if not PROJECTS_DIR.exists(): return
    orphans = []
    for proj in PROJECTS_DIR.iterdir():
        if not proj.is_dir(): continue
        hub = proj / f"{proj.name}.md"
        if not hub.exists(): continue
        m = re.search(r'##\s+Powiązane(.*)$', hub.read_text(), re.DOTALL)
        if not WIKILINK_RE.search(m.group(1) if m else ""):
            orphans.append(proj.name)
    if orphans:
        report("INFO", "HUB_SIEROTA", f"{len(orphans)} projekt(ów) bez powiązań — użyj /polacz-projekty")

# ============================================================
def main():
    print(BOLD("=== Porządek pamięci projektów ==="))
    print(f"Pamięć: {MEMORY_DIR}")
    print(f"Czas:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    if not MEMORY_DIR.exists():
        print(YEL("Brak katalogu pamięci — uruchom /zainstaluj-katalog."))
        sys.exit(0)
    print(BLU("→ R1: wyciek hasła/klucza...")); rule1_secrets()
    print(BLU("→ R7: rozmiar MEMORY.md...")); rule7_size()
    print(BLU("→ R8: format wpisu mapy...")); rule8_map_format()
    print(BLU("→ R9: martwe [[linki]]...")); rule9_dead_links()
    print(BLU("→ R10: huby-sieroty...")); rule10_orphan_hubs()
    print()
    if errors:
        print(RED(BOLD(f"❌ BŁĘDY: {len(errors)}")))
        for r, d in errors: print(RED(f"  [{r}] {d}"))
        print()
    if warnings:
        print(YEL(BOLD(f"⚠️  OSTRZEŻENIA: {len(warnings)}")))
        for r, d in warnings: print(YEL(f"  [{r}] {d}"))
        print()
    if infos:
        for r, d in infos: print(GRN(f"ℹ️  [{r}] {d}"))
    if not errors and not warnings:
        print(GRN(BOLD("✅ Pamięć w porządku.")))
    sys.exit(2 if errors else 1 if warnings else 0)

if __name__ == "__main__":
    main()
