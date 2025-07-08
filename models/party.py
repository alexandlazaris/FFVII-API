from db import db
from sqlalchemy import UniqueConstraint

class Party(db.Model):
    __tablename__ = "party"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False) 
    level = db.Column(db.Integer, nullable=False, default=1)
    save_id = db.Column(db.String, nullable=False)
    
    _table_args__ = (
        UniqueConstraint('save_id', 'name', name='uix_saveid_name'),
    ) 