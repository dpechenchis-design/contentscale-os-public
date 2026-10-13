#!/usr/bin/env python3
"""Get what the skill needs to classify a reference and adapt it 1:1:
frames (to judge the real visual mechanic -> Type) and a transcript.

Only for SHORTLISTED references (the ones that may go into the calendar),
never for the whole research table.

Usage:
  python fetch_media.py <reference_records.json> <work_dir> --urls <url> [<url> ...]
                        [--frames 8] [--model small] [--keep-video]

Per URL:
  1. yt-dlp downloads the public video into <work_dir>/media/<id>.mp4
  2. ffmpeg saves --frames evenly spaced JPG frames into <work_dir>/media/<id>/
  3. if the record has no SortFeed transcript, faster-whisper transcribes locally
     (transcript_status = WHISPER_LOCAL); on failure -> TRANSCRIPT_MISSING
  4. the video is deleted unless --keep-video
Writes frame paths + transcript back into reference_records.json.
Type is NOT decided here: the skill looks at the frames and sets type + type_evidence.

Requires yt-dlp and ffmpeg on PATH and the project venv (faster-whisper).
"""
import argparse, json, os, re, shutil, subprocess, sys


def vid_id(url):
    m = re.search(r'/(?:video|reel|p)/([A-Za-z0-9_-]+)', url)
    return m.group(1) if m else re.sub(r'\W+', '_', url)[-40:]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def duration(path):
    r = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path])
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument('records'); ap.add_argument('work_dir')
    ap.add_argument('--urls', nargs='+', required=True)
    ap.add_argument('--frames', type=int, default=8)
    ap.add_argument('--model', default='small')
    ap.add_argument('--keep-video', action='store_true')
    ap.add_argument('--lang', default='en', help="client's content language; other detected languages are treated as song/foreign audio")
    ap.add_argument('--ig-cookies', default='chrome',
                    help='browser[:profile] whose logged-in Instagram session yt-dlp uses for instagram.com URLs '
                         '(CM decision 2026-10-13); "none" disables it')
    a = ap.parse_args()
    for tool in ('yt-dlp', 'ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            sys.exit(f'{tool} not found on PATH. Install it (macOS: brew install {tool if tool != "ffprobe" else "ffmpeg"}).')

    data = json.load(open(a.records, encoding='utf8'))
    by_url = {r['reference_url']: r for r in data['records']}
    media = os.path.join(a.work_dir, 'media'); os.makedirs(media, exist_ok=True)
    whisper = None

    for url in a.urls:
        rec = by_url.get(url)
        if rec is None:
            print(f'SKIP not in records: {url}'); continue
        vid = vid_id(url)
        mp4 = os.path.join(media, f'{vid}.mp4')
        if not os.path.exists(mp4):
            cmd = ['yt-dlp', '-q', '--no-update', '--no-playlist', '-f', 'mp4/best', '-o', mp4]
            if 'instagram.com' in url and a.ig_cookies.lower() != 'none':
                cmd += ['--cookies-from-browser', a.ig_cookies]
            r = run(cmd + [url])
            if r.returncode or not os.path.exists(mp4):
                rec['media_status'] = 'DOWNLOAD_FAILED: ' + (r.stderr.strip().splitlines() or ['?'])[-1][:160]
                if 'instagram.com' in url:
                    rec['media_status'] += ' | fallback: SortFeed Transcribe + Download .txt (CM confirms the download)'
                print(f'FAIL download {url}: {rec["media_status"]}'); continue
        d = duration(mp4)
        rec['duration_sec'] = round(d, 1) if d else None
        fdir = os.path.join(media, vid); os.makedirs(fdir, exist_ok=True)
        if d:
            step = d / (a.frames + 1)
            frames = []
            for i in range(1, a.frames + 1):
                fp = os.path.join(fdir, f'f{i:02d}_{step * i:05.1f}s.jpg')
                run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{step * i:.2f}', '-i', mp4, '-frames:v', '1', '-vf', 'scale=540:-2', fp])
                if os.path.exists(fp):
                    frames.append(os.path.relpath(fp, a.work_dir))
            rec['frames'] = frames
            # one contact sheet per reference = one image to look at when deciding the Type
            cols = 4
            sheet = os.path.join(media, f'{vid}_sheet.jpg')
            run(['ffmpeg', '-y', '-loglevel', 'error', '-pattern_type', 'glob', '-i', os.path.join(fdir, 'f*.jpg'),
                 '-vf', f'scale=270:-2,tile={cols}x{-(-len(frames) // cols)}:padding=4', '-frames:v', '1', sheet])
            rec['contact_sheet'] = os.path.relpath(sheet, a.work_dir) if os.path.exists(sheet) else None
        if rec.get('transcript_status') != 'SORTFEED':
            try:
                if whisper is None:
                    from faster_whisper import WhisperModel
                    whisper = WhisperModel(a.model, device='cpu', compute_type='int8')
                # decode with ffmpeg (avoids PyAV incompatibilities): 16 kHz mono float32
                import numpy as np
                pcm = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', mp4, '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                                     capture_output=True).stdout
                audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
                segs, info = whisper.transcribe(audio, vad_filter=True)
                segs = list(segs)
                # VAD can drop speech under loud music: retry without it before calling a video silent
                if d and len(' '.join(s.text for s in segs).split()) / d < 0.6:
                    segs2, info2 = whisper.transcribe(audio, vad_filter=False)
                    segs2 = list(segs2)
                    if len(' '.join(s.text for s in segs2).split()) > len(' '.join(s.text for s in segs).split()):
                        segs, info = segs2, info2
                text = ' '.join(s.text.strip() for s in segs).strip()
                rec['transcript'] = text or None
                rec['transcript_timed'] = [[round(s.start, 1), round(s.end, 1), s.text.strip()] for s in segs]
                rec['transcript_lang'] = info.language
                # music lyrics / ambient noise are not a script: < ~0.6 words per second of video
                wps = len(text.split()) / d if d else 0
                rec['transcript_status'] = 'WHISPER_LOCAL' if wps >= 0.6 else 'NO_SPEECH_OR_MUSIC'
                if rec['transcript_status'] == 'WHISPER_LOCAL' and info.language and info.language != a.lang:
                    rec['transcript_status'] = 'FOREIGN_OR_SONG'  # e.g. lip-sync skit to a song: check frames, likely BTS
                if rec['transcript_status'] in ('NO_SPEECH_OR_MUSIC', 'FOREIGN_OR_SONG'):  # lyrics are not a script
                    rec['transcript_raw'], rec['transcript'] = rec['transcript'], None
            except Exception as e:  # keep going, never pretend
                rec['transcript_status'] = 'TRANSCRIPT_MISSING'
                rec['media_status'] = f'WHISPER_FAILED: {e}'[:200]
        rec.setdefault('media_status', 'OK')
        if not a.keep_video:
            os.remove(mp4)
        print(f"OK {url} | {rec.get('duration_sec')}s | frames {len(rec.get('frames', []))} | {rec['transcript_status']}")

    json.dump(data, open(a.records, 'w', encoding='utf8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
