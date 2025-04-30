from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)

class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)         # Rating author
    movie_id = db.Column(db.Integer, nullable=False)
    reactor_id = db.Column(db.Integer, nullable=False)      # Who agrees/disagrees
    reaction_type = db.Column(db.String(10), nullable=False) # 'agree' or 'disagree'
