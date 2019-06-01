from os import path, getcwd, mkdir
from time import strftime
from .workspace_helpers import workspace_dir_name
from matplotlib import pyplot as plt

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
    <img src="{0}/plot1.svg">

</body>
</html>
'''


def generate_report(data):
    report_name = create_report_name(data[0]['filename'], data[1]['filename'])
    create_dirs(report_name)
    create_static(report_name)
    create_html(report_name)
    return


def create_report_name(file1_name, file2_name):
    return '-'.join([file1_name, file2_name, strftime("%Y%m%d-%H%M%S")])


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


def create_static(report_name):
    static_path = path.join(getcwd(), workspace_dir_name, report_name, report_name)

    plt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])

    plt.savefig(path.join(static_path, 'plot1.svg'))
    return
