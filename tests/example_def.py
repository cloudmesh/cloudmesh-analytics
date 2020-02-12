import typing
from pprint import pprint
from copy import deepcopy, copy
from sklearn.linear_model import LinearRegression

def a (x: int, y: float) -> int:
    """
    A sample

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
    func.__code__.co_argcount,
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
