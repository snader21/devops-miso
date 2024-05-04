FROM alpine:3.14

RUN apk add py3-pip \
    && pip install --upgrade pip

WORKDIR /app
COPY . /app/
    
RUN pip install -r requirements.txt --ignore-installed six

EXPOSE 5000

ENV FLASK_APP=./src/app.py

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]