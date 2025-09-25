FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends cron postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY backup.sh /backup.sh
COPY crontab.txt /crontab.txt

RUN chmod +x /backup.sh && crontab /crontab.txt

CMD cron -f