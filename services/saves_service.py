from flask_smorest import abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.saves import Save
from models.party import Party
import json
from flask import jsonify


def form_party_lead_obj(party):
    party_lead_name = party[0].name
    party_lead_level = party[0].level
    party_lead = {"name": party_lead_name, "level": party_lead_level}
    return party_lead

def get_all_saves():
    try:
        all_saves = Save.query.all()
        response = []
        for each_save in all_saves:
            location = each_save.location
            party_members = []
            party_lead = {}
            party = Party.query.filter_by(save_id=each_save.id).all()
            if len(party) > 0:
                for m in party:
                    party_members.append(m.name)
                party_lead = form_party_lead_obj(party)
            save_info = {
                "id": each_save.id,
                "location": location,
                "party": party_members,
                "party_lead": party_lead,
            }
            response.append(save_info)
        return jsonify(response)
    except SQLAlchemyError:
        abort(500, message="Error fetching all saves.")

# TODO: convert json using pydantic
def create_save(body):
    dumps_json = json.dumps(body)
    loaded_json = json.loads(dumps_json)
    new_save = Save(**loaded_json)
    try:
        db.session.add(new_save)
        db.session.commit()
        return {"id": new_save.id, "location": new_save.location}
    except IntegrityError as e:
        abort(400, message=str(e.__cause__))
    except SQLAlchemyError:
        db.session.rollback()
        abort(500, message="Error occurred whilst creating save.")


def delete_all_saves():
    try:
        count = Save.query.count()
        all_saves = Save.query.all()
        for s in all_saves:
            Party.query.filter_by(save_id=s.id).delete()
            db.session.commit()
        Save.query.delete()
        db.session.commit()
        return {"message": f"deleted {count} save file/s"}
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, message="Error deleting saves.")


def get_save_by_id(id):
    save_file = db.session.get(Save, id)
    if save_file is None:
        abort(404)
    party = Party.query.filter_by(save_id=id).all()
    party_members = []
    party_lead = {}
    if len(party) > 0:
        for m in party:
            party_members.append(m.name)
        party_lead = form_party_lead_obj(party)
    save_info = {
        "id": save_file.id,
        "location": save_file.location,
        "party": party_members,
        "party_lead": party_lead,
    }
    return save_info


def delete_save_by_id(id):
    try:
        save_file = db.session.get(Save, id)
        if save_file is None:
            abort(404)
        db.session.delete(save_file)
        db.session.commit()
        return {"message": f"deleted {id}"}
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, message="Error occured whislt deleting save.")
