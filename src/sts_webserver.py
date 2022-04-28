import os
import use_model

from flask import Flask, request
from flask import json as flask_json

# cli = sys.modules['flask.cli'] # workaround - otherwise doesn't work in windows servoce.
# cli.show_server_banner = lambda *x: None 

DATA_CORPUS_PATH = os.path.join("..", "data", "dataset.csv")
EMBEDDINGS_PATH = os.path.join("..", "data", "embeddings.joblib")
sts_use = use_model.STS_USE(DATA_CORPUS_PATH, EMBEDDINGS_PATH)
app = Flask('SemSearch')


@app.route('/find_similar', methods=["POST"])
def estimate_changes():
    content = request.get_json()

    text = content['text']
    top_n = content['top_n']

    pred = sts_use.predict(text, top_n)
    print(pred)
    return flask_json.dumps(pred, ensure_ascii=False)


def start():
    app.run(host='0.0.0.0', threaded=True, port=5050)


if __name__ == '__main__':
    start()
