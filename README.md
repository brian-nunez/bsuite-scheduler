# BSuite Scheduler

The BSuite Scheduler is an [Apache Airflow](https://airflow.apache.org/) deployment that runs on your local network.
It’s designed to orchestrate and automate multimedia download workflows using two built-in DAGs:

* YouTube Downloader DAG — download the highest quality video + audio from YouTube.
* m3u8 Downloader DAG — download .m3u8 HLS streams or other ffmpeg-compatible sources using the [m3u8-cli](https://github.com/brian-nunez/m3u8-cli) tool.

---

## Features
* Local Airflow: Self-hosted Airflow stack with scheduler, webserver, and triggerer.
* Built-in Tools:
    - [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube and other site downloads.
    - [ffmpeg](https://ffmpeg.org/) for media processing.
    - [m3u8-cli](https://github.com/brian-nunez/m3u8-cli) for HLS/DASH stream downloads.
* Persistent Downloads: All downloaded media is stored in `/opt/airflow/downloads` inside the container (mapped to a host folder).

---

## DAGs Overview

1. yt_dlp_download
    * Purpose: Download the highest available quality video and audio from YouTube.
    * Parameters:
        - `url` (string, required) - the YouTube video URL.
        - `format` (string, optional) - format selection (default: bestvideo*+bestaudio/best).
        - `format_sort` (string, optional) - sorting preferences for streams (default: res,fps,codec:av1:vp9:h264,br,filesize).
        - `outtmpl` (string, optional) - output template (default: /opt/airflow/downloads/%(title)s.%(ext)s).
        - `extra` (string, optional) - additional yt-dlp CLI arguments.
    * Trigger: Manual run via Airflow UI => "Trigger DAG w/ config".

Example trigger JSON:
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

---

2. m3u8_cli_on_demand
    * Purpose: Download .m3u8 HLS streams or other URLs supported by ffmpeg using m3u8-cli.
    * Parameters:
      - `url` (string, required) - the HLS playlist or stream URL.
      - `output` (string, optional) - output file name (default: `output.mp4`).
      - `output_dir` (string, optional) - directory to store file (default: `/opt/airflow/downloads`).
      - `timeout` (int, optional) - timeout in seconds for stalled downloads (default: `30`).
      - `quiet` (bool, optional) - suppress ffmpeg logs.
    * Trigger: Manual run via Airflow UI => "Trigger DAG w/ config".

Example trigger JSON:
```json
{
  "url": "https://example.com/path/to/playlist.m3u8",
  "output": "movie.mp4"
}
```

---

## Getting Started

1. Build and run the Airflow stack:

```bash
docker compose up -d --build
```

2. Access the Airflow UI:
[http://localhost:8080](http://localhost:8080)
Login with your configured admin credentials.

3. Trigger a DAG

## Volumes

In `compose.yml`, the following volumes persist data:

* ./dags => /opt/airflow/dags
* ./logs => /opt/airflow/logs
* ./downloads => /opt/airflow/downloads (media output)
* ./data => /opt/airflow/data (Airflow metadata DB)

