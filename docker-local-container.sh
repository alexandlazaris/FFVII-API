#!/bin/sh

echo "---> building local image"

docker build -t dev-api-flask-ff7 .

echo "---> running local container"

docker run --env-file .env -dp 7777:7777 dev-api-flask-ff7:latest
