from init import db, ma
from marshmallow import fields

# so users can be made in db
class User(db.Model):
    # name of table
    __tablename__ = "users"

    # attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # connects to user field
    cards = db.relationship('Card', back_populates='user')

class UserSchema(ma.Schema):
    # marshmallow to de/serialize 
    cards = fields.List(fields.Nested('CardSchema', exclude=["user"]))

    class Meta:
        # convert database objects to python and vice versa
        fields = ("id", "name", "email", "password", "is_admin", "cards")

# handle singe user object
user_schema = UserSchema(exclude=["password"])

# handle a list of users objects
users_schema = UserSchema(many=True, exclude=["password"])