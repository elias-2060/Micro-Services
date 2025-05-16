from flask_restful import Resource, Api
from flask import Flask
from flask import request as flask_request
from flask_cors import CORS
from flasgger import Swagger
import yaml
import pandas as pd

# Initialize Flask application with the name "activity"
app = Flask("activity")

# Enable Cross-Origin Resource Sharing (CORS) for requests from the frontend at localhost:3000
CORS(app, origins=["http://localhost:3000"])

# Create an API object to handle RESTful routing
api = Api(app)

# Load movie dataset and retain specific columns
data = pd.read_csv('Top_10000_Movies_IMDb.csv')
data = data[['ID', 'Movie Name', 'Rating', 'Runtime', 'Genre', 'Metascore', 'Plot']]

# Load and apply Swagger documentation from YAML file
with open("movie_service_swagger.yml", "r") as f:
    swagger_template = yaml.safe_load(f)
swagger = Swagger(app, template=swagger_template)

@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200


def movie_exists(movie_id: int) -> bool:
    """
    Check if a movie ID exists in the dataset.

    Parameters:
        movie_id (int): The movie ID to check.

    Returns:
        bool: True if movie exists, False otherwise.
    """
    return movie_id in data['ID'].values


def get_movie_by_id(movie_id: int):
    """
    Retrieve a movie by its ID.

    Parameters:
        movie_id (int): The movie ID to retrieve.

    Returns:
        JSON response with movie data or an error message.
    """
    if not movie_exists(movie_id):
        return {"error": f"Movie with ID {movie_id} not found"}, 404
    return data[data['ID'] == movie_id].to_json(orient='records')


def get_movies(start, count):
    """
    Retrieve a list of movies with pagination.

    Parameters:
        start (int): Index to start retrieving movies from.
        count (int): Number of movies to retrieve.

    Returns:
        JSON response with a list of movies or error messages.
    """
    start = start if start is not None else 0
    count = count if count is not None else 50

    # Validate input parameters
    if start < 0:
        return {"error": "Start parameter cannot be negative"}, 400
    if count <= 0:
        return {"error": "Count parameter must be positive"}, 400
    if start >= len(data):
        return {"error": "Start parameter exceeds dataset size"}, 400

    return data.iloc[start:start + count].to_json(orient='records')


class MovieResource(Resource):
    """
    Resource for handling a single movie retrieval by ID.
    Endpoint: /movie/<int:id>/
    Method: GET
    """
    def get(self, id):
        return get_movie_by_id(id)


class MoviesResource(Resource):
    """
    Resource for retrieving a paginated list of movies.
    Endpoint: /movies/
    Method: GET
    Query Parameters:
        - start: (optional) Index to start from
        - count: (optional) Number of movies to return
    """
    def get(self):
        args = flask_request.args
        try:
            start = int(args['start']) if 'start' in args else None
            count = int(args['count']) if 'count' in args else None
        except ValueError:
            return {"error": "Start and count parameters must be integers"}, 400
        return get_movies(start, count)


# Register API resources and their routes
api.add_resource(MovieResource, '/movie/<int:id>/')
api.add_resource(MoviesResource, '/movies/')

# Start the Flask application on port 5006
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)
