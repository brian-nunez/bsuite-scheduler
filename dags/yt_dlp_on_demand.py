from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {"owner": "airflow"}

with DAG(
    dag_id="yt_dlp_download",
    start_date=datetime(2024, 1, 1),
    schedule=None,          # manual trigger
    catchup=False,
    default_args=default_args,
    description="Download highest-quality YouTube video via yt-dlp",
    params={
        "url": "",  # required
        # Pick best video+audio; if not available, fall back to best single stream
        "format": "bestvideo*+bestaudio/best",
        # Prefer highest res, then fps, then modern codecs, then bitrate/filesize
        "format_sort": "res,fps,codec:av1:vp9:h264,br,filesize",
        # Output location/pattern
        "outtmpl": "/opt/airflow/downloads/%(title)s.%(ext)s",
        # Optional extras (e.g., --cookies /path/cookies.txt)
        "extra": ""
    },
) as dag:
    bash = r"""
set -euo pipefail

URL="{{ params.url | default('', true) }}"
test -n "$URL" || { echo "param 'url' is required"; exit 2; }

FMT="{{ params.format | default('bestvideo*+bestaudio/best', true) }}"
FSORT="{{ params.format_sort | default('res,fps,codec:av1:vp9:h264,br,filesize', true) }}"
OUT="{{ params.outtmpl | default('/opt/airflow/downloads/%(title)s.%(ext)s', true) }}"
EXTRA="{{ params.extra | default('', true) }}"

mkdir -p /opt/airflow/downloads

# Highest quality + smart sorting + merge/remux to mp4 if needed
yt-dlp \
  --no-progress \
  --newline \
  -f "$FMT" \
  -S "$FSORT" \
  --merge-output-format mp4 \
  -o "$OUT" \
  $EXTRA \
  "$URL"
"""
    BashOperator(
        task_id="download_with_yt_dlp",
        bash_command=bash,
    )
