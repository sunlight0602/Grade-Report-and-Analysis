import os

import pkg_resources
from jinja2 import Template


class CWTReport:
    output_path = os.path.join(os.getcwd(), 'output_files')

    def open_template(self, file_name):
        path = os.path.join('templates', file_name)
        template_path = pkg_resources.resource_filename('GradeReportAndAnalysis', path)
        with open(template_path, 'r', encoding='utf-8') as file:
            template = file.read()
        return Template(template)
