#!/usr/bin/env python3
"""Collect TikTok profiles automatically (replaces the manual SortFeed export for TikTok).
0 paid credits: yt-dlp metadata listing (no video download) + public profile page for followers.

Usage:
  python fetch_tiktok.py <accounts.csv> <out_dir> [--months 12] [--max 400] [--handles a,b]

- Reads every `platform = tiktok` row of accounts.csv (or only --handles).
- Followers: public profile page (followerCount) → written back into accounts.csv
  (followers, followers_source = "tiktok.com/@h profile <date> (auto)").
- Videos: newest first, up to --max, only the last --months. For each: views, likes, comments,
  shares, caption, date, and Outlier Score = views / median views of that account in the window.
- Writes <out_dir>/<handle>_tiktok_auto.csv with SortFeed's TikTok headers, so ingest_sortfeed.py
  reads it exactly like a manual export.
Saves are not in the listing (null); fetch_media.py adds them for shortlisted videos.
If TikTok blocks or changes something, the handle is reported as FAILED and the CM falls back
to a SortFeed export for that account.
"""
import argparse, csv, datetime as dt, json, os, re, statistics, subprocess, sys, urllib.request

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120 Safari/537.36')
HDR = ['Profile', 'TikTok', 'Create Date', 'Views', 'Outlier Score', 'Likes', 'Shares', 'Comments', 'Saves', 'Captions']


def followers(handle):
    req = urllib.request.Request(f'https://www.tiktok.com/@{handle}', headers={'User-Agent': UA})
    html = urllib.request.urlopen(req, timeout=30).read().decode('utf8', 'ignore')
    m = re.search(r'"followerCount":(\d+)', html)
    return int(m.group(1)) if m else None


def videos(handle, max_n):
    r = subprocess.run(['yt-dlp', '--flat-playlist', '-J', '--no-update', '--playlist-end', str(max_n),
                        f'https://www.tiktok.com/@{handle}'], capture_output=True, text=True, timeout=900)
    if r.returncode:
        raise RuntimeError((r.stderr.strip().splitlines() or ['yt-dlp failed'])[-1][:200])
    return json.loads(r.stdout).get('entries') or []


def main():
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument('accounts_csv'); ap.add_argument('out_dir')
    ap.add_argument('--months', type=int, default=12)
    ap.add_argument('--max', type=int, default=400)
    ap.add_argument('--handles', default='')
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    with open(a.accounts_csv, encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys()) if rows else []
    only = {h.strip().lstrip('@').lower() for h in a.handles.split(',') if h.strip()}
    cutoff = dt.datetime.now().timestamp() - a.months * 30.5 * 86400
    today = dt.date.today().isoformat()
    report = []
    for row in rows:
        if row['platform'].strip().lower() != 'tiktok':
            continue
        h = row['handle'].strip().lstrip('@').lower()
        if only and h not in only:
            continue
        try:
            fo = followers(h)
            if fo:
                row['followers'] = str(fo)
                row['followers_source'] = f'tiktok.com/@{h} profile {today} (auto)'
            ent = [e for e in videos(h, a.max) if (e.get('timestamp') or 0) >= cutoff]
            views = [e.get('view_count') or 0 for e in ent]
            med = statistics.median(views) if views else 0
            out = os.path.join(a.out_dir, f'{h}_tiktok_auto.csv')
            with open(out, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f); w.writerow(HDR)
                for e in ent:
                    v = e.get('view_count')
                    w.writerow([h, e.get('url') or e.get('webpage_url'),
                                dt.datetime.fromtimestamp(e['timestamp']).date().isoformat() if e.get('timestamp') else '',
                                v, round(v / med, 2) if v and med else '', e.get('like_count'), e.get('repost_count'),
                                e.get('comment_count'), '', (e.get('title') or e.get('description') or '').replace('\n', ' ')])
            viral = sum(1 for v in views if fo and v >= 2 * fo)
            outl = sum(1 for v in views if med and v >= 3 * med)
            report.append(f'OK  @{h}: followers {fo}, {len(ent)} videos in {a.months} mo, median {int(med):,}, '
                          f'{viral} pass 2x followers, {outl} outliers (>=3x median) -> {out}')
        except Exception as ex:
            report.append(f'FAILED @{h}: {ex}  -> use a SortFeed export for this account')
    with open(a.accounts_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print('\n'.join(report))
    return 1 if any(r.startswith('FAILED') for r in report) else 0


if __name__ == '__main__':
    sys.exit(main())
