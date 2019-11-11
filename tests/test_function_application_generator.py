import pytest
from jinja2 import Environment, PackageLoader, FileSystemLoader
from sklearn.linear_model import LinearRegression

# def linear_regression(file_name, body):
#     """
#     Linear regression operation on two dimension data. The input format should be a list of pairs, e.g. [[1, 2], [3, 4]...]

#     """
#     # Extract parameters from the request body
#     paras = body['paras']
#     # TODO: Data format is not correct
#     try:
#         data = read_csv(file_name)
#         X = data[:, :-1]
#         Y = data[:, -1]
#         reg = LinearRegression(**paras).fit(X, Y)
#         return jsonify({'coefficient': reg.coef_.tolist()})
#     except Exception as e:
#         return jsonify({'error': str(e)})
import pickle
import os
import numpy as np

# X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
# y = np.dot(X, np.array([1, 2])) + 3

X = [[1, 1], [1, 2], [2, 2], [2, 3]]
y = list(np.dot(X, np.array([1, 2])))

body = {
    'init': {},
    'paras': {
        'X': X,
        'y': y
    }
}

p_body = {
    'paras': {'X': [[3, 5]]}
}


def load_obj(path):
    return np.load(path, allow_pickle=True)


def save_obj(obj):
    np.save('./cm/cloudmesh-analytics/tests/test_assets/linear_regression_constructor',
            obj, allow_pickle=True)
    return


def linear_regression_constructor(body):
    init = body['init']
    reg = LinearRegression(**init)
    save_obj(reg)
    return reg


def linear_regression_fit(body):
    reg = load_obj(
        './cm/cloudmesh-analytics/tests/test_assets/linear_regression_constructor.npy').item()
    reg = reg.fit(**body['paras'])
    save_obj(reg)
    return reg


def linear_regression_coef_(body):
    reg = load_obj(
        './cm/cloudmesh-analytics/tests/test_assets/linear_regression_constructor.npy').item()
    return reg.coef_


def linear_regression_predcit(body):
    paras = body['paras']
    reg = load_obj(
        './cm/cloudmesh-analytics/tests/test_assets/linear_regression_constructor.npy').item()
    return reg.predict(**paras)


"""
    The types of operations:
        1. Constructor
        2. Call method of the class constructed constructor after loaded
            1. Methods that do not have return value that mutate the class instance
            2. Methods that have return value
        3. Get attribute of the class after loaded 
"""


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
        env = Environment(loader=FileSystemLoader('./tests/test_assets'))
        template = env.get_template('endpoint_template.j2')
        all = {}
        
        all['cwd']='./cm/cloudmesh-analytics/tests/test_assets/'
        all['sigs'] = sigs
        res =template.render(all=all) 
        with open('./tests/test_assets/res.py', 'w') as f:
            f.write(res)