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
        This function is called every time a new report is generated. It initiates the process of creating the report
        '''
        self.create_dirs()
        self.create_static()
        self.create_html()
        return 'ok', self.report_name

    def create_report_name(self, file1_name, file2_name):
        '''
        This function combines the names of input files

        :param file1_name: name of the first file
        :type file1_name: str
        :param file2_name: name of the second file
        :type file2_name: str
        :return: combined name, indcluding the time of generation
        :rtype: str
        '''
        return '-'.join([strftime("%Y%m%d-%H%M%S"), file1_name[:-4], file2_name[:-4]])

    def create_dirs(self):
        '''
        creates appropriate directories
        '''
        mkdir(self.template_path)
        mkdir(self.static_path)
        return

    def create_html(self):
        '''
        creates and saves an html file
        '''
        args = (self.report_name, self.filename1, self.filename2)
        formatted_report = report_remplate.format(*args)

        index_path = path.join(getcwd(), workspace_dir_name, self.report_name, 'index.html')
        with open(index_path, "w") as f:
            f.write(formatted_report)
        return

    def create_static(self):
        '''
        This functions loads the data, and, depending on the data type (numeric or non numeric), calls QQ plot or histogram generating function.
        '''
        df_1 = pd.read_csv(self.filename1, usecols=[self.columnname1])
        df_2 = pd.read_csv(self.filename2, usecols=[self.columnname2])

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
        """
            Calls fucnctions that calculate quantiles and plots the resulting data. The results are saved to a file

            :param array1: first data series
            :type array1: np.array(numeric)
            :param array2: second data series
            :type array2: np.array(numeric)

        """

        def create_qq_sub(arr1, arr2):
            '''
            :param array1: first data series (a numpy array)
            :type array1: np.array
            :param array2: second data series (a numpy array)
            :type array2: np.array
            :return: 2 quantile arrays of array1 size
            :rtype: tuple(np.array, np.array)
            '''
            ret1 = quantiles(arr1, arr1.size)
            ret2 = quantiles(arr2, arr1.size)
            return ret1, ret2

        def plot(_q_1, _q_2, filename, filename_vs, plotname):
            '''
            :param _q_1: quantile array 1
            :param _q_2: quantile array 2
            :param filename: name of the file represented on horizontal axis
            :param filename_vs: name of the file represented on vertical axis
            :param plotname: resulting file name
            draws and saves QQ plot
            '''
            fig, ax = plt.subplots()
            ax.scatter(_q_1, _q_2, marker='.', alpha=.3)
            ax.plot([_q_1[0], _q_1[-1]], [_q_2[0], _q_2[-1]], color='C1', alpha=.3, linestyle='dashed')

            ax.set_xlabel(filename)
            ax.set_ylabel(filename_vs)
            ax.set_title('Q-Q plot ' + filename + ' vs ' + filename_vs)
            fig.tight_layout()
            if len(array1) < 11000 and len(array2) < 11000:
                fig.savefig(path.join(self.static_path, plotname + '.svg'))
            fig.savefig(path.join(self.static_path, plotname + '.png'))

        def analyse(_q_1, _q_2, filename, filename_vs, plotname):
            '''
            :param _q_1: first quantile set
            :param _q_2: second quantile set
            :param filename: name of the file represented on horizontal axis
            :param filename_vs: name of the file represented on vertical axis
            :param plotname: resulting file name
            Verifies the similarity betweet data distribution
            '''
            a1 = ((_q_1 - _q_1[0]) / (_q_1[-1] - _q_1[0]))
            a2 = ((_q_2 - _q_2[0]) / (_q_2[-1] - _q_2[0]))
            a3 = (a1 - a2) ** 2
            fig, ax = plt.subplots()
            ax.set_xlabel(filename)
            ax.set_ylabel(filename_vs)
            ax.set_title('Analysis ' + filename + ' vs ' + filename_vs + ' - dissimilarity = ' + str(np.average(a3)))
            ax.plot(a1, a3)
            fig.tight_layout()
            ax.set_yticks(np.arange(0, 1.0, 0.2))
            fig.savefig(path.join(self.static_path, plotname + '.png'))

        q_1, q_2 = create_qq_sub(array1, array2)
        plot(q_1, q_2, self.filename1, self.filename2, 'plot1')
        analyse(q_1, q_2, self.filename1, self.filename2, 'plot3')

        q_1, q_2 = create_qq_sub(array2, array1)
        plot(q_1, q_2, self.filename2, self.filename1, 'plot2')
        analyse(q_1, q_2, self.filename2, self.filename1, 'plot4')

    def create_histogram_plots(self, np_1, np_2):
        '''
        Calls fucnctions that calculate quantiles and plots the resulting data. The results are saved to a file

        :param array1: first data series
        :type array1: np.array(non-numeric)
        :param array2: second data series
        :type array2: np.array(non-numeric)
        '''
        def create_histogram_sub(np_1, np_2):
            d_1 = histogram(np_1)
            d_2 = histogram(np_2)

            return d_1, d_2

        def plot(_q_1, filename, plotname):
            fig, ax = plt.subplots()
            keys = list(map(lambda x: x.strip('\x00'), _q_1.keys()))
            ax.bar(keys, _q_1.values())
            ax.set_title('Histogram - ' + filename)
            fig.tight_layout()
            fig.savefig(path.join(self.static_path, plotname + '.svg'))
            fig.savefig(path.join(self.static_path, plotname + '.png'))

        def analyse(_q_1, _q_2, filename, filename_vs, plotname):
            d = {**_q_1, **_q_2}
            sum = np.sum(list(_q_1.values()))
            for k in _q_1.keys():
                d[k] = _q_1[k] / sum

            sum = np.sum(list(_q_2.values()))
            for k in _q_2.keys():
                d[k] -= _q_2[k] / sum

            for k in d.keys():
                d[k] = d[k] ** 2

            keys = list(map(lambda x: x.strip('\x00'), d.keys()))

            fig, ax = plt.subplots()
            ax.set_xlabel(filename)
            ax.set_ylabel(filename_vs)
            ax.set_title('Analysis ' + filename + ' vs ' + filename_vs + ' - dissimilarity = ' + str(
                np.average(list(d.values()))))
            ax.bar(keys, d.values())
            fig.tight_layout()
            ax.set_yticks(np.arange(0, 1.0, 0.2))
            fig.savefig(path.join(self.static_path, plotname + '.png'))

        def double_bar_chart(_q_1, _q_2, filename, filename_vs, plotname):
            d = {**_q_1, **_q_2}

            dd = {key: np.zeros(2, dtype=float) for key in d.keys()}

            sum = np.sum(list(_q_1.values()))
            for k in _q_1.keys():
                oi = dd[k]
                oi[0] = 1.0 * _q_1[k] / sum

            sum = np.sum(list(_q_2.values()))
            for k in _q_2.keys():
                oi = dd[k]
                oi[1] = 1.0 * _q_2[k] / sum

            ind = np.arange(len(dd.keys()))  # the x locations for the groups
            width = 1.0 / len(dd.keys())

            fig, ax = plt.subplots()

            ax.set_title('Normalised bar chart ' + filename + ' vs ' + filename_vs)

            ax.bar(ind - width / 2, list(map(lambda x: x[0], dd.values())), width)
            ax.bar(ind + width / 2, list(map(lambda x: x[1], dd.values())), width)
            ax.set_xticks(ind)
            ax.set_xticklabels(list(map(lambda x: x.strip('\x00'), d.keys())))
            fig.tight_layout()
            fig.savefig(path.join(self.static_path, plotname + '.png'))

        d_1, d_2 = create_histogram_sub(np_1, np_2)

        plot(d_1, self.filename1, 'plot1')
        plot(d_2, self.filename2, 'plot2')
        analyse(d_1, d_2, self.filename1, self.filename2, 'plot3')
        double_bar_chart(d_1, d_2, self.filename1, self.filename2, 'plot4')
