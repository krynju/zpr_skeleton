from flask import Flask, render_template, request
from flask_cors import CORS
import json
from os import getcwd
from os import listdir
from os.path import isfile, join
import pandas as pd

app = Flask(__name__, template_folder="static", static_url_path='')
CORS(app)


class File:
    def __init__(self, filename):
        self.filename = filename

        if filename[-4:] == '.csv':
            self.status = 'csv'
        else:
            self.status = 'wrong_format'

        if self.status == 'csv':
            try:
                self.columns = read_csv_columns(filename)
            except:
                self.status = 'error_reading_columns'
                self.columns = []

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
        'files': [File(f).__dict__ for f in listdir(getcwd()) if isfile(join(getcwd(), f))]
    })


@app.route('/api/csv_info', methods=['GET'])
def csv_info():
    filename = request.args.get('filename')
    return {'columns': read_csv_columns(filename)}


def read_csv_columns(filename):
    return list(pd.read_csv(filename, nrows=1).columns)












if __name__ == '__main__':
    app.run()
