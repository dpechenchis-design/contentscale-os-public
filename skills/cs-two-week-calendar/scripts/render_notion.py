#!/usr/bin/env python3
"""Render calendar items into Notion page payloads (properties + enhanced-markdown body)
exactly like the canonical "Week 1" calendar pages (references/notion_mapping.md).

Usage:
  python render_notion.py <calendar_items.json> <out_pages.json|out.md> [--day Monday] [--week 1] [--md]

out_pages.json = [{"id": item id, "properties": {...}, "content": "<markdown>"}]
Feed each entry to notion-create-pages (parent = the client's calendar data source).
Internal fields (sources, reskin_table, topic, feasibility, qa) are never rendered.
"""
import json, sys


def callout(it):
    if not it.get('reference_url'):
        return None  # framework posts: no reference callout
    acc = it.get('reference_account') or ''
    views = it.get('reference_views') or ''
    likes = it.get('reference_likes') or ''
    metric = f'{views} views' if views else (f'{likes} likes' if likes else '')
    label = f"@{acc.lstrip('@')}, {metric}" if acc and metric else (f'@{acc.lstrip("@")}' if acc else 'Reference')
    lines = [f"\t**Reference:** [{label}]({it['reference_url']})"]
    if it.get('type') == 'Expert video' and it.get('reaction_target_url'):
        u = it['reaction_target_url']
        lines.append(f"\t**React to this video:** [{u}]({u})")
    return '<callout icon="🎯" color="gray_bg">\n' + '\n'.join(lines) + '\n</callout>'


def esc(s):
    # "$" starts inline math in Notion enhanced markdown
    return (s or '').replace('$', '\\$')


def body(it):
    parts = [callout(it), '## **NOTES FOR THE CLIENT**', esc((it.get('notes_for_client') or '').strip())]
    t = it.get('type')
    if t == 'Talking head' and (it.get('script') or '').strip():
        parts += ['## SCRIPT', esc(it['script'].strip())]
    if t == 'BTS' and it.get('onscreen_text'):
        parts += ['## ON-SCREEN TEXT', '\n'.join(f'- {esc(x)}' for x in it['onscreen_text'])]
    if t == 'Carousel' and it.get('carousel_slides'):
        parts += ['## SLIDES', '\n'.join(f'**Slide {n}:** {esc(s)}' for n, s in enumerate(it['carousel_slides'], 1))]
    parts += ['## CAPTION', esc((it.get('caption') or '').strip())]
    return '\n'.join(p for p in parts if p is not None)


def props(it):
    p = {
        'Name': it['name'],
        'Status': it.get('status', 'Script ready'),
        'Type': json.dumps([it['type']]),
        'Format': json.dumps([it['format']]),
        'Platforms': json.dumps(it.get('platforms', [])),
    }
    if it.get('week_day'):
        p['Week day'] = it['week_day']
    if it.get('reference_url'):
        p['Reference'] = it['reference_url']
    # Source, Instructions, Publishing date, Edited video: intentionally left empty
    return p


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    cal = json.load(open(argv[1], encoding='utf8'))
    day = argv[argv.index('--day') + 1] if '--day' in argv else None
    week = int(argv[argv.index('--week') + 1]) if '--week' in argv else None
    md = '--md' in argv
    out = [{'id': it.get('id'), 'week': it.get('week'), 'properties': props(it), 'content': body(it)}
           for it in cal['items'] if (not day or it.get('week_day') == day) and (not week or it.get('week') == week)]
    if md:  # human preview: one markdown card per post
        with open(argv[2], 'w', encoding='utf8') as f:
            for o in out:
                f.write(f"# {o['properties']['Name']}\n\n" + '\n'.join(f"- **{k}:** {v}" for k, v in o['properties'].items() if k != 'Name') + '\n\n' + o['content'] + '\n\n---\n\n')
    else:
        json.dump(out, open(argv[2], 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'{len(out)} pages -> {argv[2]}')


if __name__ == '__main__':
    main(sys.argv)
