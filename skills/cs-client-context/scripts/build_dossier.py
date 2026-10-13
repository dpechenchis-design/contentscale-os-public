#!/usr/bin/env python3
"""Fill assets/dossier_shell.html with client meta + section JS.

Usage:
  python3 -I build_dossier.py <meta.json> <sections.js> <out.html>

meta.json keys: TITLE, MARK, CLIENT_NAME, BIZ_LINE, SIDE_FOOT, FOOT_SOURCES,
                DATA_FLAG, SLUG, CONSTANTS_JS (string or path ending in .js)
sections.js: the body of the `S` array (objects separated by commas),
             written with the shell helpers (head, entries, litems, bars...).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHELL = os.path.join(HERE, '..', 'assets', 'dossier_shell.html')
REQUIRED_IDS = ['overview', 'value', 'matrix', 'persona', 'icp', 'content',
                'questions', 'objections', 'beliefs', 'desires', 'pains', 'triggers', 'fears',
                'hero', 'competitors', 'iceberg', 'whitespace',
                'snapshot', 'praise', 'wrong', 'switch', 'psych', 'transform']


def main(meta_path, sections_path, out_path):
    meta = json.load(open(meta_path, encoding='utf8'))
    sections = open(sections_path, encoding='utf8').read().strip().rstrip(',')
    cj = meta.get('CONSTANTS_JS', '')
    if cj.endswith('.js') and os.path.exists(os.path.join(os.path.dirname(meta_path), cj)):
        cj = open(os.path.join(os.path.dirname(meta_path), cj), encoding='utf8').read()
    meta['CONSTANTS_JS'] = cj
    meta['SECTIONS_JS'] = sections

    ids = re.findall(r"\{id:'([a-z]+)'", sections)
    problems = []
    if ids != REQUIRED_IDS:
        missing = [i for i in REQUIRED_IDS if i not in ids]
        extra = [i for i in ids if i not in REQUIRED_IDS]
        problems.append(f'section order/ids differ from S10. missing={missing} extra={extra} got={ids}')

    html = open(SHELL, encoding='utf8').read()
    for k, v in meta.items():
        html = html.replace('{{' + k + '}}', v)
    left = sorted(set(re.findall(r'\{\{([A-Z_]+)\}\}', html)))
    if left:
        problems.append(f'unfilled placeholders: {left}')
    open(out_path, 'w', encoding='utf8').write(html)
    print(f'wrote {out_path} ({len(html):,} bytes, {len(ids)} sections)')
    for p in problems:
        print('WARN:', p)
    return 1 if problems else 0


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    sys.exit(main(*sys.argv[1:]))
