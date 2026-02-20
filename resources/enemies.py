from flask_smorest import Blueprint
from flask.views import MethodView
from schemas import EnemySchema, EnemyDeleted
from services.enemy_service import seed_enemy_boss_data, get_all_enemies, delete_enemy_all_enemies, get_enemy_by_id, update_enemy_by_id

blp = Blueprint(
    "Enemies",
    __name__,
    url_prefix="/enemies",
    description="CRUD information about enemy fights, mostly bosses.",
)

@blp.route("data")
class Enemies(MethodView):
    @blp.response(201, EnemySchema(many=True))
    def post(self):
        """
        Initialise enemy data into db.

        Perform this once. 
        """
        return seed_enemy_boss_data()

@blp.route("")
class Enemies(MethodView):
    @blp.response(200, EnemySchema(many=True))
    def get(self):
        """
        Gets useful in-game details of enemies.
        """
        return get_all_enemies()
    
    @blp.response(200, EnemyDeleted)
    def delete(self):
        """
        Delete all enemy data.
        """
        return delete_enemy_all_enemies()

@blp.route("/<int:id>")
class Enemies(MethodView):
    @blp.response(200, EnemySchema)
    def get(self, id):
        """
        Get enemy information by id.
        """ 
        return get_enemy_by_id(id)
        
    @blp.arguments(EnemySchema)
    @blp.response(200, EnemySchema)
    def put(self, request_data, id):
        """
        Update enemy information by id. Only modified data is updated.
        """
        return update_enemy_by_id(id, request_data)