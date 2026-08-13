from db import db
from sqlalchemy import Column
import uuid


class Save(db.Model):
    __tablename__ = "saves"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.UUID, nullable=False, index=True)
    location = db.Column(db.String(30), nullable=False)
    disc = db.Column(db.Integer, nullable=False, server_default=db.text("1"))
