from init import db, ma 
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    date = db.Column(db.Date) # created date for comment

    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey("cards.id"), nullable=False)

    # connects models / tables 
    # connects with user comments
    user = db.relationship("User", back_populates="comments")
    card = db.relationship("Card", back_populates="comments")

class CommentSchema(ma.Schema):
    # nested
    user = fields.Nested("UserSchema", only=["name", "email"])
    cards = fields.Nested("CardsSchema", exclude=["comments"])

    class Meta:
        fields = ("id", "message", "date", "user", "card")


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)