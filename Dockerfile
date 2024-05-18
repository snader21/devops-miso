FROM alpine:3.14

# Upgrade pip and install Python packages
RUN apk add py3-pip \
    && pip install --upgrade pip

WORKDIR /app
COPY . /app/

# Install Python dependencies, including New Relic
RUN pip install -r requirements.txt

# Set environment variables for Flask and New Relic
ENV FLASK_APP=./src/app.py
ENV NEW_RELIC_APP_NAME=black_list_app
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=404ceb0ac3b9cb226abf8ecfe6ea836e4129NRAL
ENV NEW_RELIC_LOG_LEVEL=info

EXPOSE 5000

# Configure the main command to be run by New Relic's wrapper
ENTRYPOINT ["newrelic-admin", "run-program"]
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
