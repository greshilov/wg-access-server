FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y cron vim && apt-get clean
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab && crontab /etc/cron.d/crontab

ADD requirements.txt /app
RUN pip install -r requirements.txt

ADD monitor /app/monitor
COPY main.py /app

# CMD ["cron", "-f"]
# CMD ["python", "-m", "gunicorn", "monitor.dashboard:server", "-b", "0.0.0.0:9010"]
