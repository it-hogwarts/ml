FROM python:alpine as builder

WORKDIR /code
RUN apk --no-cache add musl-dev linux-headers g++ &&\
    python3 -m venv .env &&\
    .env/bin/python -m pip install --no-cache-dir numpy flask

FROM python:alpine

WORKDIR /code
COPY --from=builder /code/.env /code/.env

COPY . .

EXPOSE 8000

CMD .env/bin/python server.py