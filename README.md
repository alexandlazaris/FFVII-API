# FFVII-API

[![Release](https://github.com/alexandlazaris/FFVII-API/actions/workflows/release.yml/badge.svg)](https://github.com/alexandlazaris/FFVII-API/actions/workflows/release.yml)
[![Better Stack Badge](https://uptime.betterstack.com/status-badges/v2/monitor/2ghkb.svg)](https://uptime.betterstack.com/?utm_source=status_badge)

[![Unit tests](https://github.com/alexandlazaris/FFVII-API/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/alexandlazaris/FFVII-API/actions/workflows/unit-tests.yml)
![unit_tests_coverage](./custom_badges/coverage-badge.svg)
![tests_number](./custom_badges/tests-badge.svg)

Ever wanted to play FF7 ... one of the greatest games of all time ... as a REST API?! 

> [!WARNING]  
> This API is still in development. You have been warned.

## current game features

```
GET /saves
{
  "saves": [
    {
      "disc": 1,
      "id": "4d002c00-1187-4e59-92c2-22f8efd1ed1a",
      "location": "Temple of the Ancients",
      "party": {
        "id": "d0b5858d-a5e3-4e99-bd94-c8f6d4575bf9",
        "lead": {
          "level": 1,
          "name": "Cloud"
        },
        "members": [
          "Cloud"
        ]
      },
      "user_id": "b2c0d3e9-3aec-4e43-b451-8434fffa2f5d"
    }
  ]
}
```

- sign up and login to user profiles
- manage save files to hold location, disc and party info
- manage party members in save parties
- create & manage your save files, storing key info on your party & location
- read boss stats & descriptions
- ~~assign materia to party members~~ > broken, do not use, started this way too early
- read all in-game materia, filtering by type (e.g `magic`), element (e.g `fire`) and sort (`asc/desc`)

## coming soon

- full list of boss fights and associated details
- display party stats for level, hp/mp, equipment
- manage party member equipment (weapon, armour, accessory)

> [!NOTE]  
> If you have any ideas or feedback, please create an **Issue** or start a **Discussion**. Cheers!

## launch dev env

1. `python3 -m venv .venv` (or rename `.venv` to whatever you like)
2. `source .venv/bin/activate`
3. `docker compose down -v` (clear any previous volumes)
4. `docker compose up -d`
5. open `localhost:7777/swagger-ui` for api docs

## tests

### unit

From `./`:

1. run `coverage run -m pytest`
2. run `coverage html`
3. open `htmlcov/index.html` to view report

## tech stack

- Python 3.12.3
- **Web framework**: Flask (https://flask.palletsprojects.com/en/stable/), gunicorn
- **OpenAPI docs**: flask-smorest (https://flask-smorest.readthedocs.io/en/latest/openapi.html)
- **ORM**: SQLAlchemy (https://www.sqlalchemy.org/) + Flask-SQLAlchemy (https://flask-sqlalchemy.readthedocs.io/en/stable/)
- **DB**: postgresql
- **Data Validation**: pydantic (https://docs.pydantic.dev/latest/)
- **API client**: Bruno (https://www.usebruno.com/)
- **unit tests**: pytest + (https://coverage.readthedocs.io/en/7.8.0/)
- **custom README badges**: https://smarie.github.io/python-genbadge/
- **observability**: Logfire (https://pydantic.dev/logfire)
