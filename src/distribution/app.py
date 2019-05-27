from flask import Flask, render_template, request
from flask_cors import CORS
import json
from os import getcwd
from os import listdir
from os.path import isfile, join
import pandas as pd

app = Flask(__name__, template_folder="static", static_url_path='')
CORS(app)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/app')
def root_app():
    return render_template('index.html')


@app.route('/api/request', methods=['GET'])
def req():
    return json.dumps({
        'response': 'test',
        'current_dir': str(getcwd())
    })


@app.route('/api/cwd', methods=['GET'])
def cwd():
    return json.dumps({
        'cwd': str(getcwd()),
        'files': [f for f in listdir(getcwd()) if isfile(join(getcwd(), f))]
    })


@app.route('/api/csv_info', methods=['GET'])
def csv_info():
    filename = request.args.get('filename')

    return json.dumps({
        'columns': list(pd.read_csv(filename, nrows=1).columns)
    })


if __name__ == '__main__':
    app.run()
