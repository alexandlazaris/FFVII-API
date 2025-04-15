# FFVII-API

> [!IMPORTANT]  
> This API is still in development. You have been warned.

Ever wanted to play FF7 as a REST API?! Well now you can.

## TODO

### dev

- add unit tests 
- add integration tests for all endpoints (needs the below)
- create a docker compose file to create an env for running integration tests
- separate logic for materia/party validation into separate classes, make it resuable
- add github actions with semantic commit + releases
- consistent transforming and handling of JSON responses (e.g use jsonify? self create dicts?)
- install & setup https://logfire.pydantic.dev/docs/ for observability
- install & setup https://docs.pydantic.dev/latest/ for type validation
- increase materia effect length from 10 to 30

### game features

- add one-to-many relation for PartyMember<>Materia (dirty but functional logic used for now)
- create a PUT /party/{id}/materia to modify materia
- create a CRUD endpoint for save states
- add a save state mechanic, with all the generated Party data belonging to a save file (each party member will have an associated save_file_id column)
- create a encounter endpoint, with POST (start battle), PUT (actions in battle), POST (finish battle with link to battle id), GET (get all battles), GET /{id} (get battle by id)
- create a CRUD endpoint for game locations

## Building app within a docker container

1. run `sh docker-local-container.sh` to build and run a container (port 80)
2. target `0.0.0.0:80` for any local tests and debugging
3. open `{url}:{port}/swagger-ui` for api docs

## DB migrations

- local dev: `sh migrations-run-local.sh`
- container: `sh docker-local-container`
- prod: `sh migrations-run-prod.sh`

## tech stack

- Python3
- **Web framework**: Flask (https://flask.palletsprojects.com/en/stable/), gunicorn
- **OpenAPI docs**: flask-smorest (https://flask-smorest.readthedocs.io/en/latest/openapi.html)
- **ORM**: SQLAlchemy (https://www.sqlalchemy.org/) + Flask-SQLAlchemy (https://flask-sqlalchemy.readthedocs.io/en/stable/)
- **DB**: sqlite for local, postgres for prod
- **API client**: Bruno (https://www.usebruno.com/)
