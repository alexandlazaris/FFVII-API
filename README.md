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

## running
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements`
4. `flask run` to start api
5. open `http://localhost:5000/swagger-ui` for api docs

- built docker image: `docker build -t dev-api-flask-ff7 .`
- run container updating with local changes: `docker run -dp 50:5000 -w /app -v "$(pwd):/app" dev-api-flask-ff7`
- run docker container: `docker run -d -p 80:5000 api-flask-ff7`


## tech stack

- Python3
- **Web framework**: Flask (https://flask.palletsprojects.com/en/stable/)
- **OpenAPI docs**: flask-smorest (https://flask-smorest.readthedocs.io/en/latest/openapi.html)
- **ORM**: SQLAlchemy (https://www.sqlalchemy.org/) + Flask-SQLAlchemy (https://flask-sqlalchemy.readthedocs.io/en/stable/)
- **DB + viewer**: sqlite (https://www.sqlite.org/) + https://sqlitebrowser.org/
- **API client**: Bruno (https://www.usebruno.com/)

## dev notes
* when running with db, the container is getting import errors, so using local `flask run` in the meantime
* import errors gone after re-building the docker image. Always do this after adding new import or pip dependencies
* docker container logs sometimes only show after I auto-save in the editor. if I run an api, the endpoint is logged however my in-buitl debugging logs (i.e print()) require an editor change + save in order to appear in container logs

## findings

`PartyMemberSchema(many=True)` 

When defining arguments for an endpoint, e.g POST /party, `blp` allows you to provide a schema for the request. In addition, you can also provide an arg of `many=True`, which transforms the expected request schema to a `List`. This allows a single schema definition to be used, instead of 2 schemas (1 for single, 1 for many).

Several ORM provided error messages to display in API responses. You could combine these into custom messages, or hide sensitive query details into your logging solution. 

```
except IntegrityError as e:
            abort(400, message=e.params)  
            # e.params > shows input value triggering error
            # e.ismulti > returns bool if multiple params included
            # e._what_are_we > "error"
            # e.statement > shows SQL query used
            # e._sql_message() > SQL query error message
            # e.__cause > print SQL cause
``` 


## DB migrations

- from clean slate run `flask db init` to generate migrations resources
- run `flask db migrate` to generate migrate file based on model changes
* run `flask db upgrade` to apply latest migration