#!/bin/sh

echo "---> run migrations"
flask db upgrade

echo "---> start server"
exec gunicorn --bind 0.0.0.0:7777 --log-level debug "app:create_app()"
