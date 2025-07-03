from flask_smorest import abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.saves import Save
from models.party import Party
import json
from flask import jsonify


def get_all_saves():
    all_saves = Save.query.all()
    response = []
    for s in all_saves:
        location = s.location
        members = []
        party = Party.query.filter_by(save_id=s.id)
        all = party.all()
        if len(all) > 0:
            print(f"save {s.id} has {len(all)} members")
            for m in all:
                members.append(m.name)
        if len(all) == 0:
            print(f"save {s.id} has no party")
        print(members)
        save_info = {"id": s.id, "location": location, "party": members}
        response.append(save_info)
    return jsonify(response)


def create_save(body):
    dumps_json = json.dumps(body)
    loaded_json = json.loads(dumps_json)
    new_save = Save(**loaded_json)
    try:
        db.session.add(new_save)
        db.session.commit()
    except IntegrityError as e:
        abort(400, message=str(e.__cause__))
    except SQLAlchemyError as e:
        abort(500, message="Error occurred whilst inserting record.")
    return {"id": new_save.id, "location": new_save.location}


def delete_all_saves():
    count = Save.query.count()
    all_saves = Save.query.all()
    for s in all_saves:
        Party.query.filter_by(save_id=s.id).delete()
        db.session.commit() 
    Save.query.delete()
    db.session.commit()    
    return {"message": f"deleted {count} save file/s"}

def get_save_by_id(id):
    save_file = Save.query.get_or_404(id)
    return save_file

def delete_save_by_id(id):
    try:
        save_file = Save.query.get_or_404(id)
        db.session.delete(save_file)
        db.session.commit()
    except SQLAlchemyError as e:
        abort(400, message="something went wrong")
    return {"message": f"deleted {id}"}