from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError
from schemas import EnemyCreate, EnemyUpdate
from models import EnemyModel
from db import db
from game_data.enemies.bosses import enemies

def seed_enemy_boss_data():
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

def get_all_enemies():
    """
    Gets useful in-game details of enemies.
    """
    return EnemyModel.query.all()

def delete_enemy_all_enemies():
    """
        Delete all enemy data.
        """
    count = EnemyModel.query.count()
    EnemyModel.query.delete()
    db.session.commit()
    return { "message": f"deleted {count} enemies"}
    
def get_enemy_by_id(id: int):
    """
    Get enemy information by id.
    """ 
    return EnemyModel.query.get_or_404(id)


def update_enemy_by_id(id: int, request_data: object):
    """
    Update enemy information by id. Only modified data is updated.
    """
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