"""The main.py generates a web application that exposes the LinearRegression class of Scikit-Learn as REST APIs.
To run this file, put the cms_autoapi.py under the same directory as the main.py

"""
from test_assets import sample_module
from utilities.cms_autoapi import SignatureScraper
from utilities.cms_autoapi import CodeGenerator

sigs = SignatureScraper().get_ab_signatures(module=sample_module)
print(sigs)
code_gen = CodeGenerator(
    func_signatures=sigs,
    cwd='.',
    function_operation_id_root='analytics',
    file_operation_id_root='file',
    server_url='http://localhost:5000/cloudmesh-analytics',
    template_folder='tests/test_assets/code_templates',
    output_folder='./build'
)

code_gen.generate_ab_module(module_name='sample_module',
                            output_name='sample.py', template_name='ab_module.j2')

code_gen.generate_api_specification(
    output_name='analytics.yaml', template_name='component.j2')

