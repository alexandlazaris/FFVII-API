from flask_smorest import abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.saves import Save
from models.party import Party
from schemas.saves import (
    GetSaveItemResponse,
    SaveItemCreateRequest,
    SaveItemCreateResponse,
    DeleteSaveResponse,
)
from uuid import UUID
from flask import jsonify
import logging
from flask import g

logger = logging.getLogger(__name__)


def form_party_lead_obj(party):
    party_lead_name = party[0].name
    party_lead_level = party[0].level
    party_lead = {"name": party_lead_name, "level": party_lead_level}
    return party_lead


def get_all_saves():
    try:
        logger.info("fetching all saves")
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
    except SQLAlchemyError as e:
        logger.error(str(e.__cause__))
        abort(500, message="Error fetching all saves.")


def create_save(new_save_request: SaveItemCreateRequest) -> SaveItemCreateResponse:
    body = SaveItemCreateRequest.model_validate(new_save_request)
    print(f"body validated: {body}", flush=True)
    print(f"body location: {body.location}", flush=True)
    try:
        user_id = g.user.user_id
        converted_user_id = UUID(user_id)
        save_params = {
            "user_id": converted_user_id,
            "location": body.location,
            "disc": body.disc,
        }
        new_save = Save(**save_params)
        db.session.add(new_save)
        db.session.commit()
        return SaveItemCreateResponse(
            id=new_save.id,
            user_id=new_save.user_id,
            location=new_save.location,
            disc=new_save.disc,
        )
    except IntegrityError as e:
        db.session.rollback()
        abort(400, message=f"Invalid request: {new_save_request}")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(e.__cause__)
        logger.error("exception: %s", e, exc_info=True)
        abort(500, message="Error occurred whilst creating save.")


def get_save_by_id(id) -> GetSaveItemResponse:
    save = db.session.get(Save, id)
    if save is None:
        logger.error(f"Not found")
        abort(404, message="Not found")
    party = Party.query.filter_by(save_id=id).all()
    party_members = []
    party_lead = {}
    if len(party) > 0:
        for m in party:
            party_members.append(m.name)
        party_lead = form_party_lead_obj(party)
    save_found = {
        "id": save.id,
        "location": save.location,
        "party": party_members,
        "party_lead": party_lead,
    }
    logger.info(f"save has been fetched: {save_found}")
    return GetSaveItemResponse(
        id=save.id, user_id=save.user_id, location=save.location, disc=save.disc
    )


def delete_save_by_id(id) -> DeleteSaveResponse:
    try:
        save_file = db.session.get(Save, id)
        if save_file is None:
            abort(404)
        db.session.delete(save_file)
        db.session.commit()
        return DeleteSaveResponse(message=f"deleted {id}")
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, message="Error deleting saves.")


def delete_all_saves() -> DeleteSaveResponse:
    try:
        count = Save.query.count()
        # all_saves = Save.query.all()
        # for s in all_saves:
        #     Party.query.filter_by(save_id=s.id).delete()
        #     db.session.commit()
        Save.query.delete()
        db.session.commit()
        return DeleteSaveResponse(message=f"deleted {count} save(s)")
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, message="Error deleting saves.")
