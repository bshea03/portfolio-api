FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y cron postgresql-client

COPY backup.sh /backup.sh
COPY crontab.txt /crontab.txt

RUN chmod +x /backup.sh && crontab /crontab.txt

CMD cron -f