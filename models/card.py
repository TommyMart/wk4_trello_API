from init import db, ma
from marshmallow import fields

class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.Date) # created date
    status = db.Column(db.String)
    priority = db.Column(db.String)
    # provided by database level, table name
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # model level 'user' match
    user = db.relationship('User', back_populates='cards')

# schema used to fetch data from controller
class CardSchema(ma.Schema):

    # marshmallow level
    user = fields.Nested('UserSchema', only=["id", "name", "email"])

    class Mata:
        # return user object not user_id 'user' schema 
        fields = ( "id", "title", "description", "date", "status", "priority", "user")   

card_schema = CardSchema()
cards_schema  = CardSchema(many=True)

