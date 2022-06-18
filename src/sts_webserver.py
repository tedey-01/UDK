import os
import use_model
import logging

from flask import Flask, request
from flask import json as flask_json


logging.basicConfig(filename='service.log', level=logging.DEBUG)
app = Flask('SemSearch')

DATA_CORPUS_PATH = os.path.join("..", "data", "dataset.csv")
EMBEDDINGS_PATH = os.path.join("..", "data", "embeddings.joblib")
sts_use = use_model.STS_USE(DATA_CORPUS_PATH, EMBEDDINGS_PATH)


@app.route('/find_similar', methods=["POST"])
def estimate_changes():
    content = request.get_json()
    app.logger.error(f"INPUT: {content}")

    text = content['text']
    top_n = content['top_n']

    predict = sts_use.predict(text, top_n)
    app.logger.info(f"PREDICT: {predict}")
    return flask_json.dumps(predict, ensure_ascii=False)


def start():
    app.run(host='0.0.0.0', threaded=True, port=5050)


if __name__ == '__main__':
    start()
