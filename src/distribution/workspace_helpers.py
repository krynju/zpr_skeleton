import os
from os import getcwd
from os import listdir
from os.path import join, isdir

import pandas as pd

workspace_dir_name = 'distribution_ws'


def prepare_workspace():
    if workspace_dir_name not in listdir(getcwd()):
        os.mkdir(workspace_dir_name)


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


def read_csv_columns(filename):
    return list(pd.read_csv(filename, nrows=1).columns)


def scan_for_reports():
    ws_path = join(getcwd(), workspace_dir_name)

    dirs = [f for f in listdir(ws_path) if isdir(join(ws_path, f))]

    reports = list(filter(lambda x: 'index.html' in listdir(join(ws_path, x)), dirs))

    return reports
