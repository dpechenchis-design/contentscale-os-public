#!/usr/bin/env python3
"""Verify that every call quote in client_context.json (and in the dossier) is real
and attributed to the right speaker.

Same idea as the dna-verify skill (VERBATIM / PARAPHRASE / NOT_FOUND + attribution),
adapted to Fathom transcripts ("MM:SS - Speaker Name: text") and to the
evidence_map of client_context.json.

Usage:
  python3 -I verify_context.py <client_context.json> <transcript.txt> [--dossier sections.js]
                               [--reviews sources/reviews_*.json] [--out report.csv]

--reviews: raw review feed ({"reviews":[{"id","title","body",...}]} or a list);
           evidence items with review_id are checked verbatim against it.

Exit code 1 if any call quote is NOT_FOUND or mis-attributed, or a dossier quote
is missing from the evidence_map.
"""
import csv, json, re, sys, unicodedata

FILLERS = {'um', 'uh', 'like', 'you', 'know', 'right', 'so', 'yeah', 'okay', 'actually', 'literally', 'honestly', 'i', 'mean'}
LINE_RE = re.compile(r'^(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*([^:]+?):\s?(.*)$')


def norm(s):
    s = unicodedata.normalize('NFKC', s).lower()
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = re.sub(r"[^a-z0-9' ]+", ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def words(s, drop_fillers=False):
    w = norm(s).split()
    return [x for x in w if x not in FILLERS] if drop_fillers else w


def fragments(quote):
    """Split on ellipses and [editor brackets]; brackets are corrections, not speech."""
    parts = re.split(r'\[[^\]]*\]|…|\.\.\.', quote)
    return [p for p in (x.strip() for x in parts) if len(words(p)) >= 3]


def load_transcript(path):
    turns = []
    for line in open(path, encoding='utf8'):
        m = LINE_RE.match(line.strip())
        if m:
            turns.append({'ts': m.group(1), 'speaker': m.group(2).strip(), 'text': m.group(3)})
    return turns


def contains(hay_words, needle_words):
    if not needle_words:
        return False
    n = len(needle_words)
    first = needle_words[0]
    for i, w in enumerate(hay_words):
        if w == first and hay_words[i:i + n] == needle_words:
            return True
    return False


def shingles(ws, k=5):
    return {' '.join(ws[i:i + k]) for i in range(max(0, len(ws) - k + 1))}


def check(quote, turns, full_words, full_shingles):
    frs = fragments(quote)
    if not frs:
        return 'TOO_SHORT', None
    found = [contains(full_words, words(f, True)) for f in frs]
    if all(found):
        verdict = 'VERBATIM'
    elif any(found) or (shingles(words(quote, True)) & full_shingles):
        verdict = 'PARAPHRASE'
    else:
        verdict = 'NOT_FOUND'
    # attribution: speaker whose turn contains the longest fragment's opening shingle
    probe = words(max(frs, key=len), True)[:6]
    speaker = None
    for t in turns:
        if contains(words(t['text'], True), probe):
            speaker = (t['speaker'], t['ts'])
            break
    if speaker is None and len(probe) >= 4:  # quote may straddle two turns
        for i in range(len(turns) - 1):
            if contains(words(turns[i]['text'] + ' ' + turns[i + 1]['text'], True), probe):
                speaker = (turns[i]['speaker'], turns[i]['ts'])
                break
    return verdict, speaker


def dossier_quotes(js):
    out = []
    for m in re.finditer(r"q:\[((?:\s*'(?:[^'\\]|\\.)*'\s*,?)+)\]", js):
        out += re.findall(r"'((?:[^'\\]|\\.)*)'", m.group(1))
    out += re.findall(r"\bq:'((?:[^'\\]|\\.)*)'", js)
    return [q.replace("\\'", "'") for q in out]


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    ctx = json.load(open(argv[1], encoding='utf8'))
    turns = load_transcript(argv[2])
    if not turns:
        sys.exit(f'No "MM:SS - Speaker: text" lines found in {argv[2]}')
    dossier = argv[argv.index('--dossier') + 1] if '--dossier' in argv else None
    out = argv[argv.index('--out') + 1] if '--out' in argv else argv[1].replace('.json', '_verify.csv')

    full_words = words(' '.join(t['text'] for t in turns), True)
    full_sh = shingles(full_words)
    call_ids = {s['source_id'] for s in ctx.get('sources', []) if 'call' in s.get('type', '')}

    reviews = {}
    if '--reviews' in argv:
        feed = json.load(open(argv[argv.index('--reviews') + 1], encoding='utf8'))
        for r in (feed.get('reviews', feed) if isinstance(feed, dict) else feed):
            reviews[str(r.get('id'))] = (r.get('title') or '') + ' ' + (r.get('body') or '')

    # quotes in working_model_evidence are verified like evidence_map quotes
    items = list(ctx.get('evidence_map', []))
    known_q = {norm(e['quote']) for e in items if e.get('quote')}
    for e in ctx.get('working_model_evidence', []):
        if isinstance(e, dict) and e.get('quote') and norm(e['quote']) not in known_q:
            items.append({**e, 'field': e.get('field', 'working_model_evidence')})

    rows, bad = [], 0
    for e in items:
        if not e.get('quote'):
            continue
        if e.get('source_id') not in call_ids:
            v = 'NON_CALL_SOURCE'
            if e.get('review_id') is not None and reviews:
                body = reviews.get(str(e['review_id']))
                if body is None:
                    v = 'REVIEW_ID_NOT_FOUND'
                else:
                    bw = words(body)
                    v = 'REVIEW_VERBATIM' if all(contains(bw, words(f)) for f in fragments(e['quote']) or [e['quote']]) else 'REVIEW_NOT_FOUND'
                if v != 'REVIEW_VERBATIM':
                    bad += 1
            rows.append({**e, 'verdict': v, 'found_speaker': '', 'found_ts': '', 'attribution': 'n/a'})
            continue
        v, sp = check(e['quote'], turns, full_words, full_sh)
        attr = 'n/a'
        if sp and e.get('speaker'):
            attr = 'OK' if norm(e['speaker']).split()[0] == norm(sp[0]).split()[0] else 'MISMATCH'
            # Fathom diarization often shifts turn boundaries; a mismatch is acceptable
            # only when a human checked the recording and wrote attribution_note.
            if attr == 'MISMATCH' and e.get('attribution_note'):
                attr = 'MISMATCH_REVIEWED'
        if v == 'NOT_FOUND' or attr == 'MISMATCH':
            bad += 1
        rows.append({**e, 'verdict': v, 'found_speaker': sp[0] if sp else '', 'found_ts': sp[1] if sp else '', 'attribution': attr})

    orphan = []
    if dossier:
        known = {norm(e['quote']) for e in ctx.get('evidence_map', []) if e.get('quote')}
        for q in dossier_quotes(open(dossier, encoding='utf8').read()):
            if norm(q) not in known:
                orphan.append(q)

    keys = ['field', 'claim', 'source_id', 'speaker', 'timestamp', 'quote', 'kind', 'review_id', 'verdict', 'found_speaker', 'found_ts', 'attribution', 'attribution_note']
    with open(out, 'w', newline='', encoding='utf8') as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)

    from collections import Counter
    c = Counter(r['verdict'] for r in rows)
    print(f'Quotes checked: {len(rows)}  ' + '  '.join(f'{k}={v}' for k, v in sorted(c.items())))
    reviewed = [r for r in rows if r['attribution'] == 'MISMATCH_REVIEWED']
    if reviewed:
        print(f'Attribution overrides to spot-check in the recording ({len(reviewed)}):')
        for r in reviewed:
            print(f"  @{r['found_ts']} transcript={r['found_speaker']} ours={r.get('speaker')} | {r.get('attribution_note', '')[:90]}")
    for r in rows:
        if r['verdict'] in ('REVIEW_NOT_FOUND', 'REVIEW_ID_NOT_FOUND'):
            print(f"  {r['verdict']} id={r.get('review_id')} {r['quote'][:90]}")
        if r['verdict'] == 'NOT_FOUND':
            print(f"  NOT_FOUND  [{r.get('speaker')}] {r['quote'][:110]}")
        if r['attribution'] == 'MISMATCH':
            print(f"  MISMATCH   said by {r['found_speaker']} @{r['found_ts']}, dossier says {r.get('speaker')}: {r['quote'][:80]}")
    if dossier:
        print(f'Dossier quotes not in evidence_map: {len(orphan)}')
        for q in orphan:
            print('  ORPHAN', q[:110])
    print(f'CSV: {out}')
    return 1 if (bad or orphan) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
