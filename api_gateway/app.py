from flask import Flask
from flasgger import Swagger
import yaml

app = Flask(__name__)

with open("swagger_docs.yml", "r") as f:
    swagger_template = yaml.safe_load(f)

swagger = Swagger(app, template=swagger_template)

@app.route('/')
def home():
    return 'Go to /apidocs/ to view Swagger UI'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
