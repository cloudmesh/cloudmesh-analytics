import typing
from pprint import pprint
from copy import deepcopy, copy
from sklearn.linear_model import LinearRegression

def a (x: int, y: float) -> int:
    """
    A sample

    :param x: a value
    :type x: int
    :return: result
    :return type: result
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

func = LinearRegression

attribute = dir(func)

print (func.__name__)
print (func.__doc__)

for a in attribute:
    if "__" not in a:
        print (">>>>", a)
        eval(f"print(func.{a})")

# print (func.__annotations__)
pprint (dir(func))

pprint (dir(func.fit))
pprint (func.fit.__doc__)