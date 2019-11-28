# Scikit-learn REST API Generation Manual

## Introduction

Scikit-learn offers various functionalities related to the machine learning, i.e., the classification model and linear regression model. When it comes to expose its AI functionalities, then repetitively work occurs. 

### A Laborious Example
For example, making two regression methods from the linear model of Scikit-learn, which are the liner regression and logistic regression, involves writing the code in the similar pattern. The examples are based Flask, which is a python web application framework. 
```python
# server.py
from flask import Flask
app = connexion.App(__name__, specification_dir=".")
app.add_api('analytics.yaml')
@app.route('/')
def hello_world():
    return 'Hello, World!'
```

```
# analytics.yaml
...
paths:
  /LinearRegression_constructor/:
      post:
        summary: this is a doc string
        operationId: analytics.LinearRegression_constructor
```

```python
# analytics.py
def LinearRegression_constructor(body):
    try:
        paras = body['paras']
        res = LinearRegression(**paras)
    except Exception as e:
        return jsonify({'Error': str(e)})
    return jsonify({'return': 'successfully constructed'})
```
In order to expose the linear regression class as a RESTful interface, one should write the yaml file which defines the routing, and the endpoint function to handle this request.

The example implies that each request to a specific function requires a corresponding definition under the path field in the yaml file. So it is not surprising that will take a large amount of time to write hundreds of functions.

### Automating the Process
Similarly, when adding a the logistic regression, the new endpoint function and corresponding yaml field follow the same pattern, which is shown below.
```
# analytics.yaml
...
paths:
  ...
  /LogisticrRegression_constructor/:
      post:
        summary: this is a doc string
        operationId: analytics.LogisticRegression_constructor
```

```python
# analytics.py
...
def LogisticRegression_constructor(body):
    try:
        paras = body['paras']
        res = LogisticRegression(**paras)
    except Exception as e:
        return jsonify({'Error': str(e)})
    return jsonify({'return': 'successfully constructed'})
```
In order to expose a function as a REST API, there are limited types of functions in the Scikit-learn. Those can be summarized as,

|Function Type/Return|  Yes | No |
|:-----------:|:-------------:|:------:|
|Constructor| object        |\|
|Methods    | getters|setter|
|Property   | attributes|\|

From the table, the function can be a constructor to initialize a new class instance without return value, or getter and setter functions. Some classes have public properties, i.e., LinearRegression.coef_. Therefore, the ways to handle the same types of functions are almost identical, which makes it easier to just write a template for each type of function, and others can be automatically generated on the fly.

## The Code Generator

### Function Signatures

The code generator can read a python module that contains classes, and generate an web application that expose the functions in the module as REST APIs. 

Function signatures need to be captured before the generation. The signature_scraper class will scrape the functions from a module, and return re-organize signature into a python dict. The shown example reads the signature of the linear regression class.

```python
# main.py
import SignaturesScraper
type_table = {'matrix': 'array',
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
sigs = SignaturesScraper.get_signatures(
    module,
    classes, type_table)

# sigs
{0: {'class_name': 'LinearRegression',
     'constructor': {'copy_X': 'bool',
                    'fit_intercept': 'bool',
                    'n_jobs': 'int',
                    'normalize': 'bool'},
     'members': {'fit': {'X': 'list', 'y': 'list'},
                'property': 'property',
                'get_params': {'deep': 'bool'},
                'predict': {'X': 'list'},
                'score': {'X': 'list',
                'sample_weight': 'list', 'y': 'list'}}}}
```

The type table is required for the signature scraper to search the doc string of functions or classes to match and retrieve the types of parameters due to lacking of types definitions in the signatures. However, the type doesn't affect the code generation but for generating more accurate definition of request bodies in the yaml file.

### Generating the Application

```python
import CodeGenerators
# Initialize the code generator
code_gen = code_generators.CodeGenerators(
    func_signatures=sigs,
    # The output directory
    output_folder='./tests/test_assets/build')
# Generate the anlaytics.py which includes
# endpoint functions
code_gen.generate_handlers(
    output_name='analytics.py)
```

The example demonstrates how to generate the endpoint functions, which are in the analytics.py file. In order to run a flask application. The analytics.yaml file and server.py are required as well.  
```python
code_gen.generate_openapi(
    output_name='analytics.ymal')
code_gen.generate_server(
    output_name='server.py)
```