import inspect
import sys
import pprint
import sklearn.linear_model
import numpy as np
import json

from numpydoc import docscrape
from sklearn.linear_model import LinearRegression
from tests.utilities import type_scraper


def get_signatures(class_names, type_table, types):
    """Getting the signatures of sklean.linear_model

        Parameters:
            Types: A accumulator to collection infomration of types.

        Notes:
            Some of the functions are private and only be used by other functions inside which should be excluded.

        Warnings:
            1. Orderdict: The order is not important if you specified the parameters names
            2. filtering the fucntions that are not public
    """
    res = {}
    for i, class_name in enumerate(class_names):
        try:
            res[i] = {class_name: {}}
            doc = inspect.getdoc(getattr(sklearn.linear_model, class_name))
            res[i][class_name]['constructor'] = get_parameters(doc, type_table,types)
            for member_name, f in get_public_members(getattr(sklearn.linear_model, class_name)).items():
                res[i][class_name][member_name] = {}
                if inspect.isfunction(f):
                    doc = inspect.getdoc(f)
                    res[i][class_name][member_name] = get_parameters(doc, type_table, types)
                else:
                    # TODO: To handle the properties
                    res[i][class_name][member_name] = f
        except ValueError:
            pass
    return res


def get_public_members(obj):
    """Get public class members.

    It detect if the name of the object starts with the "_", which is the naming convention used in sklean. Python doesn't have real "private" members.

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


def get_parameters(doc, type_table, types):
    """Get parameters from the doc of a class, function, or property object.

    Given the sklean docstring follows the numpy conventions, this function use the numpy docstring parser to read the doc of sklean.
    """
    scraper = type_scraper.TypeScraper(type_table=type_table)
    r = docscrape.NumpyDocString(doc)
    paras = {}
    for p in r['Parameters']:
        types.append(str(p.type))  # TODO: For testing purpose, to be removed.
        para_str = str(p.type)
        paras[p.name] = scraper.scrap(para_str)
    return paras
