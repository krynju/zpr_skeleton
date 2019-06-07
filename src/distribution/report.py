'''
.. module:: report
   :synopsis: This module contains functions used to generate report from raw data
'''

from os import path, getcwd, mkdir
from time import strftime
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from .distribution import quantiles, histogram
from .workspace_helpers import workspace_dir_name
from functools import reduce

report_remplate = '''
    <!DOCTYPE html>
    <html>
    
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{0}</title>
      <link rel="stylesheet" href="https://stackedit.io/style.css" />
      <base href="./">
    </head>
    
    <body class="stackedit">
      <div class="stackedit__html"><h1 id="raport-0">Raport {0}</h1>
    <h2 id="file-1">File: {1}</h2>
    <p><img src="{0}/plot1.png" alt=""></p>
    <h2 id="file-3">File: {2}</h2>
    <p><img src="{0}/plot2.png" alt=""></p>
    <h2 id="comparison">Comparison</h2>
    <p><img src="{0}/plot3.png" alt=""></p>
    <p><img src="{0}/plot4.png" alt=""></p>
    </div>
    </body>
    
    </html>
    
    '''


class Report:
    '''
    This class represents the processed report
    '''
    def __init__(self, data):
        self.filename1 = data[0]['filename']
        self.filename2 = data[1]['filename']

        self.columnname1 = data[0]['column']
        self.columnname2 = data[1]['column']

        self.report_name = self.create_report_name(self.filename1, self.filename2)
        self.template_path = path.join(getcwd(), workspace_dir_name, self.report_name)
        self.static_path = path.join(getcwd(), workspace_dir_name, self.report_name, self.report_name)
        self.data = data

    def generate(self):
        '''

        :param data:
        :return:
        '''
        self.create_dirs()
        self.create_static()
        self.create_html()
        return 'ok', self.report_name

    def create_report_name(self, file1_name, file2_name):
        '''
        :param file1_name: name of the first file
        :param file2_name: name of the second file
        :return: combined name, indcluding the time of generation
        '''
        return '-'.join([strftime("%Y%m%d-%H%M%S"), file1_name[:-4], file2_name[:-4]])

    def create_dirs(self):
        mkdir(self.template_path)
        mkdir(self.static_path)
        return

    def create_html(self):
        args = (self.report_name, self.filename1, self.filename2)
        formatted_report = report_remplate.format(*args)

        index_path = path.join(getcwd(), workspace_dir_name, self.report_name, 'index.html')
        with open(index_path, "w") as f:
            f.write(formatted_report)
        return

    def create_static(self):

        df_1 = pd.read_csv(self.filename1, usecols=[self.columnname1])
        df_2 = pd.read_csv(self.filename1, usecols=[self.columnname2])

        np_1 = df_1[self.data[0]['column']].values

        np_2 = df_2[self.data[1]['column']].values

        if self.data[0]['type'] == 'continuous' and self.data[1]['type'] == 'continuous':
            self.create_qq_plots(np_1, np_2)
        elif self.data[0]['type'] == 'discrete' and self.data[1]['type'] == 'discrete':
            np_1 = np_1.astype('U')
            np_2 = np_2.astype('U')
            self.create_histogram_plots(np_1, np_2)
        return

    def create_qq_plots(self, array1, array2):
        '''
        Calls fucnctions that calculate quantiles and plots the resulting data
        :param array1:
        :param array2:
        :param static_path:
        :return:
        '''

        def create_qq_sub(arr1, arr2):
            ret1 = quantiles(arr1, arr1.size)
            ret2 = quantiles(arr2, arr1.size)
            return ret1, ret2

        def plot(_q_1, _q_2, filename, filename_vs, plotname):
            fig, ax = plt.subplots()
            ax.scatter(_q_1, _q_2, marker='.', alpha=.3)
            ax.plot([_q_1[0], _q_1[-1]], [_q_2[0], _q_2[-1]], color='C1', alpha=.3, linestyle='dashed')

            ax.set_xlabel(filename)
            ax.set_ylabel(filename_vs)
            ax.set_title('Q-Q plot ' + filename + ' vs ' + filename_vs)

            if len(array1) < 11000 and len(array2) < 11000:
                fig.savefig(path.join(self.static_path, plotname + '.svg'))
            fig.savefig(path.join(self.static_path, plotname + '.png'))

        def analyse(_q_1, _q_2, filename, filename_vs, plotname):
            a1 = ((_q_1 - _q_1[0]) / (_q_1[-1] - _q_1[0]))
            a2 = ((_q_2 - _q_2[0]) / (_q_2[-1] - _q_2[0]))
            a3 = (a1 - a2) ** 2
            fig, ax = plt.subplots()
            ax.set_xlabel(filename)
            ax.set_ylabel(filename_vs)
            ax.set_title('Analysis ' + filename + ' vs ' + filename_vs + ' - dissimilarity = ' + str(np.average(a3)))
            ax.plot(a1, a3)
            ax.set_yticks(np.arange(0, 1.0, 0.2))
            fig.savefig(path.join(self.static_path, plotname + '.png'))

        q_1, q_2 = create_qq_sub(array1, array2)
        plot(q_1, q_2, self.filename1, self.filename2, 'plot1')
        analyse(q_1, q_2, self.filename1, self.filename2, 'plot3')

        q_1, q_2 = create_qq_sub(array2, array1)
        plot(q_1, q_2, self.filename2, self.filename1, 'plot2')
        analyse(q_1, q_2, self.filename2, self.filename1, 'plot4')

    def create_histogram_plots(self, np_1, np_2, ):
        def create_histogram_sub(np_1, np_2):
            d_1 = histogram(np_1)
            d_2 = histogram(np_2)

            return d_1, d_2

        def plot(_q_1, filename, plotname):
            fig, ax = plt.subplots()
            keys = list(map(lambda x: x.strip('\x00'), d_1.keys()))
            ax.bar(keys, d_1.values())
            ax.set_title('Histogram - ' + filename)
            fig.savefig(path.join(self.static_path, plotname + '.svg'))
            fig.savefig(path.join(self.static_path, plotname + '.png'))

        def analyse(_q_1, _q_2, filename, filename_vs, plotname):
            a = [*_q_1.keys(), *_q_2.keys()]
            d = dict(keys=a, values=np.zeros(len(np.unique(a)), dtype=int))

            # sum = np.sum(_q_1.values())
            # for k in _q_1.keys():
            #     d[k] += _q_1[k] / sum
            #
            # sum = np.sum(_q_2.values())
            # for k in _q_2.keys():
            #     d[k] -= _q_2[k] / sum

            # fig, ax = plt.subplots()
            # ax.set_xlabel(filename)
            # ax.set_ylabel(filename_vs)
            # ax.set_title('Analysis ' + filename + ' vs ' + filename_vs + ' - dissimilarity = ' + str(np.average(a3)))
            # ax.plot(a1, a3)
            # ax.set_yticks(np.arange(0, 1.0, 0.2))
            # fig.savefig(path.join(self.static_path, plotname + '.png'))

        d_1, d_2 = create_histogram_sub(np_1, np_2)

        plot(d_1, self.filename1, 'plot1')
        plot(d_2, self.filename2, 'plot2')
        analyse(d_1, d_2, self.filename1, self.filename2, 'plot3')
