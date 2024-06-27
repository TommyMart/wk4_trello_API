from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.card import Card, card_schema, cards_schema
from controllers.comment_controller import comments_bp

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
cards_bp.register_blueprint(comments_bp)

# dont need to write /cards now becayse of url_prefix
# /cards - GET - fetch all cards
# /cards/<id> - GET - fetch a single card
# /cards/<id> - DELETE - delete a card
# /cards/<id> - PUT, PATCH - edit a card

# /cards/ - GET deafult - fetch all cards
@cards_bp.route("/")
def get_all_cards():
    # fetch all cards by date ordered by desc order
    stmt = db.select(Card).order_by(Card.date.desc()) # select * from cards
    cards = db.session.scalars(stmt) 
    return cards_schema.dump(cards) # return cards info


# /cards/<id> - GET - fetch a single cards
# /cards/<id> - GET - fetch a single card
@cards_bp.route("/<int:card_id>")
def get_one_card(card_id):
    stmt = db.select(Card).filter_by(id=card_id)
    # stmt = db.select(Card).where(Card.id==card_id)
    card = db.session.scalar(stmt)
    if card: # if card exists

        return card_schema.dump(card)
    else: return {"error": f"Card with id {card_id} not found"}

# /cards - POST - create a new card
# @cards_bp.route("/", methods=["POST"])
# @jwt_required()
# def create_card():
#     # get the data fromt the body of the request
#     body_data = request.get_json()
#     # create a new Card model instance 
#     card = Card(
#         title=body_data.get("title"),
#         description=body_data.get("description"),
#         date=date.today(),
#         status=body_data.get("status"),
#         priority=body_data.get("priority"),
#         # use user id via identity from auth controller
#         user_id=get_jwt_identity()
#     )
#     # add and commit to DB
#     db.session.add(card)
#     db.session.commit()
#     # respond
#     return card_schema.dump(card)

# /cards - POST - create a new card
@cards_bp.route("/", methods=["POST"])
@jwt_required()
def create_card():
    # get the data from the body of the request
    body_data = request.get_json()
    # create a new Card model instance
    card = Card(
        title=body_data.get("title"),
        description=body_data.get("description"),
        date=date.today(),
        status=body_data.get("status"),
        priority=body_data.get("priority"),
        user_id=get_jwt_identity()
    )
    # add and commit to DB
    db.session.add(card)
    db.session.commit()
    # respond
    return card_schema.dump(card)

# /cards/<id> - DELETE - delete a card
# @cards_bp.route("/<card:id>", methods=["DELETE"])
# @jwt_required()
# def delete_card(card_id):
#     # fetch the card from the database
#     stmt = db.select(Card).filter_by(id=card_id)
#     card = db.session.scalar(stmt)
#     if card:
#         # if card
#         # delete the card
#         db.session.delete(card)
#         db.session.commit()
#         return {"message": f"Card {card.title} deleted successfuly"}
#     # else
#     else:
#         # return error
#         return {"message": f"Card with id {card_id} not found"}, 404

# /cards/<id> - DELETE - delete a card
@cards_bp.route("/<int:card_id>", methods=["DELETE"])
@jwt_required()
def delete_card(card_id):
    # fetch the card from the database
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    # if card
    if card:
        # delete the card
        db.session.delete(card)
        db.session.commit()
        return {"message": f"Card '{card.title}' deleted successfully"}
    # else
    else:
        # return error
        return {"error": f"Card with id {card_id} not found"}, 404
    
# /cards/<id> - PUT, PATCH - edit a card
# @cards_bp.route("/<int:card_id>", methods=["PUT, PATCH"])
# @jwt_required
# def update_card(card_id):
#     # get data from the body of the request
#     body_data = request.get_json()
#     # get card from the database
#     stmt = db.select(Card).filter_by(id=card_id)
#     card = db.session.scalar(stmt) # retieve card from db
#     # if card exists
#     if card:
#         # update the fields as required
#         # if user can provided update, if not, title = existing value 
#         card.title = body_data.get("title") or card.title 
#         card.description = body_data.get("description") or card.description
#         card.status = body_data.get("status") or card.status
#         card.priority = body_data.get("priority") or card.priority
#         # commit to db
#         db.session.commit()
#         # return response
#         return card_schema.dump(card)
    
#     # else
#     else:
#         # return an error
#         return {"error": f"Card with id {card_id} not found"}, 404

# /cards/<id> - PUT, PATCH - edit a card
@cards_bp.route("/<int:card_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_card(card_id):
    # get the data from the body of the request
    body_data = request.get_json()
    # get the card from the database
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    # if card exists
    if card:
        # update the fields as required
        card.title = body_data.get("title") or card.title
        card.description = body_data.get("description") or card.description
        card.status = body_data.get("status") or card.status
        card.priority = body_data.get("priority") or card.priority
        # commit to the DB
        db.session.commit()
        # return a response
        return card_schema.dump(card)
    # else
    else:
        # return an error
        return {"error": f"Card with id {card_id} not found"}, 404