# internal
from datetime import date
# extental
from flask import Blueprint
# imports from files
from init import db, bcrypt
from models.card import Card
from models.user import User
from models.comment import Comment

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")
    
@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_tables():
    # create a list of User instances
    users = [
        User(
            email="admin@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
            is_admin=True
        ),
        User(
            name="User 1",
            email="user1@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
        )
    ]

    db.session.add_all(users)

    # db.session.commit() / 

    cards = [
        Card(
            title="Card 1",
            description="Card 1 desc",
            date=date.today(),
            status="To do",
            priority="High",
            user=users[0]
        ),
        Card(
            title="Card 2",
            description="Card 2 desc",
            date=date.today(),
            status="Ongoing",
            priority="Low",
            user=users[0]
        ),
        Card(
            title="Card 3",
            description="Card 3 desc",
            date=date.today(),
            status="Done",
            priority="Medium",
            user=users[1]
            # user_id=users[0].id
        ),
    ]
    
    db.session.add_all(cards)
    db.session.commit()

    print("Tables seeded")
