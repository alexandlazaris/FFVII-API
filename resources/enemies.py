import json
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from schemas import EnemySchema
from models import EnemyModel

blp = Blueprint(
    "Enemies",
    __name__,
    url_prefix="/enemies",
    description="CRUD information about enemy fights, mostly bosses.",
)

@blp.route("data")
class Enemies(MethodView):
    @blp.response(200, EnemySchema(many=True))
    def post(self):
        """
        Initialise enemy data into db.

        Perform this once. 
        """
        enemies = []
        enemies.append(boss_airbuster)
        enemies.append(boss_schizo)
        dumps_json = json.dumps(enemies)
        loaded_json = json.loads(dumps_json)
        for enemy in loaded_json:
            new_enemy = EnemyModel(**enemy)
            try:
                db.session.add(new_enemy)
                db.session.commit()
            except IntegrityError as e:
                abort(400, message="enemies already created")
            except SQLAlchemyError():
                abort(500, message="Error occurred whilst inserting record.")
        return EnemyModel.query.all() 

@blp.route("")
class Enemies(MethodView):
    @blp.response(200, EnemySchema(many=True))
    def get(self):
        """
        Gets useful in-game details of enemies.
        """
        print("get bosses")
        return EnemyModel.query.all()
    
    def delete(self):
        """
        Delete all enemy data.
        """
        count = EnemyModel.query.count()
        EnemyModel.query.delete()
        db.session.commit()
        return {"message": f"deleted {count} enemies"}


@blp.route("/<string:enemy_id>")
class Enemies(MethodView):
    @blp.response(200, EnemySchema)
    def get(self, enemy_id):
        """
        Get enemy information by id.
        """ 
        enemy = EnemyModel.query.get_or_404(enemy_id)
        return enemy

    @blp.arguments(EnemySchema)
    @blp.response(200, EnemySchema)
    # RAGE: my god this was brutal, the route path arg (enemy_id) goes in the 3rd position below, I had it in 2nd position & for >2 hours spent troubleshooting why it wasn't working. fml
    def put(self, request_data, enemy_id):
        """
        Update enemy information by id.

        Only modified data is updated.
        """
        enemy = EnemyModel.query.get_or_404(enemy_id)
        try:
            db.session.query(EnemyModel).filter(EnemyModel.id == enemy_id).update(request_data)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message=str(e.__cause__))
        except SQLAlchemyError():
            abort(500, message="Error occurred whilst updating record.")
        return enemy

boss_schizo = {
    "name": "Schizo",
    "hp": 36000,
    "description": "Multi-headed beast that deals fire, ice, lightning and earth attacks. Both heads deal elemental damage and both unleash a final attack when hp is 0.",
    "steal": "Protect ring",
    "location": "Gaias Cliff",
    "disc": "2",
}

boss_airbuster = {
    "name": "Airbuster",
    "hp": 1200,
    "description": "A robot created by Shinra's Weapon Development Department.",
    "steal": "",
    "location": "Outside No. 5 Reactor",
    "disc": "1",
}
