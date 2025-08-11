FROM golang:1.22-alpine AS builder
RUN apk add --no-cache git
RUN go install github.com/brian-nunez/m3u8-cli@latest

FROM apache/airflow:2.10.2-python3.11

USER root
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
  && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install --no-cache-dir yt-dlp

COPY --from=builder /go/bin/m3u8-cli /usr/local/bin/m3u8-cli
