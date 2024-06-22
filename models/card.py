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

    # gets data from a seperate table using a foreign key
    # fetch info of user to display # back_populates / links to 'user' model
    # model level 'user' match / get info of user from different table
    user = db.relationship('User', back_populates='cards')

# schema used to fetch data from controller
class CardSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=["id", "name", "email"])
    # foreign key id 
    # {
    #     id: 1,
    #     title: "Card 1",
    #     description: "Card 1 desc",
    #     date: "..",
    #     status: "..",
    #     priority: "..",
    #     user_id: 1,
    #     user: {
    #       id: 1,
    #       name: "User 1",
    #       email: "user1@email.com",
    #   }
    # }

    class Meta:
        fields = ( "id", "title", "description", "date", "status", "priority", "user" )
        
card_schema = CardSchema()
cards_schema  = CardSchema(many=True)

