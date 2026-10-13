#!/bin/sh
# One-time setup for every Content Manager machine (macOS).
# Creates ~/.contentscale-venv with the Python packages the cs-* skills use.
set -e
command -v yt-dlp >/dev/null || echo "Install yt-dlp:  brew install yt-dlp"
command -v ffmpeg >/dev/null || echo "Install ffmpeg:  brew install ffmpeg"
python3 -m venv "$HOME/.contentscale-venv"
"$HOME/.contentscale-venv/bin/pip" install -q --upgrade pip openpyxl faster-whisper
"$HOME/.contentscale-venv/bin/python" -c "import openpyxl, faster_whisper; print('cs-* skills: python env ready')"
