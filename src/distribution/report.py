from os import path, getcwd, mkdir
from time import strftime
from .workspace_helpers import workspace_dir_name
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import math
from .distribution import quantiles
import time


report_remplate = '''
<!DOCTYPE html>
<html lang="en">
<head>

    <meta charset="UTF-8">
    <title>{0}</title>
    <base href="./">
</head>
<body>
    <p>raport : {0} </p>
    <img src="{0}/plot1.png">
    <img src="{0}/plot2.png">
</body>
</html>
'''


def generate_report(data):
    report_name = create_report_name(data[0]['filename'], data[1]['filename'])
    create_dirs(report_name)
    create_static(report_name, data)
    create_html(report_name)
    return 'ok', report_name


def create_report_name(file1_name, file2_name):
    return '-'.join([strftime("%Y%m%d-%H%M%S"), file1_name[:-4], file2_name[:-4]])


def create_dirs(report_name):
    template_path = path.join(getcwd(), workspace_dir_name, report_name)
    static_path = path.join(getcwd(), workspace_dir_name, report_name, report_name)
    mkdir(template_path)
    mkdir(static_path)
    return


def create_html(report_name):
    args = (report_name,)
    formatted_report = report_remplate.format(*args)

    index_path = path.join(getcwd(), workspace_dir_name, report_name, 'index.html')
    with open(index_path, "w") as f:
        f.write(formatted_report)
    return


def create_static(report_name, data):
    static_path = path.join(getcwd(), workspace_dir_name, report_name, report_name)

    df_1 = pd.read_csv(data[0]['filename'], usecols=[data[0]['column']])
    df_2 = pd.read_csv(data[1]['filename'], usecols=[data[1]['column']])

    np_1 = df_1[data[0]['column']].values

    np_2 = df_2[data[1]['column']].values

    if data[0]['type'] == 'continuous' and data[1]['type'] == 'continuous':
        create_qq_plots(np_1, np_2, static_path)
    else:
        create_histogram_plots(np_1, np_2, static_path)

    return


def create_qq_sub(array1, array2):
    # def quantiles(array, count):
    #     q = np.ndarray(count)
    #     for i in np.arange(count):
    #         p = i / count
    #         h = (array.size - 1) * p + 1 / 2
    #         q[i] = (array[math.ceil(h - 1 / 2)] + array[math.floor(h + 1 / 2)]) / 2
    #     return q

    # def quantiles_python(array, count):
    #     array.sort()
    #     q = np.ndarray(count)
    #     N = array.size - 1
    #     for i in np.arange(count):
    #         p = i / count
    #         h = (N - 1) * p + 1
    #         q[i] = array[math.floor(h)] + (h - math.floor(h)) * (array[math.floor(h) + 1] - array[math.floor(h)])
    #     return q
    #
    # np.random.shuffle(array1)
    # np.random.shuffle(array2)
    #
    # start = time.perf_counter_ns()
    # q_1 = quantiles(array1, array1.size)
    # end = time.perf_counter_ns()
    # print(end - start)
    #
    # np.random.shuffle(array1)
    # np.random.shuffle(array2)
    # start = time.perf_counter_ns()
    # q_2 = quantiles(array2, array1.size)
    # end = time.perf_counter_ns()
    # print(end - start)
    # np.random.shuffle(array1)
    # np.random.shuffle(array2)
    # start = time.perf_counter_ns()
    # q_1 = quantiles_python(array1, array1.size)
    # end = time.perf_counter_ns()
    # print(end - start)
    # np.random.shuffle(array1)
    # np.random.shuffle(array2)
    # start = time.perf_counter_ns()
    # q_2 = quantiles_python(array2, array1.size)
    # end = time.perf_counter_ns()
    # print(end - start)

    q_1 = quantiles(array1, array1.size)
    q_2 = quantiles(array2, array1.size)

    return q_1, q_2


def create_qq_plots(array1, array2, static_path):


    q_1, q_2 = create_qq_sub(array1, array2)
    fig, ax = plt.subplots()
    ax.scatter(q_1, q_2)
    if len(array1) < 11000 and len(array2) < 11000:
        fig.savefig(path.join(static_path, 'plot1.svg'))
    fig.savefig(path.join(static_path, 'plot1.png'))

    q_1, q_2 = create_qq_sub(array2, array1)
    fig, ax = plt.subplots()
    ax.scatter(q_1, q_2)
    if len(array1) < 11000 and len(array2) < 11000:
        fig.savefig(path.join(static_path, 'plot2.svg'))
    fig.savefig(path.join(static_path, 'plot2.png'))


def create_histogram_plots(np_1, np_2, static_path):
    fig, ax = plt.subplots()
    ax.hist(np_1, bins=100)
    fig.savefig(path.join(static_path, 'plot1.svg'))
    fig.savefig(path.join(static_path, 'plot1.png'))

    fig, ax = plt.subplots()
    ax.hist(np_2, bins=100)
    fig.savefig(path.join(static_path, 'plot2.svg'))
    fig.savefig(path.join(static_path, 'plot2.png'))
