#!/usr/bin/env python3
"""Automatic regression checks (references/regression_tests.md) for calendar_items.json.

Usage:
  python qa_calendar.py <calendar_items.json> <reference_records.json> [--day Monday] [--week 1]

calendar_items.json:
{
  "client": "Example Brand",
  "allowed_formats": ["Proof", "Objection handling", "Connection", "Education"],
  "allowed_types": ["Talking head", "Expert video", "BTS"],
  "hashtags": ["#brand", "#brandname"],          # client's pattern (from their own captions)
  "core_objection_topic": "foam",                   # topic key that must appear at least once per week
  "items": [{
     "id": "w1-mon-01", "week": 1, "week_day": "Monday", "name": "...",
     "format": "Objection handling", "type": "Talking head", "platforms": ["TT", "IG"],
     "topic": "foam", "reference_url": "...", "reference_views": "696.9K",
     "reaction_target_url": null, "notes_for_client": "...", "script": "...",
     "onscreen_text": [], "carousel_slides": [], "caption": "...",
     "reskin_table": [["original line", "client line"], ...],    # TH only, internal
     "sources": ["C:evidence_map[60]", "R:<url>"]                  # internal provenance
  }]
}
Writes nothing; prints ERROR / WARN lines; exit 1 on any ERROR.
"""
import json, re, sys
from collections import Counter, defaultdict

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
BANNED_CLIENT_TEXT = [r'\bclaude\b', r'\bAI[- ]generated\b', r'\bwe (decided|chose|picked)\b', r'\bstrategy note\b',
                      r'\binternal\b', r'\{\{', r'\bTODO\b', r'\bUNKNOWN\b', r'\bQA\b']
SLOP = [(r'—', 'em dash'), (r'[«»]', 'guillemets'), (r"here'?s the thing", '"here\'s the thing"'),
        (r"here is what that actually means|here's exactly what", 'banned build-up phrase'),
        (r"\bit'?s not (an? )?[\w ]{1,30}(problem|thing)?, it'?s\b", '"it\'s not X, it\'s Y"'),
        (r'\b(game[- ]changer|unlock|elevate|delve|seamless)\b', 'AI buzzword')]
DATE_RE = r'\b(\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2}|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]* \d{1,2}(st|nd|rd|th)?)\b(?!\d)'


def norm(s):
    return re.sub(r'\W+', ' ', (s or '').lower()).strip()


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    cal = json.load(open(argv[1], encoding='utf8'))
    refs = {r['reference_url']: r for r in json.load(open(argv[2], encoding='utf8'))['records']}
    day = argv[argv.index('--day') + 1] if '--day' in argv else None
    week = int(argv[argv.index('--week') + 1]) if '--week' in argv else None
    items = [i for i in cal['items'] if (not day or i.get('week_day') == day) and (not week or i.get('week') == week)]
    E, W = [], []
    tags = [t.lower() for t in cal.get('hashtags', [])]

    for it in items:
        w = it.get('id', it.get('name'))
        t, body = it.get('type'), ' '.join(str(it.get(k) or '') for k in
                                           ('name', 'notes_for_client', 'script', 'caption')) + ' ' + \
            ' '.join(it.get('onscreen_text') or []) + ' ' + ' '.join(it.get('carousel_slides') or [])
        # R2 dates
        if it.get('publishing_date') or it.get('edited_video'):
            E.append(f'{w}: Publishing date / Edited video must be empty (R2)')
        if re.search(DATE_RE, body, re.I):
            W.append(f'{w}: looks like a date in client text (R2)')
        mode = it.get('mode')  # None (calendar post) | 'caption_only' | 'framework'
        if it.get('week_day') is not None and it.get('week_day') not in DAYS:
            E.append(f'{w}: Week day must be one of Monday..Sunday (R2)')
        if mode is None and not it.get('single') and it.get('week_day') is None:
            E.append(f'{w}: calendar post needs Week day (R2)')
        # R3 / R15 / R14 / R16
        if it.get('format') not in cal.get('allowed_formats', []):
            E.append(f'{w}: Format "{it.get("format")}" not in strategy categories (R3)')
        if t not in cal.get('allowed_types', []):
            E.append(f'{w}: Type "{t}" not allowed for this client')
        ref = refs.get(it.get('reference_url'))
        if mode == 'framework':
            if not it.get('creator') or not it.get('framework_slots'):
                E.append(f'{w}: framework post needs creator + framework_slots (internal)')
        elif not ref:
            E.append(f'{w}: Reference URL not found in research (R14)')
        else:
            if t == 'Carousel' or ref.get('type') == 'Carousel':
                if not (it.get('ratio_exception_by_cm') or ref.get('cm_viral_ok')):
                    E.append(f'{w}: carousel reference needs a CM decision on virality (no views on carousels) (R14)')
            elif ref.get('passes_ratio') is not True and ref.get('viral_signal') != 'OUTLIER' and not it.get('ratio_exception_by_cm'):
                E.append(f'{w}: reference does not pass the views/followers rule and has no CM exception (R14)')
            if ref.get('type') and ref['type'] != t and not it.get('rerecord_of_own_post'):
                E.append(f'{w}: Type {t} differs from reference Type {ref["type"]} (R15)')
            if not ref.get('type'):
                W.append(f'{w}: reference Type not classified from frames yet (R15)')
            if ref.get('type_status') == 'NEEDS_REVIEW':
                E.append(f'{w}: reference Type is NEEDS_REVIEW; CM must decide before use (R15)')
            if it.get('rerecord_of_own_post') and ref.get('hook') and t == 'Talking head':
                import difflib
                h = norm(re.sub(r'\[[^\]]*\]', '', ref['hook'])).split()
                sc = norm(it.get('script')).split()[:len(h)]
                if h and difflib.SequenceMatcher(None, h, sc).ratio() < 0.8:
                    E.append(f'{w}: re-record must keep the original hook (only transcription fixes allowed)')
            v = ref.get('views')
            if v and it.get('reference_views'):
                shown = float(re.sub(r'[^\d.]', '', it['reference_views']) or 0) * (1e6 if 'M' in it['reference_views'] else 1e3 if 'K' in it['reference_views'].upper() else 1)
                if abs(shown - v) / v > 0.06:
                    E.append(f'{w}: callout views {it["reference_views"]} != research {int(v):,} (R16)')
        # R4..R7 type-specific
        if mode == 'caption_only':
            pass
        elif t == 'Expert video':
            if not it.get('reaction_target_url'):
                E.append(f'{w}: Expert video without a concrete reaction target URL (R4)')
            if (it.get('script') or '').strip():
                E.append(f'{w}: Expert video must not carry a SCRIPT (R4)')
        if t == 'BTS' and mode != 'caption_only':
            if (it.get('script') or '').strip():
                E.append(f'{w}: BTS must not carry a spoken SCRIPT (R5)')
            if not it.get('onscreen_text'):
                E.append(f'{w}: BTS needs ON-SCREEN TEXT (R5)')
        if t == 'Carousel' and mode != 'caption_only' and len(it.get('carousel_slides') or []) < 3:
            E.append(f'{w}: Carousel needs every slide written (R6)')
        if t == 'Talking head' and mode != 'caption_only':
            if not (it.get('script') or '').strip():
                E.append(f'{w}: Talking head needs SCRIPT (R7)')
            if not it.get('reskin_table') and mode != 'framework':
                E.append(f'{w}: Talking head needs the internal original|new reskin table (R7)')
        # R1 / R18 client text hygiene
        for pat in BANNED_CLIENT_TEXT:
            if re.search(pat, body, re.I):
                E.append(f'{w}: client-facing text contains /{pat}/ (R1/R18)')
        # R10 / R17 slop
        for pat, name in SLOP:
            if re.search(pat, body, re.I):
                E.append(f'{w}: {name} in client text (R10/R17)')
        # R11 hashtags
        cap = (it.get('caption') or '').lower()
        found = re.findall(r'#\w+', cap)
        if tags and not all(tg in cap for tg in tags):
            E.append(f'{w}: caption must keep the client hashtags {tags} (R11)')
        extra = [x for x in found if x not in tags]
        if extra:
            W.append(f'{w}: extra hashtags {extra}; keep only if the client uses them (R11)')
        for term in cal.get('banned_terms', []):
            if term.lower() in body.lower():
                E.append(f'{w}: mentions "{term}" (not allowed for this client)')
        if re.search(r"\b(because|so that|this works|the reason|why we)\b", it.get('notes_for_client') or '', re.I):
            W.append(f'{w}: NOTES explain "why"; keep them to instructions')
        if not it.get('sources'):
            E.append(f'{w}: no internal sources for the topic (R9)')
        cap_words = len(re.split(r'(?<=[.!?])\s', (it.get('caption') or '').strip())[0].split())
        if cap_words > 12:
            W.append(f'{w}: caption opening sentence has {cap_words} words; Head of Content 1.5 wants a punchy hook (<=7 words ideal)')
        if not (it.get('notes_for_client') or '').strip():
            E.append(f'{w}: NOTES FOR THE CLIENT empty')

    # R12 duplicates
    names = Counter(norm(i.get('name')) for i in items)
    for n, c in names.items():
        if c > 1:
            E.append(f'duplicate Name x{c}: "{n}" (R12)')
    sent = defaultdict(set)
    for i in items:
        for s in re.split(r'(?<=[.!?])\s+', i.get('caption') or ''):
            if len(s) > 40:
                sent[norm(s)].add(i.get('id'))
    for s, ids in sent.items():
        if len(ids) > 1:
            W.append(f'same caption sentence in {sorted(ids)}: "{s[:60]}" (R12)')
    # R13 topic on consecutive days
    by_day = defaultdict(set)
    for i in cal['items']:
        by_day[(i.get('week'), i.get('week_day'))].add(i.get('topic'))
    for wk in {i.get('week') for i in cal['items']}:
        for a, b in zip(DAYS, DAYS[1:]):
            rep = (by_day[(wk, a)] & by_day[(wk, b)]) - {None}
            if rep:
                W.append(f'week {wk}: topic {sorted(rep)} on {a} and {b} (R13)')
    # category mix vs strategy (only meaningful with enough posts)
    mix = cal.get('category_mix') or {}
    if mix and len(items) >= 5:
        cnt = Counter(i.get('format') for i in items)
        for cat, pct in mix.items():
            got = 100 * cnt.get(cat, 0) / len(items)
            if abs(got - pct) > 15:
                W.append(f'category mix: {cat} {got:.0f}% vs strategy {pct}%')
    # R8 core objection present each week
    core = cal.get('core_objection_topic')
    if core and not day:
        for wk in {i.get('week') for i in cal['items']}:
            if not any(i.get('topic') == core for i in cal['items'] if i.get('week') == wk):
                E.append(f'week {wk}: no post on the core objection "{core}" (R8)')

    for e in E:
        print('ERROR', e)
    for x in W:
        print('WARN ', x)
    print(f'{len(items)} items checked: {len(E)} errors, {len(W)} warnings')
    return 1 if E else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
