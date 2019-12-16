import os
import re
import inspect
import sys
import numpy as np
import json
from numpydoc import docscrape
from jinja2 import Environment, PackageLoader, FileSystemLoader
import sklearn.linear_model


class CodeGenerator:
    """Generate code for REST API applications
    """

    def __init__(self, func_signatures, cwd, function_operation_id_root,
                 file_operation_id_root, server_url, template_folder,
                 output_folder):
        self.func_signatures = func_signatures
        self.cwd = cwd
        self.function_operation_id_root = function_operation_id_root
        self.file_operation_id_root = file_operation_id_root
        self.server_url = server_url
        self.template_folder = template_folder
        self.output_folder = output_folder

    def _generate_from_template(self, all, role_name, template_name):
        env = Environment(loader=FileSystemLoader(self.template_folder))
        template = env.get_template(template_name)

        res = template.render(all=all)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        with open(os.path.join(self.output_folder, role_name), 'w') as f:
            f.write(res)

    def generate_server(self, output_name, template_name, port):
        all = {}
        all['port'] = port
        self._generate_from_template(
            all, output_name, template_name)

    def generate_handlers(self, output_name, template_name):
        all = {}
        all['cwd'] = self.cwd
        all['sigs'] = self.func_signatures
        self._generate_from_template(all, output_name, template_name)

    def generate_command_interfaces(self, output_name, template_name):
        self._generate_from_template(
            self.func_signatures, output_name, template_name)

    def generate_command_setting(self, output_name, template_name, port):
        all = {}
        all['port'] = port
        self._generate_from_template(
            all, output_name, template_name)

    def generate_api_specification(self, output_name, template_name):
        all = self.construct_yaml_fields(signatures=self.func_signatures,
                                         function_operation_id_root=self.function_operation_id_root,
                                         file_operation_id_root=self.file_operation_id_root,
                                         server_root_url=self.server_url)
        self._generate_from_template(all, output_name, template_name)

    def generate_file_operations(self, output_name, template_name):
        self._generate_from_template(all, output_name, template_name)

    def generate_docker_build_run(self, output_name, template_name, class_name, port):
        all = {}
        all['class_name'] = class_name
        all['port'] = port
        self._generate_from_template(all, output_name, template_name)

    def generate_dockerfile(self, output_name, template_name):
        self._generate_from_template(
            self.func_signatures, output_name, template_name)

    def generate_requirements(self, output_name, template_name):
        self._generate_from_template(
            self.func_signatures, output_name, template_name)


    def construct_yaml_fields(self, signatures, function_operation_id_root,
                              file_operation_id_root, server_root_url):
        """
        Parse the signatures of functions to a dictionary that is used to generate yaml files.

        f = {0: {'name': 'linear-regression',
                    'request_method': 'post',
                    'doc_string': 'this is a doc string',
                    'operation_id': 'cloudmesh.linear_regression',
                    'paras': {
                    'file_name': {'name': 'file_name', 'type': 'string'},
                    'intercept': {'name': 'intercept', 'type': 'int'}
                }}}
        """
        table_yaml = {}
        count = 0
        for i, class_i in signatures.items():
                # build the yaml information table for class constructor
            count += 1
            class_i_name = class_i['class_name']
            constructor_yaml_info = {}
            constructor_yaml_info['name'] = class_i_name + '_constructor'
            constructor_yaml_info['request_method'] = 'post'
            constructor_yaml_info['doc_string'] = 'this is a doc string'
            constructor_yaml_info['operation_id'] = function_operation_id_root + '.' + \
                class_i_name + '_constructor'
            constructor_yaml_info['paras'] = {}
            for init_para_name, init_para_type in class_i['constructor'].items():
                constructor_yaml_info['paras'][init_para_name] = {
                    'name': init_para_name, 'type': init_para_type}
            table_yaml[count] = constructor_yaml_info

            # build the yaml information table for class members
            for member_name, parameters in class_i['members'].items():
                count += 1
                if (member_name != 'property'):
                    member_yaml_info = {}
                    member_yaml_info['name'] = class_i_name + '_' + member_name
                    member_yaml_info['request_method'] = 'post'
                    member_yaml_info['doc_string'] = 'this is a doc string'
                    member_yaml_info['operation_id'] = function_operation_id_root + '.' + \
                        class_i_name + '_' + member_name
                    member_yaml_info['paras'] = {}
                    for member_para_name, member_para_type in parameters.items():
                        member_yaml_info['paras'][member_para_name] = {
                            'name': member_para_name, 'type': member_para_type}
                    table_yaml[count] = member_yaml_info
        res = {'header': {'server_url': server_root_url},
               'functions': table_yaml,
               'files': {'operation_id': file_operation_id_root}
               }
        return res


class TypeScraper:
    """Scrape types from a string.
        Using  the regular expression to match the keywords that imply the types.

        A type table for matching the types from the string is required

        Examples:
            'boolean, optional, default True' = bool
            'int or None, optional (default=None)' = int
            'array-like or sparse matrix, shape (n_samples, n_features)' = list
            'numpy array of shape [n_samples]' 'boolean, optional' = list
 """

    def __init__(self, type_table):
        """The Constructor function

            Parameters:
                type_table: A dictionary indicates the matching rules
        """
        self.type_table = type_table

    def scrap(self, literal_type):
        """Match types from the string

            Parameters:
                literal_type: A string that defines a type
        """

        res = set()

        # Traverse all known mappings to check which key of the table matches the string
        for table_key in self.type_table.keys():
            if re.search(table_key, literal_type, re.IGNORECASE):
                res.add(self.type_table[table_key])

        # For testing purpose, if more than one is machted, it should report error
        if len(res) == 1:
            return res.pop()
        else:
            return 'Error'


class SignatureScraper:

    def get_signatures(self, module, classes, type_table):
        """Getting the signatures of sklean.linear_model

            Examples:
                {0: {'class_name': 'LinearRegression',
                        'constructor': {'copy_X': 'bool',
                                        'fit_intercept': 'bool',
                                        'n_jobs': 'int',
                                        'normalize': 'bool'},
                        'members': {'fit': {'X': 'list', 'y': 'list'},
                                    '__property___': '__property___',
                                    'get_params': {'deep': 'bool'},
                                    'predict': {'X': 'list'},
                                    'score': {'X': 'list', 'sample_weight': 'list', 'y': 'list'}}}}
        """
        res = {}
        # Traverse all classes and its members
        for i, class_name in enumerate(classes):
            try:
                current_class = {}
                res[i] = current_class
                current_class['class_name'] = class_name

                # Get the clas obj and its doc string
                class_obj = getattr(module, class_name)
                doc = inspect.getdoc(class_obj)

                # Add members of the current class constructor
                current_class['constructor'] = self.get_parameters(
                    doc, type_table)

                # Operate on individual members
                current_members = {}
                current_class['members'] = current_members

                for member_name, f in self.get_public_members(class_obj).items():
                    if inspect.isfunction(f):
                        doc = inspect.getdoc(f)
                        paras_dict = self.get_parameters(doc, type_table)
                        current_members[member_name] = paras_dict
                    else:
                        continue
            # Ignore the classes that do not have signatures
            except ValueError:
                pass

            # Delete the setter functions
            if 'set_params' in current_members.keys():
                del current_members['set_params']

            current_members['get_properties'] = {'name': 'str'}

            # current_members['get_properties'] = {'name':'str'}
        return res

    def get_public_members(self, obj):
        """Get public class members.

        It detect if the name of the object starts with the "_", which is the naming convention used in sklean. Python doesn't have real "private" members.

        Attention:
            The type of members
                1. public
                    1. properties -- How to deal with properties? #TODO
                    2. functions -- only functions should be exposed
                2. private
        """
        def isprivate(name):
            if name[0] == '_':
                return True
            else:
                return False

        public_members = {}
        for k, v in inspect.getmembers(obj):
            if not isprivate(k):
                public_members[k] = v
        return public_members

    def get_parameters(self, doc, type_table):
        """Get parameters from the doc of a class, function, or property object.

        Given the sklean docstring follows the numpy conventions, this function use the numpy docstring parser to read the doc of sklean.
        """
        scraper = TypeScraper(type_table=type_table)
        r = docscrape.NumpyDocString(doc)
        paras = {}
        for p in r['Parameters']:

            para_str = str(p.type)
            para_type = scraper.scrap(para_str)
            if self.is_valid_para(para_type, type_table):
                paras[p.name] = scraper.scrap(para_str)
            else:
                continue
        return paras

    def is_valid_para(self, para_type, type_table):
        """Check if it is a valid parameter type contained in the type table.
        """
        # The values of the table contain all known destination types
        if para_type in type_table.values():
            return True
        return True

    def is_valid_function(self, paras):
        """Check if a valid method with parameters

            Parameters:
                paras: A dictionary contains all parameters of the method

            Exampls:
                For some situation the there will no parameters due to empty doc string. This should be recorded and processed futher, e.g., {'set_params': {}} is not acceptable when doing conversion.
        """
        if len(paras) != 0:
            return True
        return True


def main_generate(class_name, port):
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

    template_folder = os.path.join(
        (os.path.dirname(__file__)), 'code_templates')
    output_folder = os.path.join(
        (os.path.dirname(__file__)), 'build')

    print(template_folder)
    print(output_folder)

    code_gen = CodeGenerator(
        func_signatures=sigs,
        cwd=output_folder,
        function_operation_id_root='analytics',
        file_operation_id_root='file',
        server_url='http://localhost:8000/cloudmesh-analytics',
        template_folder=template_folder,
        output_folder=output_folder
    )


    code_gen.generate_handlers(
        output_name='analytics.py', template_name='handlers.j2')
    code_gen.generate_file_operations(
        output_name='file.py', template_name='file.j2')
    code_gen.generate_server(
        output_name='server.py', template_name='server.j2', port=port)
    code_gen.generate_api_specification(
        output_name='analytics.yaml', template_name='component.j2')
    code_gen.generate_dockerfile(
        output_name='Dockerfile', template_name='dockerfile.j2')
    code_gen.generate_requirements(
        output_name='requirements.txt', template_name='requirements.j2')

    code_gen.output_folder = os.path.join((os.path.dirname(__file__)), 'command')
    print(output_folder)
    #code_gen.generate_command_interfaces(
    #    output_name='analytics.py', template_name='command_interfaces.j2')
    code_gen.generate_docker_build_run(
        output_name='docker_build_run_commands.sh', template_name='docker_build_run_commands.j2', class_name=class_name, port=port)
    code_gen.generate_command_setting(
        output_name='command_setting.json', template_name='command_setting.j2', port=port)