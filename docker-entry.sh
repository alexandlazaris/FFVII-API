#!/bin/sh

echo "---> run migrations"
flask db upgrade

echo "---> start server"
exec gunicorn --bind 0.0.0.0:80 "app:create_app()"
