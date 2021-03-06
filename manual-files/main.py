"""The main.py generates a web application that exposes the LinearRegression class of Scikit-Learn as REST APIs.
To run this file, put the cms_autoapi.py under the same directory as the main.py

"""
import sklearn.linear_model
from cms_autoapi import SignatureScraper
from cms_autoapi import CodeGenerator

def generate(class_name):
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
    classes = [class_name]
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
            template_folder='./templates',
            output_folder='./build'
        )

    code_gen.generate_command_interfaces(
        output_name='analytics_commands.py', template_name='command_interfaces.j2')
    code_gen.generate_command_setting(
        output_name='command_setting.json', template_name='command_setting.j2')
    code_gen.generate_handlers(
        output_name='analytics.py', template_name='handlers.j2')
    code_gen.generate_file_operations(
        output_name='file.py', template_name='file.py')
    code_gen.generate_server(
        output_name='server.py', template_name='server.j2')