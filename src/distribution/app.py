"""
.. module:: controller
   :synopsis: All endpoints of the aplication are defined here

"""

import json
from os import getcwd
from os import listdir
from os.path import isfile, join

from flask import Flask, render_template, request, Blueprint, send_from_directory
from flask_cors import CORS

from .report import Report
from .workspace_helpers import prepare_workspace, workspace_dir_name, scan_for_reports, read_csv_columns, File

prepare_workspace()

app = Flask(__name__, template_folder="static", static_url_path='')
CORS(app)

reports = Blueprint(__name__,
                    'reports',
                    root_path=join(getcwd()),
                    template_folder=join(getcwd(), workspace_dir_name))

app.register_blueprint(reports)


@app.route('/')
def root():
    """
    template index.html endpoint for the root path

    :return: rendered template index.html
    """
    return render_template('index.html')


@app.route('/app')
def root_app():
    """
    template index.html endpoint for the /app path

    :return: rendered template index.html
    """
    return render_template('index.html')


@app.route('/api/request', methods=['GET'])
def req():
    """
    endpoint for communication tests

    :return: dict with current working directory
    """
    return json.dumps({
        'response': 'test',
        'current_dir': str(getcwd())
    })


@app.route('/api/cwd', methods=['GET'])
def cwd():
    """
    get the current working directory and its contents

    :return: dict with current working directory and its contents
    """
    return json.dumps({
        'cwd': str(getcwd()),
        'files': [File(f).__dict__ for f in listdir(getcwd()) if isfile(join(getcwd(), f))]
    })


@app.route('/api/csv_info', methods=['GET'])
def csv_info():
    """
    reads the columns off a specific .cvs

    :return: dict with column names
    """
    filename = request.args.get('filename')
    return {'columns': read_csv_columns(filename)}


@app.route('/api/report', methods=['POST'])
def report_request():
    """
    endpoint for generating reports

    :return: dict with end status after the report is complete
    """
    data = request.get_json()['data']
    r = Report(data)
    status, report_name = r.generate()
    return json.dumps({'status': status, 'report_name': report_name})


@app.route('/api/report', methods=['GET'])
def report_list():
    """
    gets all the reports that were previously generated from this directory

    :return: dict with report names
    """
    return json.dumps(scan_for_reports())


@app.route('/report/<report_name>')

def see_report(report_name):
    """
    endpoint for serving template files of reports

    :return: rendered index.html template of a specific report
    """
    return render_template('%s/index.html' % report_name)


@app.route('/report/<report_name>/<file_name>')
def see_report_static(report_name, file_name):
    """
    endpoint for serving static files of reports

    :return: static file of a specific report
    """
    return send_from_directory(join(getcwd(), workspace_dir_name, report_name, report_name), file_name)


if __name__ == '__main__':
    app.run()
