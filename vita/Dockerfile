FROM python:3.7-alpine3.10 as base

RUN apk add --update --no-cache g++ gcc libxslt-dev

FROM base as reqs


WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

FROM reqs as app

WORKDIR /app
COPY di-vita.py .

CMD ["python",  "/app/di-vita.py"]