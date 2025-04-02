from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import PartyModel, PartyMateriaModel, MateriaModel
from schemas.schemas import PartyMemberSchema, DeleteSchema, AssignMateriaSchema

import json

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
        if new_party_length < 1 or new_party_length > 3:
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


@blp.route("<string:member_id>/materia")
class PartyMateria(MethodView):
    @blp.arguments(AssignMateriaSchema)
    @blp.response(201, AssignMateriaSchema)
    def post(self, request_data, member_id):
        """
        Assign multiple materia to 1 party member.
        """
        dumps_json = json.dumps(request_data)
        loaded_json = json.loads(dumps_json)
        print(loaded_json)
        list_of_m = []
        for m in loaded_json["materia_id"]:
            # step 1: check materia exists
            try:
                m_to_fetch = MateriaModel.query.get(m)
                if m_to_fetch == None:
                    abort(404, message=f"'materia_id' not found: {m}")
                print(f">>> id {m} is mapped to {m_to_fetch.__getattribute__('name')}")
                list_of_m.append(m)
            except SQLAlchemyError as e:
                abort(500, message=f"error checking materia")
            # step 2: add both ids into party_materia table
        try:
            list_of_string = str.join(", ", list_of_m)
            add_obj = {"member_id": member_id, "member_materia": list_of_string}
            new_member_materia = PartyMateriaModel(**add_obj)
            db.session.add(new_member_materia)
            db.session.commit()
            return add_obj
        except SQLAlchemyError as e:
            error_msgs = []
            error_msgs.append(e.args)
            error_msgs.append(e._message)
            error_msgs.append(e._sql_message)
            error_msgs.append(e.__cause__)
            abort(500, message=f"Error occurred whilst inserting record: {error_msgs}")
        print(list_of_m)
        print(">>>> finished fetching materia data:")
        # return add_obj


@blp.route("/materia")
class PartyMateria(MethodView):
    @blp.response(200, DeleteSchema)
    def delete(self):
        """
        Delete all assigned materia.
        """
        PartyMateriaModel.query.delete()
        db.session.commit()
        return {"message": f"deleted all assigned materia"}


# TODO:
# continue testing error states
# how to find out member id + materia ids attempted in response body
# create GET /party/materia endpoint
# create GET /party/id/materia endpoint
