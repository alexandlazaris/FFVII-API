from flask_smorest import abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.materia import MateriaModel
import json
from sqlalchemy import desc, asc
from game_data.materia.materia_data import materia_data


def get_materia_with_filters(params):
    print("filtering")
    query = MateriaModel.query
    if "type" in params:
        param = params["type"]
        if param != "":
            query = query.filter_by(type=param)

    if "element" in params:
        param = params["element"]
        if param != "":
            query = query.filter_by(element=param)

    if "sort" in params:
        param = params["sort"]
        if param != "":
            if param == "asc":
                query = query.order_by(asc(MateriaModel.name))
            elif param == "desc":
                query = query.order_by(desc(MateriaModel.name))
    return query.all()


def seed_materia_data():
    query = MateriaModel.query
    if query.count() == materia_data.__len__():
        print("materia data has already been seeded, skipping", flush=True)
        abort(400)
    else:
        # TODO: below needs to be refactored, messy json handling
        dumps_json = json.dumps(materia_data)
        loaded_json = json.loads(dumps_json)
        for index in loaded_json:
            m = {
                "name": index["name"],
                "element": index["element"],
                "type": index["type"],
            }
            materia = MateriaModel(**m)
            try:
                db.session.add(materia)
                db.session.commit()
            except IntegrityError as e:
                abort(400, message=e._message)
            except SQLAlchemyError():
                abort(500, message="Error occurred whilst inserting record.")
        return MateriaModel.query.all()
