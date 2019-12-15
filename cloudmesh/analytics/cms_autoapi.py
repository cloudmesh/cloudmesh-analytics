import os
import re
import inspect
import sys
import numpy as np
import json
from numpydoc import docscrape
from jinja2 import Environment, PackageLoader, FileSystemLoader
import sklearn.linear_model
from cloudmesh.common.util import path_expand
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import writefile
from cloudmesh.analytics.OpenAPIServer import OpenAPIServer
from pprint import pprint


class CodeGenerator:
    """Generate code for REST API applications
    """

    def __init__(self,
                 func_signatures=None,
                 cwd=None,
                 function_operation_id_root=None,
                 file_operation_id_root=None,
                 server_url=None,
                 template_folder=None,
                 output_folder=None,
                 port=8000,
                 service=None):
        self.func_signatures = func_signatures
        self.cwd = cwd
        self.function_operation_id_root = function_operation_id_root
        self.file_operation_id_root = file_operation_id_root
        self.server_url = server_url
        self.template_folder = template_folder
        self.output_folder = output_folder
        self.port = port
        self.service = service

        self.all = {
            'service': service,
            'port': self.port,
            'class_name': service,
            'cwd': self.cwd,
            'sigs': self.func_signatures
        }

        all = self.construct_yaml_fields(
            signatures=self.func_signatures,
            function_operation_id_root=self.function_operation_id_root,
            file_operation_id_root=self.file_operation_id_root,
            server_root_url=self.server_url)
        self.all.update(all)

        pprint(self.all)


    def _generate_from_template(self, role_name, template_name):
        env = Environment(loader=FileSystemLoader(self.template_folder))
        template = env.get_template(template_name)

        res = template.render(all=self.all)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        with open(os.path.join(self.output_folder, role_name), 'w') as f:
            f.write(res)

    def generate_server(self, output_name, template_name, class_name):
        self._generate_from_template(output_name, template_name)

    def generate_handlers(self, output_name, template_name):
        self._generate_from_template(output_name, template_name)

    def generate_command_setting(self, output_name, template_name):
        self._generate_from_template(output_name, template_name)

    def generate_api_specification(self,
                                   output_name,
                                   template_name):
        self._generate_from_template(output_name, template_name)

    def generate_file_operations(self, output_name, template_name):
        self._generate_from_template(output_name, template_name)

    def construct_yaml_fields(self,
                              signatures,
                              function_operation_id_root,
                              file_operation_id_root,
                              server_root_url):
        """
        Parse the signatures of functions to a dictionary that is used to
        generate yaml files.

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
            constructor_yaml_info = {
                'name': 'constructor',
                'request_method': 'post',
                'doc_string': 'this is a doc string',
                'operation_id': f'{class_i_name}.constructor',
                'paras': {}}

            for _name, _type in class_i['constructor'].items():
                constructor_yaml_info['paras'][_name] = {
                    'name': _name, 'type': _type}
            table_yaml[count] = constructor_yaml_info

            # build the yaml information table for class members
            for member_name, parameters in class_i['members'].items():
                count += 1
                if member_name != 'property':
                    member_yaml_info = {
                        'name': member_name,
                        'request_method': 'post',
                        'doc_string': 'this is a doc string',
                        'operation_id': f'{class_i_name}.{member_name}',
                        'paras': {}
                    }

                    for _name, _type in parameters.items():
                        member_yaml_info['paras'][_name] = {
                            'name': _name, 'type': _type
                        }
                    table_yaml[count] = member_yaml_info
        res = {
            'header': {'server_url': server_root_url},
            'functions': table_yaml,
            'files': {'operation_id': file_operation_id_root}
        }
        return res


class TypeScraper:
    """Scrape types from a string.
        Using  the regular expression to match the keywords that imply the
        types.

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

        # Traverse all known mappings to check which key of the table
        # matches the string
        for table_key in self.type_table.keys():
            if re.search(table_key, literal_type, re.IGNORECASE):
                res.add(self.type_table[table_key])

        # For testing purpose, if more than one is machted, it should report
        # error
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
                                    'score': {'X': 'list',
                                    'sample_weight': 'list', 'y': 'list'}}}}
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

                for name, f in self.get_public_members(class_obj).items():
                    if inspect.isfunction(f):
                        doc = inspect.getdoc(f)
                        paras_dict = self.get_parameters(doc, type_table)
                        current_members[name] = paras_dict
                    else:
                        continue
            # Ignore the classes that do not have signatures
            except ValueError:
                pass

            # Delete the setter functions
            if 'set_params' in current_members.keys():
                del current_members['set_params']

        return res

    def get_public_members(self, obj):
        """Get public class members.

        It detect if the name of the object starts with the "_",
        which is the naming convention used in sklean. Python doesn't have
        real "private" members.

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

        Given the sklean docstring follows the numpy conventions, this function
        use the numpy docstring parser to read the doc of sklean.
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
                For some situation the there will no parameters due to empty
                doc string. This should be recorded and processed futher,
                e.g., {'set_params': {}} is not acceptable when doing conversion.
        """
        if len(paras) != 0:
            return True
        return True


def main_generate(class_name,
                  directory,
                  port=8000):
    #
    # set up dir structure
    #

    Shell.mkdir(f"{directory}/{class_name}")
    Shell.mkdir(f"{directory}/{class_name}/cloudmesh")
    writefile(f"{directory}/{class_name}/cloudmesh/__init__.py", "")

    #
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

    template_folder = os.path.join((os.path.dirname(__file__)),
                                   'code_templates')
    directory = path_expand(directory)

    print(template_folder)
    print(directory)

    generator = CodeGenerator(
        func_signatures=sigs,
        cwd=directory,
        # BUG: THIS IS WRONG
        function_operation_id_root='.',
        file_operation_id_root='cloudmesh.analytics.build.file',
        # server_url=f'http://localhost:5000/cloudmesh-analytics/{class_name}',
        server_url=f'http://localhost:5000/cloudmesh/{class_name}',
        template_folder=template_folder,
        output_folder=directory,
        port=port,
        service=class_name
    )

    generator.generate_api_specification(
        output_name=f'{class_name}/{class_name}.yaml',
        template_name='component.j2')

    generator.generate_handlers(
        output_name=f'{class_name}/cloudmesh/{class_name}.py',
        template_name='handlers.j2')

    generator.generate_file_operations(
        output_name=f'{class_name}/cloudmesh/file.py',
        template_name='file.py')

    #
    # Generate the server code while using a build in cloudmesh specific server
    #
    server = OpenAPIServer(
        host="127.0.0.1",
        path=".",
        spec=f"{class_name}.yaml",
        key="dev")
    server.write(f'{directory}/{class_name}/{class_name}_server.py')

    generator.output_folder = os.path.join((os.path.dirname(__file__)),
                                           'command')
    print(directory)

    # generator.generate_command_setting(
    #     output_name='command_setting.json',
    #     template_name='command_setting.j2')
