import pytest
from jinja2 import Environment, PackageLoader, FileSystemLoader
from sklearn.linear_model import LinearRegression


class TestGenerateFunctionApplications:

    @pytest.fixture
    def sigs(self):
        sigs = {0: {'class_name': 'LinearRegression',
                    'constructor': {'copy_X': 'bool',
                                    'fit_intercept': 'bool',
                                    'n_jobs': 'int',
                                    'normalize': 'bool'},
                    'members': {'fit': {'X': 'list', 'y': 'list'},
                                'property': 'property',
                                'get_params': {'deep': 'bool'},
                                'predict': {'X': 'list'},
                                'score': {'X': 'list', 'sample_weight': 'list', 'y': 'list'}}}}
        return sigs

    def test_generate(self, sigs):
        """Generate endpoint functions given parameters
        """
        env = Environment(loader=FileSystemLoader('./tests/test_assets'))
        template = env.get_template('endpoint_template.j2')

        all = {}
        all['cwd'] = './cm/cloudmesh-analytics/tests/test_assets/'
        all['sigs'] = sigs
        res = template.render(all=all)
        with open('./tests/test_assets/res.py', 'w') as f:
            f.write(res)
