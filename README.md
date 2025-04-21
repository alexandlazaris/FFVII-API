# FFVII-API

Ever wanted to play FF7 ... one of the greatest games of all time ... as a REST API?! 

> [!WARNING]  
> This API is still in development. You have been warned.

## current game features

- choose your party of 3 from playable characters
- manage all your party materia 
- obtain enemy stats and modify as needed

## coming soon

- save states to contain all game data
- full in-game materia lists
- full in-game enemy details
- improved db relationships between Party members, Materia & Save States 
- wild encounters to fight enemies and gain XP/AP/Gil

> [!NOTE]  
> If you have any ideas or feedback, please create an **Issue** or start a **Discussion**. Cheers!

## launch API in container

1. run `sh docker-local-container.sh` to build and run a container (port 80)
2. target `0.0.0.0:80` for any local tests and debugging
3. open `{url}:{port}/swagger-ui` for api docs

## launch API locally

> [!TIP]  
> Use a virtual python env to isolate your workspace. 

1. clone repo & start with `pip install -r requirements.txt`
2. run `sh migrations-run-local.sh` to prep your db 
3. start server using `gunicorn --bind 0.0.0.0:80 "app:create_app()"`
4. jump to `localhost:80/swagger-ui` for api docs

## tests

- unit: `coverage run -m pytest && coverage html`

## tech stack

- Python 3.12.3
- **Web framework**: Flask (https://flask.palletsprojects.com/en/stable/), gunicorn
- **OpenAPI docs**: flask-smorest (https://flask-smorest.readthedocs.io/en/latest/openapi.html)
- **ORM**: SQLAlchemy (https://www.sqlalchemy.org/) + Flask-SQLAlchemy (https://flask-sqlalchemy.readthedocs.io/en/stable/)
- **DB**: sqlite for local, postgres for prod
- **API client**: Bruno (https://www.usebruno.com/)
- **unit tests**: pytest + (https://coverage.readthedocs.io/en/7.8.0/)