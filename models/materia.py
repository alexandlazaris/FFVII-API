from db import db


class MateriaModel(db.Model):
    __tablename__ = "materia"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    element = db.Column(db.String(10), unique=False, nullable=True)
    level = db.Column(db.Integer, unique=False, nullable=False)
    # member_id = db.Column(
    #     db.Integer, db.ForeignKey("party.id"), nullable=True
    # )
    # party = db.relationship("PartyModel", back_populates="materia")
