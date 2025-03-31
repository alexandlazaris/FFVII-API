from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.party import PartyModel
from schemas.schemas import (
    PartyMemberSchema,
    DeleteSchema,
)

blp = Blueprint(
    "Party",
    __name__,
    url_prefix="/party",
    description="Endpoints for managing the party",
)


@blp.route("")
class Party(MethodView):
    @blp.response(200, PartyMemberSchema(many=True))
    def get(self):
        """
        Gets all party members

        Gets all party members and a count.
        """
        return PartyModel.query.all()

    @blp.arguments(PartyMemberSchema(many=True))
    @blp.response(201, PartyMemberSchema(many=True))
    def post(self, request):
        """
        Create a party.

        Add 1 of each character into your party, between 1-3 members.
        """
        request_party = []
        for p in request:
            member = PartyModel(**p)
            request_party.append(member)
        new_party_length = request_party.__len__()
        if(new_party_length < 1 or new_party_length > 3):
            abort(400, message="Party size invalid. Must between 1-3 members.")
        try:
            db.session.add_all(request_party)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message=str(e.__cause__))
        except SQLAlchemyError():
            abort(500, message="Error occurred whilst inserting record.")
        return request_party


@blp.route("<string:member_id>")
class Party(MethodView):
    @blp.response(200, PartyMemberSchema)
    def get(self, member_id):
        """
        Get a single party member by id.
        """
        member = PartyModel.query.get_or_404(member_id)
        return member

    @blp.response(200, DeleteSchema)
    def delete(self, member_id):
        """
        Delete a single party member by id.
        """
        try:
            party_member_to_delete = PartyModel.query.get_or_404(member_id)
            db.session.delete(party_member_to_delete)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message="something went wrong")
        return {"message": "deleted successfully"}


@blp.route("")
class Party(MethodView):
    @blp.response(200, DeleteSchema)
    def delete(self):
        """
        Delete all party members.
        """
        count = PartyModel.query.count()
        PartyModel.query.delete()
        db.session.commit()
        return {"message": f"deleted {count} party member/s"}
