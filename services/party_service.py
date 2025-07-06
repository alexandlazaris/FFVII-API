from flask_smorest import abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import Party, Save


def create_party(body, id):
    Save.query.get_or_404(id)
    new_party = []
    for p in body:
        member = Party(name=p["name"], save_id=id)
        new_party.append(member)
    new_party_length = new_party.__len__()
    if new_party_length < 1 or new_party_length > 3:
        abort(400, message="Party size invalid. Must between 1-3 members.")
    try:
        db.session.add_all(new_party)
        db.session.commit()
    except IntegrityError as e:
        abort(
            400,
            message=f"A party already exists for this save. Instead, edit the party to modify your party members.",
        )
    except SQLAlchemyError():
        db.session.rollback()
        abort(500, message="Error occurred whilst inserting record.")
    return new_party


def get_party_using_save(id):
    try:
        party = Party.query.filter_by(save_id=id)
        if party.first() == None:
            abort(404, message=f"Party with 'save_id' {id} cannot be found.")
        return party.all()
    except IntegrityError as e:
        abort(500, message="Something went wrong.")


def update_party_using_save(body, id):
    # add step to validate incoming members
    # must be within 1-3 members - DONE
    # must be unique - TODO
    try:
        current_members = []
        party = Party.query.filter_by(save_id=id).all()
        for p in party:
            current_members.append(p.name)
        print(f"current party members: {current_members}")
        print(f"party members to clear: {len(current_members)}")

        for delete in party:
            db.session.delete(delete)

        db.session.commit()

        new_members = []
        for m in body:
            new_members.append(m["name"])
        print(f"new party members: {new_members}")
        return create_party(body, id)

    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, messcreate_partyage=f"Error updating party: {e._sql_message}")


def delete_party_using_save(id):
    try:
        party = Party.query.filter_by(save_id=id).all()
        count = len(party)
        for delete in party:
            db.session.delete(delete)
        db.session.commit()
        return {"message": f"deleted {count} party member/s"}
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, messcreate_partyage=f"Error deleting party: {e._sql_message}")
