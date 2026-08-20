from flask import jsonify
from pydantic import BaseModel
from collections.abc import Sequence


def api_response(
    data: BaseModel | Sequence[BaseModel],
    status: int = 200,
):
    if isinstance(data, BaseModel):
        return jsonify(data.model_dump()), status

    return jsonify([item.model_dump() for item in data]), status
