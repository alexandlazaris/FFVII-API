from db import db


class PartyMateriaModel(db.Model):
    __tablename__ = "party_materia"

    member_id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.String)
