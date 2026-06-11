from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'sets.json')


def load_data():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, 'r') as f:
        return json.load(f)


@app.route('/')
def index():
    sets = load_data()
    return render_template('index.html', sets=sets)


@app.route('/api/sets')
def api_sets():
    return jsonify(load_data())


if __name__ == '__main__':
    print('Starting Flask app at http://127.0.0.1:5000/')
    app.run(debug=True)
