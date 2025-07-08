#!/bin/sh

echo "---> building local image"

docker build -t dev-api-flask-ff7 .

echo "---> running local container"

docker run -dp 7777:7777 dev-api-flask-ff7:latest
