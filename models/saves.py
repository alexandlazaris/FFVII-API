from db import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column
import uuid


class Save(db.Model):
    __tablename__ = "saves"

    id = Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    location = db.Column(db.String(30), unique=False, nullable=False)
    disc = db.Column(db.Integer, nullable=False, default=0)