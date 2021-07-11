import os
import shutil


def remove(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)


add_prometheus_and_grafana = '{{cookiecutter.add_prometheus_and_grafana}}' == 'yes'
add_sentry = '{{cookiecutter.add_sentry}}' == 'yes'
production_domain_url = '{{cookiecutter.production_domain_url}}'
project_path = os.getcwd()

icon_check = '✅'
icon_cross = '❌'
icon_warning = '⚠️'
summary_text = """

   ███████╗██╗   ██╗███╗   ███╗███╗   ███╗ █████╗ ██████╗ ██╗   ██╗
   ██╔════╝██║   ██║████╗ ████║████╗ ████║██╔══██╗██╔══██╗╚██╗ ██╔╝
   ███████╗██║   ██║██╔████╔██║██╔████╔██║███████║██████╔╝ ╚████╔╝ 
   ╚════██║██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██╔══██╗  ╚██╔╝  
   ███████║╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝                                                              

"""
if not add_prometheus_and_grafana:
    remove(os.path.join(project_path, 'prometheus'))

print(summary_text)
print('{icon} Project generated in: {project_path}'.format(
    project_path=project_path,
    icon=icon_check)
)
print('{icon} Grafana and Prometheus added to the project'.format(
    project_path=project_path,
    icon=(icon_check if add_prometheus_and_grafana else icon_cross))
)
print('{icon} Sentry and Prometheus added to the project'.format(
    project_path=project_path,
    icon=(icon_check if add_sentry else icon_cross))
)
print('{icon} HTTPS certificates will be generated for the following domains:'.format(icon=icon_check))
print('   - {production_domain_url} '.format(
    production_domain_url=production_domain_url)
)
print('   - www.{production_domain_url}'.format(
    production_domain_url=production_domain_url)
)
if add_sentry:
    print('{icon}  Sentry - manual configuration required:'
          ' Update "dsn" Sentry configuration in the bottom of the Django settings.py file'.format(icon=icon_warning))
