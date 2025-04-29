from flask import Flask, request, jsonify
from models import db, WatchHistory
from database import init_db
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watchhistory.db'
init_db(app)

@app.route('/watch/<int:user_id>/<int:movie_id>/', methods=['POST'])
def add_watch(user_id, movie_id):
    watch = WatchHistory(user_id=user_id, movie_id=movie_id, timestamp=datetime.utcnow())
    db.session.add(watch)
    db.session.commit()
    return {"message": f"Movie {movie_id} added to user {user_id}'s history"}, 201

@app.route('/watch/<int:user_id>/', methods=['GET'])
def get_watch_history(user_id):
    history = WatchHistory.query.filter_by(user_id=user_id).all()
    output = [
        {"movie_id": h.movie_id, "timestamp": h.timestamp.isoformat()}
        for h in history
    ]
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
