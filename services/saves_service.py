from flask_smorest import abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.saves import Save
from models.party import Party
from models.party_member import PartyMember
from schemas.saves import (
    GetSaveItemResponse,
    SaveItemCreateRequest,
    SaveItemCreateResponse,
    DeleteSaveResponse,
    GetAllSaves,
    PartyLead,
    PartyResult,
)
from uuid import UUID
import logging
from flask import g
from services.user.user_service import get_user_id

logger = logging.getLogger(__name__)


def form_party_lead_obj(lead: PartyLead):
    party_lead_name = lead.name
    party_lead_level = lead.level
    party_lead = {"name": party_lead_name, "level": party_lead_level}
    return party_lead


def map_party_data_in_save(party_id: UUID) -> PartyResult | None:
    party_members_list = PartyMember.query.filter_by(party_id=party_id).all()
    if len(party_members_list) > 0 and len(party_members_list) <= 3:
        first_party_member = party_members_list[0]
        party_lead_stats = PartyLead(
            name=first_party_member.name, level=first_party_member.level
        )
        party_members = [member.name for member in party_members_list]
        return PartyResult(id=party_id, lead=party_lead_stats, members=party_members)


def get_all_saves() -> GetAllSaves:
    response = []
    all_saves = Save.query.filter_by(user_id=get_user_id()).all()
    for save in all_saves:
        party_result = PartyResult()
        save_id = save.id
        party = Party.query.filter_by(save_id=save_id).one_or_none()
        # TODO: potentially pass the whole party in here instead of the id only, running the check and the mapping within
        if party is not None:
            party_result = map_party_data_in_save(party.id)
        save = GetSaveItemResponse(
            id=save_id,
            user_id=save.user_id,
            location=save.location,
            disc=save.disc,
            party=party_result,
        )
        response.append(save)
    return GetAllSaves(saves=response)


def create_save(new_save_request: SaveItemCreateRequest) -> SaveItemCreateResponse:
    body = SaveItemCreateRequest.model_validate(new_save_request)
    try:
        save_params = {
            "user_id": get_user_id(),
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
        abort(500, message="Error occurred whilst creating save.")


def get_save_by_id(save_id) -> GetSaveItemResponse:
    save = Save.query.filter_by(id=save_id, user_id=get_user_id()).one_or_none()
    if save is None:
        abort(404, message="Not found")
    party_result = PartyResult()
    party = Party.query.filter_by(save_id=save_id).one_or_none()
    if party is not None:
        party_result = map_party_data_in_save(party.id)
    return GetSaveItemResponse(
        id=save_id,
        user_id=save.user_id,
        location=save.location,
        disc=save.disc,
        party=party_result,
    )


def delete_save_by_id(save_id) -> DeleteSaveResponse:
    try:
        save = Save.query.filter_by(id=save_id, user_id=get_user_id()).one_or_none()
        if save is None:
            abort(404, message="Not found")
        db.session.delete(save)
        db.session.commit()
        return DeleteSaveResponse(message=f"deleted {save_id}")
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, message="Error deleting saves.")


def delete_all_saves() -> DeleteSaveResponse:
    try:
        saves = Save.query.filter_by(user_id=get_user_id()).all()
        count = len(saves)
        if saves:
            for save in saves:
                db.session.delete(save)
            db.session.commit()
        return DeleteSaveResponse(message=f"deleted {count} save(s)")
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, message="Error deleting saves.")
