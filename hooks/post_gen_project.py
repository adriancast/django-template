import os
import shutil


def remove(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)


add_prometheus_and_grafana = '{{cookiecutter.add_prometheus_and_grafana}}' == 'yes'


if not add_prometheus_and_grafana:
    remove(os.path.join(os.getcwd(), 'prometheus'))
