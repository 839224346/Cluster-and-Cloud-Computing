from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route("/", methods = ['GET'])
def hello_world():
    return jsonify({'Hello ': 'World'})

if __name__ == "__main__":
    app.run(debug=True)