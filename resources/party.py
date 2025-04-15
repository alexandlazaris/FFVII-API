from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import PartyModel, PartyMateriaModel, MateriaModel
from schemas import (
    PartyMemberSchema,
    AssignMateriaSchema,
    GetMemberMateriaSchema,
    GetSingleMemberMateriaSchema,
)

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
        response = []
        for p in request:
            member = PartyModel(**p)
            response.append(member)
        new_party_length = response.__len__()
        if new_party_length < 1 or new_party_length > 3:
            abort(400, message="Party size invalid. Must between 1-3 members.")
        try:
            db.session.add_all(response)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message=str(e.__cause__))
        except SQLAlchemyError():
            abort(500, message="Error occurred whilst inserting record.")
        return response


@blp.route("<int:member_id>")
class Party(MethodView):
    @blp.response(200, PartyMemberSchema)
    def get(self, member_id):
        """
        Get a single party member by id.
        """
        member = PartyModel.query.get_or_404(member_id)
        return member

    @blp.response(200)
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
    @blp.response(200)
    def delete(self):
        """
        Delete all party members.
        """

        # TODO: this is a forced delete for both party + party assigned materia
        # this will be replaced onto db models have implemented one-to-many relationships
        count = PartyModel.query.count()
        PartyModel.query.delete()
        db.session.commit()

        # don
        PartyMateriaModel.query.delete()
        db.session.commit()

        return {"message": f"deleted {count} party member/s"}


@blp.route("<int:member_id>/materia")
class PartyMateria(MethodView):
    @blp.response(200, GetSingleMemberMateriaSchema)
    def get(self, member_id):
        """
        Get a single party member and their materia
        """
        member = PartyMateriaModel.query.get(member_id)
        if member == None:
            abort(404, message=f"'member' not found: {member_id}")
        materia_list = []
        materia = str(member.__getattribute__("materia_id")).split(",")
        for m in materia:
            materia_object = MateriaModel.query.get(m).__dict__
            if materia_object == None:
                abort(404, message=f"'materia_id' not found: {m}")
            materia_list.append(materia_object)
        response = {"member_id": member_id, "materia": materia_list}
        return response

    @blp.arguments(AssignMateriaSchema)
    @blp.response(201)
    def post(self, request_data, member_id):
        """
        Assign multiple materia to 1 party member.

        The same cannot be assigned to multiple members.
        """
        dumps_json = json.dumps(request_data)
        loaded_json = json.loads(dumps_json)
        materia_list = []

        # step 1: check if party member exists
        member = PartyModel.query.get(member_id)
        if member == None:
            abort(404, message=f"'member_id' not found: {member_id}")
        for m in loaded_json["materia_id"]:
            # step 2: check if materia is already assigned to a member
            all_materia_assigned_members = PartyMateriaModel.query.all()
            for members in all_materia_assigned_members:
                # iterate through all members with materia, checking if the incoming materia is already assigned
                iter_m = str(members.__getattribute__("materia_id"))
                iter_id = str(members.__getattribute__("member_id"))
                if iter_m.__eq__(m):
                    abort(
                        500,
                        messages=f"materia_id '{m}' is already assigned to member '{iter_id}'. Please use another materia.",
                    )
            # step 3: check if materia id exists in db
            try:
                materia_object = MateriaModel.query.get(m)
                if materia_object == None:
                    abort(404, message=f"'materia_id' not found: {m}")
                materia_list.append(m)
            except SQLAlchemyError as e:
                abort(500, message=f"error checking materia")
            # step 4: add both ids into party_materia table
        try:
            list_of_string = str.join(", ", materia_list)
            # TODO: add the full materia data here, not just the string ids.
            add_obj = {"member_id": member_id, "materia_id": list_of_string}
            new_member_materia = PartyMateriaModel(**add_obj)
            db.session.add(new_member_materia)
            db.session.commit()
            return add_obj
        except SQLAlchemyError as e:
            abort(
                500,
                message=f"cannot create another record for member {member_id}. Use PUT instead.",
            )


@blp.route("/materia")
class PartyMateria(MethodView):
    @blp.response(200)
    def delete(self):
        """
        Delete all assigned materia.
        """
        PartyMateriaModel.query.delete()
        db.session.commit()
        return {"message": f"deleted all assigned materia"}

    @blp.response(200, GetMemberMateriaSchema(many=True))
    def get(self):
        """
        Get all party assigned materia
        """
        all_members_with_materia = PartyMateriaModel.query.all()
        response = []
        # for each member who has materia assigned
        for a in all_members_with_materia:
            # step 1: construct member data
            attr_member_id = a.__getattribute__("member_id")
            db_member = PartyModel.query.get(attr_member_id)
            attr_member_name = db_member.__getattribute__("name")
            response_member = {"id": attr_member_id, "name": attr_member_name}
            # step 2: construct materia data
            materia_list = []
            attr_materia_id = str(a.__getattribute__("materia_id")).split(",")
            for materia_index in attr_materia_id:
                materia_object = MateriaModel.query.get(materia_index).__dict__
                if materia_object == None:
                    abort(404, message=f"'materia_id' not found: {materia_index}")
                materia_list.append(materia_object)
            # step 3: construct response body
            combined_response = {"member": response_member, "materia": materia_list}
            response.append(combined_response)
        return response
