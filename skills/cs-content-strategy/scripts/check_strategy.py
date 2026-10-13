#!/usr/bin/env python3
"""QA gate for strategy_content.json before anything is written to Canva.

Usage:
  python check_strategy.py <strategy_content.json> [--capacity master_capacity.json] [--clients-dir clients]

strategy_content.json:
{
  "client": "Example Brand",
  "cadence": {"tiktok": "10 per day", "instagram": "5 per week"},     # required, from C or CM
  "format_categories": ["Proof", "Objection handling", "Connection", "Education"],
  "pages": [
    {"section": "COMM_GOALS", "module": "core|optional", "include": true,
     "fields": {"COMM_GOAL_1_TITLE": {"text": "...", "sources": ["C:evidence_map[12]"]}, ...}}
  ],
  "open_questions": ["..."]
}

Fails (exit 1) on:
- empty field in an included page (use include:false to drop a page, never leave a placeholder)
- a number in the text with no source
- words from another client's strategy (reference template terms, other client names in clients/)
- leftover {{PLACEHOLDER}} or UNKNOWN/TBD in client-facing text
- more than 4 Format categories, or missing cadence
- text longer than the box capacity (when --capacity is given)
Warns on AI-slop patterns (run sharrans-ai-slop to fix them).
"""
import json, os, re, sys

# Words from other clients' strategies that must never appear: client names found in clients/*/context
# plus an optional private list (one term per line) in <clients-dir>/../contentscale_leak_terms.txt
EXTRA_LEAK_FILE = 'contentscale_leak_terms.txt'
SLOP = [(r'—', 'em dash'), (r'\bnot (just )?\w+[^.]{0,40}, but\b', '"not X, but Y" flip'),
        (r"\b(game[- ]changer|unlock|elevate|delve|leverage|seamless|robust|in today's)\b", 'AI buzzword'),
        (r'\b[\w-]+(?: [\w-]+)?, [\w-]+(?: [\w-]+)?,? and [\w-]+(?: [\w-]+)?[.!]', 'triple list (check rhythm)')]


def family(key):
    """COMM_GOAL_3_TEXT -> COMM_GOAL_TEXT ; SWOT_STRENGTH_6 -> SWOT_STRENGTH"""
    return re.sub(r'_\d+(?=_|$)', '', key)


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    data = json.load(open(argv[1], encoding='utf8'))
    cap = json.load(open(argv[argv.index('--capacity') + 1])) if '--capacity' in argv else {}
    cdir = argv[argv.index('--clients-dir') + 1] if '--clients-dir' in argv else None
    client = data.get('client', '')
    leak = []
    if cdir:
        lf = os.path.join(os.path.dirname(os.path.abspath(cdir)), EXTRA_LEAK_FILE)
        if os.path.exists(lf):
            leak += [l.strip() for l in open(lf, encoding='utf8') if l.strip() and not l.startswith('#')]
    if cdir and os.path.isdir(cdir):
        for d in os.listdir(cdir):
            p = os.path.join(cdir, d, 'context', 'client_context.json')
            if os.path.exists(p):
                name = json.load(open(p, encoding='utf8')).get('client_name') or ''
                if name and name.lower() != client.lower():
                    leak.append(name)
    errors, warns = [], []
    if not data.get('cadence') or any(str(v).strip().upper() in ('', 'UNKNOWN', 'TBD', 'NONE') for v in data['cadence'].values()):
        errors.append('cadence missing: strategy cannot be finalised without posts per day/week (ask CM)')
    if len(data.get('format_categories', [])) > 4:
        errors.append(f"{len(data['format_categories'])} Format categories (max 4)")
    for pg in data.get('pages', []):
        if not pg.get('include', True):
            continue
        for key, f in pg.get('fields', {}).items():
            t = (f.get('text') or '').strip()
            where = f"{pg.get('section')}.{key}"
            if not t:
                errors.append(f'{where}: empty'); continue
            if re.search(r'\{\{|\bUNKNOWN\b|\bTBD\b', t):
                errors.append(f'{where}: placeholder/UNKNOWN left in client text')
            if re.search(r'\d', t) and not f.get('sources'):
                errors.append(f'{where}: has numbers but no sources')
            elif len(t) > 80 and not f.get('sources'):
                warns.append(f'{where}: long statement without sources')
            for term in leak:
                if term.lower() in t.lower():
                    errors.append(f'{where}: contains "{term}" (from another client or the template)')
            if key in cap and len(t) > cap[key] * 1.1:
                errors.append(f'{where}: {len(t)} chars > capacity {cap[key]}')
            for pat, name in SLOP:
                if re.search(pat, t, flags=re.I):
                    warns.append(f'{where}: {name}')
    # master keys left unfilled: if a page uses any key of a family (e.g. SWOT_STRENGTH_1),
    # every master key of that family must be filled or the slot removed (listed in "removed_keys")
    if cap:
        used = {k for pg in data.get('pages', []) if pg.get('include', True) for k in pg.get('fields', {})}
        removed = {k for pg in data.get('pages', []) for k in pg.get('removed_keys', [])}
        fams = {family(k) for k in used}
        for k in cap:
            if family(k) in fams and k not in used and k not in removed:
                errors.append(f'{k}: master placeholder in a used block is not filled (fill it or list it in the page "removed_keys")')
    for e in errors:
        print('ERROR', e)
    for w in warns:
        print('SLOP ', w)
    n = sum(len(p.get('fields', {})) for p in data.get('pages', []) if p.get('include', True))
    print(f'{n} fields checked, {len(errors)} errors, {len(warns)} slop warnings, {len(data.get("open_questions", []))} open questions')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
