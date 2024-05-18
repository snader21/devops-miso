FROM alpine:3.14

RUN apk add py3-pip \
    && pip install --upgrade pip

WORKDIR /app
COPY . /app/
    
RUN pip install -r requirements.txt --ignore-installed six

EXPOSE 5000

ENV FLASK_APP=./src/app.py

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]

RUN pip install newrelic

ENV NEW_RELIC_APP_NAME="Blacklist"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=319f3248ed269e4ed4fa356dd95cd9817fe8NRAL
ENV NEW_RELIC_LOG_LEVEL=info

ENTRYPOINT [ "newrelic-admin", "run-program" ]