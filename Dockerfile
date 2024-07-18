FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev build-essential cron && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

COPY . .

COPY crontab /etc/cron.d/my-cron-job

RUN chmod 0644 /etc/cron.d/my-cron-job

RUN touch /var/log/cron.log

RUN crontab /etc/cron.d/my-cron-job

CMD cron && tail -f /var/log/cron.log