from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError
from schemas import EnemyCreate, EnemyUpdate, EnemySchema, EnemyDeleted
from models import EnemyModel
from db import db
from game_data.enemies.bosses import enemies

blp = Blueprint(
    "Enemies",
    __name__,
    url_prefix="/enemies",
    description="CRUD information about enemy fights, mostly bosses.",
)

@blp.route("data")
class Enemies(MethodView):
    # find out how pydantic returns a list type containing a single schema
    @blp.response(201, EnemySchema(many=True))
    def post(self):
        """
        Initialise enemy data into db.

        Perform this once. 
        """
        try:
            for enemy_dict in enemies:
                validated_enemy = EnemyCreate(**enemy_dict)
                new_enemy = EnemyModel(**validated_enemy.model_dump())
                db.session.add(new_enemy)
            db.session.commit()
        except ValidationError as e:
            abort(400, message=f"Validation error: {e.errors()}")
        except IntegrityError:
            db.session.rollback()
            abort(400, message="enemies already created")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Error occurred whilst inserting record.")        
        return EnemyModel.query.all() 


@blp.route("")
class Enemies(MethodView):
    @blp.response(200, EnemySchema(many=True))
    def get(self):
        """
        Gets useful in-game details of enemies.
        """
        return EnemyModel.query.all()
    
    @blp.response(200, EnemyDeleted)
    def delete(self):
        """
        Delete all enemy data.
        """
        count = EnemyModel.query.count()
        EnemyModel.query.delete()
        db.session.commit()
        return { "message": f"deleted {count} enemies"}


@blp.route("/<int:id>")
class Enemies(MethodView):
    @blp.response(200, EnemySchema)
    def get(self, id):
        """
        Get enemy information by id.
        """ 
        return EnemyModel.query.get_or_404(id)
        
    # RAGE: my god this was brutal, the route path arg (id) goes in the 3rd position below, I had it in 2nd position & for >2 hours spent troubleshooting why it wasn't working. fml
    @blp.arguments(EnemySchema)
    @blp.response(200, EnemySchema)
    def put(self, request_data, id):
        """Update enemy information by id. Only modified data is updated."""
        enemy = db.session.get(EnemyModel, id)
        if enemy is None:
            abort(404)
        try:
            # Validate incoming data with Pydantic
            validated_data = EnemyUpdate(**request_data)
            
            # Update only provided fields
            update_dict = validated_data.model_dump(exclude_unset=True)
            
            # Update the ORM object
            for key, value in update_dict.items():
                setattr(enemy, key, value)
            db.session.commit()
        except ValidationError as e:
            abort(400, message=f"Validation error: {e.errors()}")
        except IntegrityError as e:
            db.session.rollback()
            abort(400, message=str(e.__cause__))
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Error occurred whilst updating record.")
        return enemy