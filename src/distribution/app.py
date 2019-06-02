import json
from os import getcwd
from os import listdir
from os.path import isfile, join

from flask import Flask, render_template, request, Blueprint, send_from_directory
from flask_cors import CORS

from .report import generate_report
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


@app.route('/api/report', methods=['POST'])
def report_request():
    data = request.get_json()['data']
    status, report_name = generate_report(data)
    return json.dumps({'status': status, 'report_name': report_name})


@app.route('/api/report', methods=['GET'])
def report_list():
    return json.dumps(scan_for_reports())


@app.route('/report/<report_name>')
def see_report(report_name):
    return render_template('%s/index.html' % report_name)


@app.route('/report/<report_name>/<file_name>')
def see_report_static(report_name, file_name):
    return send_from_directory(join(getcwd(), workspace_dir_name, report_name, report_name), file_name)


if __name__ == '__main__':
    app.run()
