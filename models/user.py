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
    cards = db.relationship("Card", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")

class UserSchema(ma.Schema):
    # numerous cards to single user, list of cards / serialize / deserialize 
    # marshmallow to de/serialize 
    cards = fields.List(fields.Nested('CardSchema', exclude=["user"]))
    comments = fields.List(fields.Nested('CommentSchema', exclude=["user"]))
    class Meta:
        # convert database objects to python and vice versa
        fields = ("id", "name", "email", "password", "is_admin", "cards", "comments")

# handle singe user object
user_schema = UserSchema(exclude=["password"])

# handle a list of users objects
users_schema = UserSchema(many=True, exclude=["password"])