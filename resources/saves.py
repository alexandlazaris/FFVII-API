from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.saves import Save
from models.party import Party
from schemas import SavesSchema
import json
from flask import jsonify


blp = Blueprint(
    "Save",
    __name__,
    url_prefix="/saves",
    description="CRUD for save files.",
)


@blp.route("")
class SaveApi(MethodView):
    @blp.arguments(SavesSchema)
    @blp.response(201, SavesSchema)
    def post(self, body):
        """
        Create a save file.
        """
        dumps_json = json.dumps(body)
        loaded_json = json.loads(dumps_json)
        new_save = Save(**loaded_json)
        try:
            db.session.add(new_save)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message=str(e.__cause__))
        except SQLAlchemyError as e:
            abort(500, message="Error occurred whilst inserting record.")
        return {"id": new_save.id, "location": new_save.location}

    # @blp.response(200, SavesSchema(many=True))
    @blp.response(200, SavesSchema(many=True))
    def get(self):
        """
        Get all save files with associated party info
        """
        # results = db.session.query(Save, Party).outerjoin(Party, Save.id == Party.save_id).all()
        saves = Save.query.all()
        response = []
        for s in saves:
            location = s.location
            members = []
            party = Party.query.filter_by(save_id=s.id)
            all = party.all()
            if len(all) >0 :
                print (f"save {s.id} has {len(all)} members")
                for m in all:
                    members.append(m.name)
            if len(all) == 0:
                print (f"save {s.id} has no party")
            print (members)
            save_info = {
                "id": s.id,
                "location": location,
                "party": members
            }
            response.append(save_info)
        return jsonify(response)

    @blp.response(200)
    def delete(self):
        """
        Delete all save files
        """
        count = Save.query.count()
        Save.query.delete()
        db.session.commit()
        return {"message": f"deleted {count} save file/s"}
    
@blp.route("<string:save_id>")
class SaveApi(MethodView):
    @blp.response(200, SavesSchema)
    def get(self, save_id):
        """
        Get a save file by id
        """
        save_file = Save.query.get_or_404(save_id)
        return save_file
    
    @blp.response(200)
    def delete(self, save_id):
        """
        Delete a save file by id
        """
        try:
            save_file = Save.query.get_or_404(save_id)
            db.session.delete(save_file)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message="something went wrong")
        return {"message": f"deleted {save_id}"}