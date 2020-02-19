import typing
from pprint import pprint
from copy import deepcopy, copy
from cloudmesh.common.util import readfile

def a (x: int, y: float) -> int:
    """
    A sample.

    :param x: x value
    :type x: int
    :param y: y value
    :type y: float
    :return: result
    :return type: int
    """
    return 1

# help(a)

func = a

print ()
counter = 1
for f in [
    func.__name__,
    func.__code__.co_argcount,
    func.__code__.co_varnames,
    func.__code__.co_cellvars,
    func.__code__.co_code,
    func.__code__.co_consts,
    func.__code__.co_filename,
    func.__code__.co_firstlineno,
    func.__code__.co_flags,
    func.__code__.co_freevars,
    func.__code__.co_kwonlyargcount,
    func.__code__.co_lnotab,
    func.__code__.co_name,
    func.__code__.co_names,
    func.__code__.co_nlocals,
    func.__code__.co_posonlyargcount,
    func.__code__.co_stacksize,
    func.__code__.co_varnames,
    func.__doc__]:
    print (counter, f)
    counter +=1

print (func.__annotations__)

template = """
openapi: 3.0.0
info:
  title: {title}
  description: {description}
  version: {version}
servers:
  - url: http://localhost/cloudmesh/{title}
    description: Optional server description, e.g. Main (production) server
paths:
  /{name}:
     get:
        ....
  /users:
    get:
      summary: Returns a list of users.
      description: Optional extended description in CommonMark or HTML.
      responses:
        '200':    # status code
          description: A JSON array of user names
          content:
            application/json:
              schema: 
                type: array
                items: 
                  type: string
"""

description = func.__doc__.strip().split("\n")[0]
version = open('../VERSION','r').read()

spec = template.format(
    title = func.__name__,
    name = func.__name__,
    description = description,
    version = version
)

print (spec)

print (version)