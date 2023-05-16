from website import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(150))
    destination = db.Column(db.String(150))
    length_route = db.Column(db.String(150))
    travel_time = db.Column(db.String(150))
    avoid = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))