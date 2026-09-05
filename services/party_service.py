from flask_smorest import abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import Party, Save, PartyMember
from schemas.party import (
    PartyResponse,
    PartyRequest,
    PartyMemberObj,
)
import logging

logger = logging.getLogger(__name__)


def create_party(body: list[dict], save_id) -> PartyResponse:
    # check if save is valid
    save = db.session.get(Save, save_id)
    if save == None:
        abort(404, message=f"Save not found.")

    # validate incoming payload
    partyList = [PartyRequest.model_validate(item) for item in body]

    # check if party length is valid
    if len(partyList) < 1 or len(partyList) > 3:
        abort(400, message="Party size invalid. Must be between 1-3 members.")

    has_existing_party = Party.query.filter_by(save_id=save_id).all()
    if has_existing_party:
        abort(400, message=f"Party already exists for save {save_id}.")

    # add new party
    party_params = {"save_id": save_id}
    party = Party(**party_params)
    try:
        db.session.add(party)
        db.session.commit()
    except SQLAlchemyError:
        abort(
            400,
            message=f"Error adding new party.",
        )

    party_id = party.id
    party_members = add_members_to_party(members=body, party_id=party_id)

    return PartyResponse(party=party_members, id=party_id)


def get_party_using_save(id) -> PartyResponse:
    try:
        party = Party.query.filter_by(save_id=id).first()
        party_id = party.id
        if party == None:
            abort(404, message=f"Party not found.")
        party_members_for_party_id = PartyMember.query.filter_by(
            party_id=party_id
        ).all()
        party_response = []
        for member in party_members_for_party_id:
            party_response.append(PartyMemberObj(name=member.name, level=member.level))
        return PartyResponse(party=party_response, id=party.id)
    except SQLAlchemyError:
        abort(500, message="Error getting save.")

def update_party_using_save(body: list[dict], save_id: str) -> PartyResponse:
    save = db.session.get(Save, save_id)
    if save == None:
        abort(404, message=f"Save not found.")

    party = Party.query.filter_by(save_id=save_id).one_or_none()
    if party == None:
        abort(404, message=f"Party not found for save {save_id}")
    party_id = party.id

    # delete existing party members from party
    try:
        party_members_in_party = PartyMember.query.filter_by(party_id=party_id).all()
        for member in party_members_in_party:
            db.session.delete(member)
        db.session.commit()
    except SQLAlchemyError():
        db.session.rollback()
        abort(500, message="Error when deleting party.")

    # add new members from request into party
    party_id = party.id
    party_members = add_members_to_party(members=body, party_id=party_id)
    return PartyResponse(party=party_members, id=party_id)


def add_members_to_party(members: list[dict], party_id: str):
    # validate incoming party
    party_member_list = [PartyRequest.model_validate(item) for item in members]

    if len(party_member_list) < 1 or len(party_member_list) > 3:
        abort(400, message="Party size invalid. Must be between 1-3 members.")

    # add new members from request into party
    response = []
    try:
        for member in party_member_list:
            db_member = PartyMember(name=member.name, party_id=party_id)
            db.session.add(db_member)
            response.append(PartyMemberObj(name=db_member.name, level=1))
        db.session.commit()
    except IntegrityError:
        abort(
            409,
            message=f"Error adding member to party, no duplicates allowed.",
        )
    return response
