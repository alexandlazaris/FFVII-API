from db import db

class PartyMember(db.Model):
    __tablename__ = "party_member"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    level = db.Column(db.Integer, nullable=False, default=1)
    party_id = db.Column(
        db.String,
        db.ForeignKey(
            "party.id",
            ondelete="CASCADE",
            name="fk_party_member_party_id",
        ),
        nullable=False,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "party_id",
            "name",
            name="uq_party_member_party_name",
        ),
    )

