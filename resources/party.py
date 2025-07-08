from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import Party, PartyMateriaModel, MateriaModel
from schemas import (
    AssignMateriaSchema,
    GetMemberMateriaSchema,
    GetSingleMemberMateriaSchema,
    PartyMemberRequestSchema,
    PartyMemberResponseSchema
)
from services.party_service import (
    create_party,
    get_party_using_save,
    update_party_using_save,
)
import json

blp = Blueprint(
    "Party",
    __name__,
    url_prefix="/party",
    description="Endpoints for managing the party",
)


@blp.route("<string:id>")
class PartyApi(MethodView):
    @blp.arguments(PartyMemberRequestSchema(many=True))
    @blp.response(201, PartyMemberResponseSchema(many=True))
    def post(self, body, id):
        """
        Create a party for a save file, adding 1-3 members
        """
        return create_party(body, id)

    @blp.response(200, PartyMemberResponseSchema(many=True))
    def get(self, id):
        """
        Get party for a save
        """
        return get_party_using_save(id)

    @blp.arguments(PartyMemberRequestSchema(many=True))
    @blp.response(200, PartyMemberResponseSchema(many=True))
    def put(self, body, id):
        """
        Update a party for a save
        """
        return update_party_using_save(body, id)


@blp.route("<int:member_id>/materia")
class PartyMateria(MethodView):
    @blp.response(200, GetSingleMemberMateriaSchema)
    def get(self, member_id):
        """
        DO NOT USE - WIP -
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
        DO NOT USE - WIP -
        Assign multiple materia to 1 party member.

        The same cannot be assigned to multiple members.
        """
        dumps_json = json.dumps(request_data)
        loaded_json = json.loads(dumps_json)
        materia_list = []

        # step 1: check if party member exists
        member = Party.query.get(member_id)
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
        DO NOT USE - WIP -
        Delete all assigned materia.
        """
        PartyMateriaModel.query.delete()
        db.session.commit()
        return {"message": f"deleted all assigned materia"}

    @blp.response(200, GetMemberMateriaSchema(many=True))
    def get(self):
        """
        DO NOT USE - WIP -
        Get all party assigned materia
        """
        all_members_with_materia = PartyMateriaModel.query.all()
        response = []
        # for each member who has materia assigned
        for a in all_members_with_materia:
            # step 1: construct member data
            attr_member_id = a.__getattribute__("member_id")
            db_member = Party.query.get(attr_member_id)
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
