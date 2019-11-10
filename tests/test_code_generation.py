"""Generate yaml and python code from the target functions
"""
from jinja2 import Environment, PackageLoader, FileSystemLoader
from .utilities import signature_retriever
from numpydoc import docscrape
import inspect
import pprint
import pytest
import sklearn.linear_model
from sklearn import svm


def test_generate_yaml():
    """Generate yaml file using the python template engine"""
    # template = env.get_template('component.yaml')

    f = {'name': 'linear-regression',
         'request_method': 'post',
         'doc_string': 'this is a doc string',
         'operation_id': 'cloudmesh.linear_regression',
         'paras': {
             'file_name': {'name': 'file_name', 'type': 'string'},
             'intercept': {'name': 'intercept', 'type': 'int'}

         }}

    g = {'name': 'logistic-regression',
         'request_method': 'post',
         'doc_string': 'this is a doc string',
         'operation_id': 'cloudmesh.linear_regression',
         'paras': {
             'file_name': {'name': 'file_name', 'type': 'string'},
             'intercept': {'name': 'intercept', 'type': 'int'}
         }}

    all = {1: g, 2: f}

    # print(all)
    # print(template.render(all=all))


class TestSignatureRetrievers:
    """Test Signature Retrivers

    In order to automate REST API generate process, the signature retriever would collect the signatures of class, func-
    tions and properties.

    Notes:
        - Given a list of class, to acquire the signatures of class __init__ attribute, and the members
        - Some functions are private and should not be exposed. Making a list to ignore those functions or properties
    """
    @pytest.fixture()
    def sample_parameters(self):
        res = signature_retriever.get_signatures(['LinearRegression'])
        doc = inspect.getdoc(sklearn.linear_model.LinearRegression.set_params)
        r = docscrape.NumpyDocString(doc)
        return r['Parameters']

    def test_exclude_private_members(self):
        pass

    def test_exclude_functions(self):
        pass

    def test_retrieve_signatures(self):
        modules = sklearn.linear_model.__all__
        sample = ['LinearRegression']
        pprint.pprint(signature_retriever.get_signatures(modules))

    def test_get_parameters(self, sample_parameters):
        for p in sample_parameters:
            print(p.name, ':', str(p.type).split(' ')[0])

    def test_generate_data_type_table(self):
        pass


class TestLiteralTypeMatcher:
    """Match types from text what literally defined.

        The types are crucial to generate yaml and endpoint functinos.

        Examples:
            x = [[1,2],[3,4]]
            reg = LinearRegression(X= x ...)
            The x must be a list when it is passed to the counstructor. When the functions are automatically generated, it must know the type of the x given mapped by connexion from request or errors occur.
    """

    @pytest.fixture
    def type_table():
        re_key = {
            'array': 'list',
            'bool': 'bool',
            'int': 'int'
        }
        return

    def test_match(self):
        a = 'boolean'
        assert bool == literal_match_type(a)
