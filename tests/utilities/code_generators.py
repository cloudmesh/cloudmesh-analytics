from jinja2 import Environment, PackageLoader, FileSystemLoader
import os


class CodeGenerators:
    """Generate code for RES API applications
    """

    def __init__(self, func_signatures, cwd, template_folder, output_folder):
        self.func_signatures = func_signatures
        self.cwd = cwd
        self.template_folder = template_folder
        self.output_folder = output_folder

    def _generate_from_template(self, all, role_name, template_name):
        env = Environment(loader=FileSystemLoader(self.template_folder))
        template = env.get_template(template_name+'.j2')

        res = template.render(all=all)
        with open(os.path.join(self.output_folder, role_name+'.py'), 'w') as f:
            f.write(res)

    def generate_handlers(self, output_name, template_name):
        all = {}
        all['cwd'] = self.cwd
        all['sigs'] = self.func_signatures
        self._generate_from_template(all, output_name, template_name)

    def generate_command_runner(self, output_name, template_name):
        self._generate_from_template(self.func_signatures, output_name, template_name)

    def generate_command_definitions(self, output_name, template_name):
        self._generate_from_template(self.func_signatures, output_name, template_name)
