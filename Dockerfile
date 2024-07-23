FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y cron && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

COPY . .

COPY crontab /etc/cron.d/my-cron-job

RUN chmod 0644 /etc/cron.d/my-cron-job

RUN sed -i -e '$a\' /etc/cron.d/my-cron-job

RUN touch /var/log/cron.log

RUN crontab /etc/cron.d/my-cron-job

CMD cron && tail -f /var/log/cron.log