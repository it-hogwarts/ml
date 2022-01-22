import json
from flask import Flask, request

from recommend_courses import Recommender


app = Flask(__name__)

recommendation_model = Recommender(source_path='./source_files/')


@app.route("/", methods=["POST"])
def index():
    data = request.json
    return json.dumps({'tags': recommendation_model.predict(
        data['tags'],
        topk=5
    )})


app.run(port=8000, host="0.0.0.0")
