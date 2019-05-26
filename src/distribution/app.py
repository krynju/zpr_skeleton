from flask import Flask, render_template, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/request', methods=['GET'])
def request():
    return json.dumps({'response': 'test'})


if __name__ == '__main__':
    app.run()
