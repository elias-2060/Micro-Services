from flask_restful import Resource, Api, reqparse
from flask import Flask
from flask import request as flask_request
from flask_cors import CORS
from json import dumps, loads
from flasgger import Swagger
import yaml
import pandas as pd

app = Flask("activity")
CORS(app, origins=["http://localhost:3000"])
api = Api(app)

# Load movie data
data = pd.read_csv('Top_10000_Movies_IMDb.csv')
data = data[['ID', 'Movie Name', 'Rating', 'Runtime', 'Genre', 'Metascore', 'Plot']]

# Add Swagger configuration
with open("movie_service_swagger.yml", "r") as f:
    swagger_template = yaml.safe_load(f)
swagger = Swagger(app, template=swagger_template)


def movie_exists(movie_id: int) -> bool:
    """Check if a movie ID exists in the dataset."""
    return movie_id in data['ID'].values


def get_movie_by_id(movie_id: int):
    """Get movie by ID with existence check."""
    if not movie_exists(movie_id):
        return {"error": f"Movie with ID {movie_id} not found"}, 404
    return data[data['ID'] == movie_id].to_json(orient='records')


def get_movies(start, count):
    """Get movies with range parameters validation."""
    start = start if start is not None else 0
    count = count if count is not None else 50

    # Validate parameters
    if start < 0:
        return {"error": "Start parameter cannot be negative"}, 400
    if count <= 0:
        return {"error": "Count parameter must be positive"}, 400

    # Check if start is beyond dataset
    if start >= len(data):
        return {"error": "Start parameter exceeds dataset size"}, 400

    return data.iloc[start:start + count].to_json(orient='records')


class MovieResource(Resource):
    def get(self, id):
        return get_movie_by_id(id)


class MoviesResource(Resource):
    def get(self):
        args = flask_request.args
        try:
            start = int(args['start']) if 'start' in args else None
            count = int(args['count']) if 'count' in args else None
        except ValueError:
            return {"error": "Start and count parameters must be integers"}, 400
        return get_movies(start, count)


api.add_resource(MovieResource, '/movie/<int:id>/')
api.add_resource(MoviesResource, '/movies/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)

