#!/usr/bin/env python3
"""Where is this client in the ContentSCALE pipeline, and what happens next?

Usage:
  python3 -I pipeline_status.py clients/<slug>                       # status + next action
  python3 -I pipeline_status.py clients/<slug> --approve <gate> [--note "..."]   # record a CM decision
  python3 -I pipeline_status.py clients/<slug> --set <key>=<value>   # e.g. strategy_design_id=DAH...

Gates (recorded only when the Content Manager says yes in the chat):
  dossier            CM approved the client dossier
  competitors        CM approved/rejected AI-found competitors (or none were needed)
  research           CM reviewed the research table
  strategy           CM approved the Canva strategy preview (then commit happens)
  calendar_test_page CM approved the first Notion test page
  calendar_w<N>_<Day> CM approved that calendar day (e.g. calendar_w1_Monday)

State lives in clients/<slug>/pipeline_state.json, so any CM can continue where another stopped.
"""
import datetime as dt, glob, json, os, sys

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def load(p, default=None):
    try:
        return json.load(open(p, encoding='utf8'))
    except Exception:
        return default


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    c = argv[1].rstrip('/')
    if not os.path.isdir(c):
        sys.exit(f'No client folder {c}. Create it: mkdir -p {c}/sources (stage 1 starts there).')
    sp = os.path.join(c, 'pipeline_state.json')
    st = load(sp, {}) or {}
    st.setdefault('gates', {})
    now = dt.datetime.now().isoformat(timespec='minutes')
    if '--approve' in argv:
        g = argv[argv.index('--approve') + 1]
        note = argv[argv.index('--note') + 1] if '--note' in argv else ''
        st['gates'][g] = {'approved_at': now, 'note': note}
        json.dump(st, open(sp, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        print(f'recorded gate {g}')
        return 0
    if '--set' in argv:
        k, v = argv[argv.index('--set') + 1].split('=', 1)
        st[k] = v
        json.dump(st, open(sp, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        print(f'set {k}')
        return 0

    G = st['gates']
    rows, blockers, next_action = [], [], None
    has = lambda p: os.path.exists(os.path.join(c, p))

    # Stage 1
    ctx = load(os.path.join(c, 'context/client_context.json'))
    transcripts = [p for p in glob.glob(os.path.join(c, 'sources/*.txt'))]
    if not transcripts:
        s1 = 'NOT STARTED'; next_action = next_action or 'Stage 1: get the Unpacking transcript (Fathom link or file) → cs-client-context'
    elif not ctx:
        s1 = 'IN PROGRESS'; next_action = next_action or 'Stage 1: build client_context.json + dossier (cs-client-context)'
    else:
        wm = ctx.get('client_working_model')
        qs = ctx.get('missing_critical_questions') or []
        s1 = f'DONE (Working Model {wm})'
        if wm == 'UNKNOWN':
            blockers.append('Working Model UNKNOWN: ask CM whether the client records new content')
        if not has('onboarding_brief.md'):
            blockers.append('onboarding_brief.md missing: team fills it from brain/onboarding_brief_template.md (materials, 5-source rule, Working Model)')
        if not has('client_rules.md'):
            blockers.append('client_rules.md missing: create from brain/client_rules_template.md')
        if 'dossier' not in G:
            s1 += ' · waiting: CM approval of dossier'
            next_action = next_action or 'Stage 1 gate: show the dossier (Artifact) + critical questions to CM'
        if qs:
            s1 += f' · {len(qs)} open questions'
    rows.append(('1 Client Context', s1))

    # Stage 2
    recs = load(os.path.join(c, 'research/reference_records.json'))
    exports = glob.glob(os.path.join(c, 'sources/sortfeed/*')) + glob.glob(os.path.join(c, 'sources/auto/*'))
    if not ctx:
        s2 = 'BLOCKED by stage 1'
    elif not exports and not recs:
        s2 = 'NOT STARTED'; next_action = next_action or 'Stage 2: confirm accounts.csv → fetch_tiktok.py (auto) + Instagram via browser (instagram_browser_capture.md)'
    elif not recs:
        s2 = 'IN PROGRESS'; next_action = next_action or 'Stage 2: ingest_sortfeed.py → write_workbook.py'
    else:
        R = recs.get('records', [])
        blocked = {r['source_account'] for r in R if r.get('approval_gate') == 'BLOCKED_PENDING_APPROVAL'}
        classified = sum(1 for r in R if r.get('type_status') == 'CLASSIFIED')
        passing = sum(1 for r in R if r.get('passes_ratio') is True)
        s2 = f'DONE ({len(R)} posts, {passing} pass 2×, {classified} Type-classified)'
        if blocked:
            blockers.append(f'AI-found competitors waiting for CM: {sorted(blocked)}')
        if 'research' not in G:
            s2 += ' · waiting: CM review'
            next_action = next_action or 'Stage 2 gate: show research table summary to CM'
    rows.append(('2 Content Research', s2))

    # Stage 3
    strat = load(os.path.join(c, 'strategy/strategy_content.json'))
    if not recs:
        s3 = 'BLOCKED by stage 2'
    elif not strat:
        s3 = 'NOT STARTED'; next_action = next_action or 'Stage 3: cs-content-strategy (ask CM for cadence/Types if missing)'
    else:
        cad = strat.get('cadence') or {}
        s3 = 'DRAFT' if 'strategy' not in G else 'APPROVED'
        if not cad:
            blockers.append('Strategy has no cadence: ask CM')
        if st.get('strategy_design_id'):
            s3 += f" · Canva {st['strategy_design_id']}"
        if 'strategy' not in G:
            next_action = next_action or 'Stage 3 gate: Canva preview → CM yes → commit'
    rows.append(('3 Content Strategy', s3))

    # Stage 4
    cal = load(os.path.join(c, 'calendar/calendar_items.json'))
    if not strat or 'strategy' not in G:
        s4 = 'BLOCKED by stage 3'
    elif not cal:
        s4 = 'NOT STARTED'; next_action = next_action or 'Stage 4: cs-two-week-calendar (plan → references → texts → QA → 1 test page)'
    else:
        items = cal.get('items', [])
        done_days = [k for k in G if k.startswith('calendar_w')]
        s4 = f'{len(items)} posts drafted · {len(done_days)} day(s) approved'
        if 'calendar_test_page' not in G:
            next_action = next_action or 'Stage 4 gate: write ONE test page to Notion → CM yes'
        else:
            for w in (1, 2):
                for d in DAYS:
                    if f'calendar_w{w}_{d}' not in G:
                        next_action = next_action or f'Stage 4: write + review week {w} {d}'
                        break
                else:
                    continue
                break
    rows.append(('4 Two-week Calendar', s4))

    st['last_status_at'] = now
    json.dump(st, open(sp, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'Client: {os.path.basename(c)}')
    for a, b in rows:
        print(f'  {a:<22} {b}')
    for b in blockers:
        print(f'  BLOCKER: {b}')
    print(f'NEXT: {next_action or "Pipeline complete: two weeks approved in Notion"}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
