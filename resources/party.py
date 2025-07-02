from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import Party, PartyMateriaModel, MateriaModel, Save
from schemas import (
    PartyMemberSchema,
    AssignMateriaSchema,
    GetMemberMateriaSchema,
    GetSingleMemberMateriaSchema, SinglePartyMemberSchema
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
    @blp.arguments(SinglePartyMemberSchema(many=True))
    @blp.response(201, SinglePartyMemberSchema(many=True))
    def post(self, body, id):
        """
        Create a party for a save file.

        Add 1-3 members into your party.
        """
        new_party = []
        print (id)
        for p in body:
            member = Party(name=p['name'], save_id=id)
            new_party.append(member)
        print(new_party.__len__())
        new_party_length = new_party.__len__()
        if new_party_length < 1 or new_party_length > 3:
            abort(400, message="Party size invalid. Must between 1-3 members.")
        # TODO: add a check to see if a party already exists for this save
        # new_party.append(save_id)
        print (new_party)
        try:
            db.session.add_all(new_party)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message=str(e.__cause__))
        except SQLAlchemyError():
            abort(500, message="Error occurred whilst inserting record.")
        return new_party
    
    @blp.response(200, SinglePartyMemberSchema(many=True))
    def get(self, id):
        """
        Get party for a save
        """
        try:
            party = Party.query.filter_by(save_id=id)
            if party.first() == None:
                abort(404, message=f"Party with 'save_id' {id} cannot be found.")
            return party.all()
        except IntegrityError as e:
            abort(500, message="Something went wrong.")

    # TODO: add using PUT /party/id to update the party

@blp.route("<string:save_id>")
class PartyApi(MethodView):
    @blp.response(200, PartyMemberSchema)
    def get(self, save_id):
        """
        Get a single party member by id.
        """
        member = Party.query.get_or_404(save_id)
        return member

    @blp.response(200)
    def delete(self, member_id):
        """
        Delete a single party member by id.
        """
        try:
            party_member_to_delete = Party.query.get_or_404(member_id)
            db.session.delete(party_member_to_delete)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message="something went wrong")
        return {"message": "deleted successfully"}


@blp.route("")
class PartyApi(MethodView):
    @blp.response(200)
    def delete(self):
        """
        Delete all party members.
        """

        # TODO: this is a forced delete for both party + party assigned materia
        # this will be replaced onto db models have implemented one-to-many relationships
        count = Party.query.count()
        Party.query.delete()
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
