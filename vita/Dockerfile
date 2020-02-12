FROM python:3.7-alpine3.10

WORKDIR /app

COPY di-vita.py /app
COPY requirements.txt /app

RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip install -r requirements.txt

CMD ["python",  "/app/di-vita.py"]