FROM python:3.10-alpine

WORKDIR /app
ADD monitor.py /app

COPY crontab /tmp/crontab
RUN cat /tmp/crontab > /etc/crontabs/root

CMD ["crond", "-f", "-l", "2"]
