from db import db

class PartyMateriaModel(db.Model):
    __tablename__ = "party_materia" 

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.String, unique=True)
    member_materia = db.Column(db.String, unique=True)
    
     