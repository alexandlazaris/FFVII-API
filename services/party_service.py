from flask_smorest import abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import Party, Save, PartyMember
from schemas.party import *
import logging

logger = logging.getLogger(__name__)

# define a response type here
def create_party(body: list[dict], id) -> CreatePartyResponse:
    target_save = db.session.get(Save, id)

    # validate incoming payload
    partyList = [PartyRequest.model_validate(item) for item in body]

    # check if save is valid
    if target_save == None:
        logger.error("Save id not provided")
        abort(404, message=f"Save {id} not found.")

    # check if party length is valid
    if partyList.__len__() < 1 or partyList.__len__() > 3:
        logger.error(f"Party size of {partyList.__len__()} invalid")
        abort(400, message="Party size invalid. Must be between 1-3 members.")

    # add new party
    party = Party(save_id=target_save.id)
    try:
        db.session.add(party)
        db.session.commit()
        logger.info("new party created")
    except IntegrityError as e:
        abort(
            400,
            message=f"Error adding new party. Ensure each party member is unique.",
        )

    # form party members
    party_id = party.id
    response: CreatePartyResponse = []
    try:
        for member in partyList:
            db_member = PartyMember(name=member.name, party_id=party_id)
            db.session.add(db_member)
            response.append(PartyResponse(name=db_member.name, level=1))
        db.session.commit()
    except IntegrityError as e:
        abort(
            400,
            message=f"Error adding new member. Only one of each character allowed.",
        )
    return response


def get_party_using_save(id):
    try:
        party = Party.query.filter_by(save_id=id)
        if party.first() == None:
            abort(404, message=f"Party with 'save_id' {id} cannot be found.")
        return party.all()
    except IntegrityError as e:
        abort(500, message="Something went wrong.")


# TODO: this delete->add->save approach is dirty, makes too many table changes. Need to improve this. Perhaps straight swap the party member's name instead?
def update_party_using_save(body, id):
    try:
        # step 1 - validate target save
        target_save = db.session.get(Save, id)
        if target_save == None:
            abort(404, message=f"Save {id} cannot be found. Ensure the save id valid.")
        # step 2 - delete existing party
        current_members = []
        party = Party.query.filter_by(save_id=id).all()
        for p in party:
            current_members.append(p.name)
        for delete in party:
            db.session.delete(delete)
        db.session.commit()
        # step 3 - form new party
        new_party = []
        for p in body:
            member = Party(name=p["name"], save_id=id)
            new_party.append(member)
        # step 4 - validate new party
        if new_party.__len__() < 1 or new_party.__len__() > 3:
            abort(400, message="Party size invalid. Must be between 1-3 members.")
        try:
            db.session.add_all(new_party)
            db.session.commit()
            return new_party
        except IntegrityError as e:
            abort(
                400,
                message=f"Error adding new members. Ensure each party member is unique.",
            )
        except SQLAlchemyError():
            db.session.rollback()
            abort(500, message="Error occurred whilst updating record.")
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, messcreate_partyage=f"Error updating party: {e._sql_message}")
