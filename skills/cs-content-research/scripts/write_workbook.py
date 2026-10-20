#!/usr/bin/env python3
"""Write reference_records.json into the canonical research workbook.

Usage:
  python write_workbook.py <reference_records.json> <out.xlsx> [--include-below-ratio] [--include-exceptions]
  --include-exceptions: also add EXCEPTION_1X / OUTLIER candidates (only flagged for accounts with < 5 posts at 2x; CM decision)

- Starts from assets/research_template.xlsx (the team's real tabs and headers,
  plus the approved "Carousels" tab). Decision 2026-10-20: no separate BTS / Expert videos /
  IG Competitors / Competitive analysis tabs; every video tab has a "Type" column instead
  (Type from frames; "not classified" until the skill has checked the frames) and a "Transcript"
  column next to each link (filled where a transcript exists). No "Accounts" tab.
- If <out.xlsx> already exists, human-set "Approved?" / "Used?" values are kept
  for every link that is already there (a re-run never overwrites approvals).
- "Approved?" is written only from approval_status set by a human
  (in_review -> "In Review ", approved -> "Approved "; the trailing spaces are
  the team's dropdown values). Default is blank.
- Only posts that pass the views/followers rule go in, unless --include-below-ratio.
  Competitors blocked at the approval gate never go in.
"""
import copy, json, os, sys
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, '..', 'assets', 'research_template.xlsx')
APPROVED = {'in_review': 'In Review ', 'approved': 'Approved '}
LINK_COLS = {'Video link', 'Reel', 'Post link'}


def compact(n):
    if n is None:
        return None
    n = float(n)
    if n >= 1e6:
        s = f'{n / 1e6:.1f}'.rstrip('0').rstrip('.') + ' M'
    elif n >= 1e3:
        s = f'{n / 1e3:.1f}'.rstrip('0').rstrip('.') + 'k'
    else:
        s = str(int(n))
    return s


def existing_marks(path):
    marks = {}
    if not os.path.exists(path):
        return marks
    wb = load_workbook(path, data_only=True)
    for ws in wb.worksheets:
        hdr = None
        for row in ws.iter_rows():
            vals = [c.value for c in row]
            if 'Approved?' in vals:
                hdr = vals
                continue
            if not hdr:
                continue
            d = dict(zip(hdr, vals))
            link = next((d[k] for k in LINK_COLS if d.get(k)), None)
            if link:
                marks[(ws.title, str(link).strip())] = (d.get('Approved?'), d.get('Used?'))
    return marks


def style_like(dst, src):
    dst.font = copy.copy(src.font); dst.fill = copy.copy(src.fill)
    dst.alignment = copy.copy(src.alignment); dst.border = copy.copy(src.border)


VIDEO_TABS = ['Best performing content IG', 'Best performing content Tik Tok', 'Competitors (IG)', 'Competitors (Tik Tok)']
DROP_TABS = ['BTS', 'Expert videos', 'IG Competitors', 'Competitive analysis']


def transcript_label(r):
    st = r.get('transcript_status')
    if r.get('transcript') and st in ('WHISPER_LOCAL', 'SORTFEED', 'TIKTOK_CAPTIONS'):
        return r['transcript']
    return {'NO_SPEECH_OR_MUSIC': 'no speech (music only)', 'FOREIGN_OR_SONG': 'song only, no speech'}.get(st)


def type_label(r):
    return r.get('type') if r.get('type_status') == 'CLASSIFIED' else 'not classified'


def add_type_column(ws):
    """Insert 'Type' and 'Transcript' before 'Approved?'."""
    for name, width in (('Transcript', 60), ('Type', 16)):
        hdr = [c.value for c in ws[1]]
        if name in hdr:
            continue
        i = hdr.index('Approved?') + 1 if 'Approved?' in hdr else len([h for h in hdr if h]) + 1
        ws.insert_cols(i)
        c = ws.cell(1, i, name)
        style_like(c, ws.cell(1, i + 1))
        ws.column_dimensions[c.column_letter].width = width


class Sheet:
    def __init__(self, ws, header_row):
        self.ws, self.hr = ws, header_row
        self.hdr = [c.value for c in ws[header_row] if c.value is not None]
        self.hdr_cells = [c for c in ws[header_row]][:len(self.hdr)]
        self.row = header_row + 1
        self.data_ranges = []
        self._start = self.row

    def new_block(self):
        """Blank row + repeated header, as in the team's competitor tabs."""
        if self.row > self.hr + 1:
            self._close()
            self.row += 1
            for i, src in enumerate(self.hdr_cells, 1):
                c = self.ws.cell(self.row, i, src.value)
                style_like(c, src)
            self.row += 1
            self._start = self.row

    def _close(self):
        if self.row > self._start:
            self.data_ranges.append((self._start, self.row - 1))
            self._start = self.row

    def add(self, values, marks, sheet_title):
        d = dict(values)
        link = next((d[k] for k in LINK_COLS if d.get(k)), None)
        if link and (sheet_title, link) in marks:
            appr, used = marks[(sheet_title, link)]
            d['Approved?'] = appr if appr is not None else d.get('Approved?')
            d['Used?'] = used if used is not None else d.get('Used?')
        for i, h in enumerate(self.hdr, 1):
            v = d.get(h)
            c = self.ws.cell(self.row, i, v)
            if h in LINK_COLS and v:
                c.hyperlink = v
                c.style = 'Hyperlink'
            if isinstance(v, float) and v.is_integer():
                c.value = int(v)
                c.number_format = '#,##0'
        self.row += 1

    def finish(self):
        self._close()
        if not self.data_ranges:
            return
        for col_name, formula in (('Approved?', '"In Review ,Approved "'), ('Used?', '"Yes,No"')):
            if col_name not in self.hdr:
                continue
            letter = self.ws.cell(1, self.hdr.index(col_name) + 1).column_letter
            dv = DataValidation(type='list', formula1=formula, allow_blank=True)
            for a, b in self.data_ranges:
                dv.add(f'{letter}{a}:{letter}{b}')
            self.ws.add_data_validation(dv)


def add_logic_sheets(wb, recs, ok):
    """Read-only sheet for the reviewer: why each post is in the table."""
    from openpyxl.styles import Font
    for name in ('Why selected',):
        if name in wb.sheetnames:
            del wb[name]
    ws = wb.create_sheet('Why selected')
    hdr = ['Account', 'Platform', 'Role', 'Link', 'Views', 'Followers', 'Views / followers', 'Signal',
           'Why selected', 'Type', 'Type evidence (frames)', 'Hook']
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in recs:
        if not ok(r):
            continue
        ws.append([r['source_account'], r['platform'], r.get('client_or_competitor'), r['reference_url'], r.get('views'),
                   r.get('followers'), r.get('views_to_followers'),
                   {'RATIO': '2x followers', 'EXCEPTION_1X': 'EXCEPTION (1x followers)', 'OUTLIER': 'EXCEPTION (3x median)'}.get(r.get('viral_signal'), ''),
                   r.get('eligibility_reason'), r.get('type'), r.get('type_evidence'), r.get('hook')])
        ws.cell(ws.max_row, 4).hyperlink = r['reference_url']


def main(records_json, out_xlsx, include_below=False, include_outliers=False):
    recs = json.load(open(records_json, encoding='utf8'))['records']
    marks = existing_marks(out_xlsx)
    wb = load_workbook(TEMPLATE)
    for name in DROP_TABS:
        if name in wb.sheetnames:
            del wb[name]
    for name in VIDEO_TABS:
        add_type_column(wb[name])
    S = {t: Sheet(wb[t], 1) for t in VIDEO_TABS + ['Carousels']}

    def ok(r):
        return r.get('approval_gate') == 'OK' and (r.get('passes_ratio') is True or include_below
                                                    or (include_outliers and r.get('viral_signal') in ('OUTLIER', 'EXCEPTION_1X')))

    counts = {k: 0 for k in S}
    last_comp = {}
    for r in recs:
        if not ok(r):
            continue
        base = {'Approved?': APPROVED.get(r.get('approval_status')), 'Used?': r.get('used_status') or 'No',
                'Followers on this account': compact(r.get('followers'))}
        is_client = r.get('client_or_competitor') == 'client'
        if r.get('type') == 'Carousel' or (r.get('media_kind') == 'post' and r.get('type') == 'Carousel'):
            t = 'Carousels'
            S[t].add({**base, 'Post link': r['reference_url'], 'Profile': r['source_account'],
                      'Slides': len(r['carousel_slides']) if r.get('carousel_slides') else None,
                      'Likes': r.get('likes'), 'Comments': r.get('comments'), 'Shares': r.get('shares'),
                      'Saves': r.get('saves'), 'Caption': r.get('caption')}, marks, t)
            counts[t] += 1
        elif r.get('media_kind') == 'post':
            continue  # image/carousel posts wait for a visual check before they go anywhere
        elif is_client:
            t = 'Best performing content Tik Tok' if r['platform'] == 'tiktok' else 'Best performing content IG'
            S[t].add({**base, 'Video link': r['reference_url'], 'Views on the video': r.get('views'),
                      'Caption': r.get('caption'), 'Type': type_label(r), 'Transcript': transcript_label(r)}, marks, t)
            counts[t] += 1
        else:
            t = 'Competitors (Tik Tok)' if r['platform'] == 'tiktok' else 'Competitors (IG)'
            if last_comp.get(t) not in (None, r['source_account']):
                S[t].new_block()
            last_comp[t] = r['source_account']
            S[t].add({**base, 'Profile': r['source_account'], 'Reel': r['reference_url'], 'Likes': r.get('likes'),
                      'Comments': r.get('comments'), 'Views': r.get('views'), 'Shares': r.get('shares'),
                      'Saves': r.get('saves'), 'Caption': r.get('caption'), 'Type': type_label(r), 'Transcript': transcript_label(r)}, marks, t)
            counts[t] += 1
    for s in S.values():
        s.finish()
    add_logic_sheets(wb, recs, ok)
    wb.save(out_xlsx)
    print(f'wrote {out_xlsx}')
    for k, v in counts.items():
        print(f'  {k}: {v}')
    kept = sum(1 for a, u in marks.values() if a is not None or u not in (None, 'No'))
    if kept:
        print(f'  kept {kept} human Approved?/Used? marks from the previous file')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 2:
        sys.exit(__doc__)
    main(*args, include_below='--include-below-ratio' in sys.argv, include_outliers='--include-exceptions' in sys.argv or '--include-outliers' in sys.argv)
