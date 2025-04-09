# FFVII-API

> [!IMPORTANT]  
> This API is still in development. You have been warned.

## TODO

- add unit tests for all endpoints
- add integration tests for all endpoints
- add one-to-many relation for PartyMember<>Materia (dirty but functional logic used for now)
- create a PUT /party/{id}/materia to modify materia
- separate logic for materia/party validation into separate classes, make it resuable
- add github actions with semantic commit + releases
- consistent transforming and handling of JSON responses (e.g use jsonify? self create dicts?)
- add a save state mechanic, with all the generated Party data belonging to a save file (each party member will have an associated save_file_id column)

## Building to a docker container

1. run `sh docker-local-container.sh` to build and run a container (port 80)
2. target `0.0.0.0:80` for any local tests and debugging

## API docs

open `{url}:{port}/swagger-ui` for api docs

## DB migrations

- local dev: `sh migrations-run-local.sh`
- container: `sh docker-local-container`
- prod: `sh migrations-run-prod.sh`

## tech stack

- Python3
- **Web framework**: Flask (https://flask.palletsprojects.com/en/stable/), gunicorn
- **OpenAPI docs**: flask-smorest (https://flask-smorest.readthedocs.io/en/latest/openapi.html)
- **ORM**: SQLAlchemy (https://www.sqlalchemy.org/) + Flask-SQLAlchemy (https://flask-sqlalchemy.readthedocs.io/en/stable/)
- **DB + viewer**: sqlite for local, postgres for prod
- **API client**: Bruno (https://www.usebruno.com/)
