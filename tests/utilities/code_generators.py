from jinja2 import Environment, PackageLoader, FileSystemLoader
import os

class CodeGenerators:
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
        with open(os.path.join(self.output_folder, role_name), 'w') as f:
            f.write(res)

    def generate_handlers(self, output_name, template_name):
        all = {}
        all['cwd'] = self.cwd
        all['sigs'] = self.func_signatures
        self._generate_from_template(all, output_name, template_name)

    # def generate_command_runner(self, output_name, template_name):
    #     self._generate_from_template(
    #         self.func_signatures, output_name, template_name)

    # def generate_command_definitions(self, output_name, template_name):
    #     self._generate_from_template(
    #         self.func_signatures, output_name, template_name)

    def generate_command_interfaces(self, output_name, template_name):
        self._generate_from_template(
            self.func_signatures, output_name, template_name)

    def generate_api_specification(self, output_name, template_name):
        all = construct_yaml_fields(signatures=self.func_signatures,
                                    function_operation_id_root=self.function_operation_id_root,
                                    file_operation_id_root=self.file_operation_id_root,
                                    server_root_url=self.server_url)
        self._generate_from_template(all, output_name, template_name)

    def generate_file_operations(self, output_name, template_name):
        self._generate_from_template(all, output_name, template_name)


def construct_yaml_fields(signatures, function_operation_id_root,
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
           'files':{'operation_id':file_operation_id_root}
           }
    return res


"""
Code generation configurations
    1. The naming rules
    2. The working directory that makses it works
    3. Add a way to configure the generator
    4. The configurations
        1. type table
    5. configure url in the yaml 
    6. load X, y from file
    7. Add a new field to get all propertyies
"""
