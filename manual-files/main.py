"""The main.py generates a web application that exposes the LinearRegression class of Scikit-Learn as REST APIs.
To run this file, put the cms_autoapi.py under the same directory as the main.py

"""
import sklearn.linear_model
from cms_autoapi import SignatureScraper
from cms_autoapi import CodeGenerator

# Type table
type_table = {
    'matrix': 'array',
    'array': 'array',
    'array-like': 'array',
    'numpy array': 'array',
    'bool': 'boolean',
    'int': 'integer',
    'float': 'number'
}

# The module to read
module = sklearn.linear_model
# The classes to read from the module
classes = ['LinearRegression']
# If type table is specified, it will read all classes in the module
sigs = SignatureScraper().get_signatures(
    module=module,
    classes=classes,
    type_table=type_table)

code_gen = CodeGenerator(
        func_signatures=sigs,
        cwd='.',
        function_operation_id_root='analytics',
        file_operation_id_root='file',
        server_url='http://localhost:5000/cloudmesh-analytics',
        template_folder='./code_templates',
        output_folder='./build'
    )
    
code_gen.generate_command_runner(
    output_name='command_runner.py', template_name='command_runner.j2')
code_gen.generate_command_setting(
    output_name='command_setting.json', template_name='command_setting.j2')
code_gen.generate_handlers(
    output_name='analytics.py', template_name='handlers.j2')
code_gen.generate_command_definitions(
    output_name='command_docstring.py', template_name='command_docstring.j2')
code_gen.generate_api_specification(
    output_name='analytics.yaml', template_name='component.j2')
code_gen.generate_file_operations(
    output_name='file.py', template_name='file.j2')
code_gen.generate_server(
    output_name='server.py', template_name='server.j2')