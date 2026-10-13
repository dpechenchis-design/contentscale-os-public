#!/usr/bin/env python3
"""Turn an Instagram Reels capture made in the browser into a SortFeed-format CSV,
so ingest_sortfeed.py reads it like a manual export (see references/instagram_browser_capture.md).

Usage:
  python ig_capture_to_csv.py <capture.json> <out_dir>

capture.json:
{"handle": "examplebrand", "followers": 14000, "captured_at": "2026-10-13",
 "reels": [{"url": "https://www.instagram.com/reel/DQUEcXKDmk8/", "views": 126000, "outlier": null,
            "likes": null, "comments": null}, ...]}

Only reels that were opened (have a url) are written; grid-only rows are counted in the report.
Also prints the followers line to put into accounts.csv.
"""
import csv, json, os, statistics, sys


def main(argv):
    if len(argv) != 3:
        sys.exit(__doc__)
    cap = json.load(open(argv[1], encoding='utf8'))
    h = cap['handle'].lstrip('@').lower()
    reels = cap.get('reels', [])
    views = [r['views'] for r in reels if r.get('views')]
    med = statistics.median(views) if views else None
    os.makedirs(argv[2], exist_ok=True)
    out = os.path.join(argv[2], f'{h}_ig_reels_browser.csv')
    n = 0
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Profile', 'Reel', 'Create Date', 'Views', 'Outlier Score', 'Likes', 'Comments'])
        for r in reels:
            if not r.get('url'):
                continue
            outl = r.get('outlier')
            if outl is None and med and r.get('views'):
                outl = round(r['views'] / med, 2)
            w.writerow([h, r['url'], r.get('date') or '', r.get('views'), outl, r.get('likes'), r.get('comments')])
            n += 1
    print(f'{n} reels with links -> {out} ({len(reels)} on the grid, median views {int(med or 0):,})')
    if cap.get('followers'):
        print(f"accounts.csv: instagram,{h},<role>,{cap['followers']},instagram.com/{h} profile {cap.get('captured_at', '')} (browser)")


if __name__ == '__main__':
    main(sys.argv)
