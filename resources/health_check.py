from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint(
    "Health check",
    __name__,
    url_prefix="/healthcheck",
    description="Display availability of FF7 API",
)


@blp.route("")
class Enemies(MethodView):
    @blp.response(200)
    def get(self):
        """
        Return 200 if service is running.
        """
        return {"message": "active"}
