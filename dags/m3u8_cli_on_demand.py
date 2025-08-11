from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {"owner": "airflow"}

with DAG(
    dag_id="m3u8_cli_on_demand",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    description="Download HLS via m3u8-cli",
    params={
        "url": "",
        "output": "output.mp4",
        "output_dir": "/opt/airflow/downloads",
        "timeout": 30,
        "quiet": False
    },
) as dag:
    bash = r"""
set -euo pipefail

command -v m3u8-cli >/dev/null 2>&1 || { echo "m3u8-cli not found in PATH"; exit 127; }

URL="{{ params.url | default('', true) }}"
OUT="{{ params.output | default('output.mp4', true) }}"
OUTDIR="{{ params.output_dir | default('/opt/airflow/downloads', true) }}"
TIMEOUT="{{ params.timeout | default(30, true) }}"
QUIET="{{ params.quiet | default(False, true) }}"

test -n "$URL" || { echo "param 'url' is required"; exit 2; }
mkdir -p "$OUTDIR"

QFLAG=""
if [ "$QUIET" = "True" ] || [ "$QUIET" = "true" ]; then
  QFLAG="--quiet"
fi

m3u8-cli \
  --url "$URL" \
  --output "$OUT" \
  --output-dir "$OUTDIR" \
  --timeout "$TIMEOUT" \
  $QFLAG
"""
    BashOperator(
        task_id="download_with_m3u8_cli",
        bash_command=bash,
    )
