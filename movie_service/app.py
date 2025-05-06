from flask_restful import Resource, Api, reqparse
from flask import Flask
from flask import request as flask_request
from json import dumps, loads
from flasgger import Swagger
import yaml

import pandas as pd

data = pd.read_csv('Top_10000_Movies_IMDb.csv')
data = data[['ID', 'Movie Name', 'Rating', 'Runtime', 'Genre', 'Metascore', 'Plot']]

app = Flask("activity")
api = Api(app)

# Add Swagger configuration
with open("movie_service_swagger.yml", "r") as f:
    swagger_template = yaml.safe_load(f)
swagger = Swagger(app, template=swagger_template)

def get_movie_by_id(id:int):
    return data[data['ID'] == id].to_json(orient='records')  # Assumes that ID is unique


def get_movies(start, count):  # !!! This is not by ID, but by position in the list (ID is 1-indexed, position is 0-indexed)

    start = start if start is not None else 0
    count = count if count is not None else 50

    return data.iloc[start:start+count].to_json(orient='records')

class MovieResource(Resource):
    def get(self, id):
        return get_movie_by_id(id)

class MoviesResource(Resource):
    def get(self):
        args = flask_request.args
        start = int(args['start']) if 'start' in args else None
        count = int(args['count']) if 'count' in args else None
        return get_movies(start, count)

api.add_resource(MovieResource, '/movie/<int:id>/')
api.add_resource(MoviesResource, '/movies/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)