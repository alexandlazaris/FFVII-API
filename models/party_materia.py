from db import db

class PartyMateriaModel(db.Model):
    __tablename__ = "party_materia" 

    member_id = db.Column(db.Integer, unique=True, primary_key=True)
    materia_id = db.Column(db.String, unique=True)