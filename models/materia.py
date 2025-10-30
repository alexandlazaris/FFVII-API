from db import db


class MateriaModel(db.Model):
    __tablename__ = "materia"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)
    element = db.Column(db.String(15), unique=False, nullable=True)
    type = db.Column(db.String(15), unique=False, nullable=False)
