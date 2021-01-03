FROM python:3
ENV PYTHONUNBUFFERED=1
# Install crontab
RUN apt update && apt install cron unzip -y

# Copy cron file
COPY update-score-cron /etc/cron.d/update-score-cron
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/update-score-cron
# Apply cron job
RUN crontab /etc/cron.d/update-score-cron
# Create the log file to be able to run tail
RUN touch /var/log/update-score-cron.log
# Run the command on container startup
CMD cron

# Copy django project
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
