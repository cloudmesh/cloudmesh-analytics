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

        Attention:
            1. So far the attributes will not be included in signatures. Attributes should be considered later.

        Warnings:
            1. Orderdict: The order is not important if you specified the parameters names
            2. filtering the fucntions that are not public
    """
    res = {}
    # Traverse all classes and its members
    for i, class_name in enumerate(class_names):
        try:
            res[i] = {class_name: {}}

            # Get the clas obj and its doc string
            class_obj = getattr(sklearn.linear_model, class_name)
            doc = inspect.getdoc(class_obj)

            # Add members of the current class constructor
            res[i][class_name]['constructor'] = get_parameters(
                doc, type_table, types)

            # Operate on individual members
            for member_name, f in get_public_members(class_obj).items():
                if inspect.isfunction(f):
                    doc = inspect.getdoc(f)
                    paras_dict = get_parameters(doc, type_table, types)
                    if is_valid_function(paras_dict):
                        # The function whose parameters dict is not empy is valid for the conversion
                        res[i][class_name][member_name] = {}
                        res[i][class_name][member_name] = paras_dict
                    else:
                        continue
                else:
                    # TODO: To handle the properties
                    res[i][class_name][member_name] = f
        # Ignore the classes that do not have signatures
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
        ###################
        types.append(str(p.type))  # TODO: For testing purpose, to be removed.
        if p.name == 'set_params':
            print(p)
        ###################

        para_str = str(p.type)
        para_type = scraper.scrap(para_str)
        if is_valid_para(para_type, type_table):
            paras[p.name] = scraper.scrap(para_str)
        else:
            continue
    return paras


def is_valid_para(para_type, type_table):
    """Check if it is a valid parameter type contained in the type table.
    """
    # The values of the table contain all known destination types
    if para_type in type_table.values():
        return True
    return False


def is_valid_function(paras):
    """Check if a valid method with parameters

        Parameters:
            paras: A dictionary contains all parameters of the method

        Exampls:
            For some situation the there will no parameters due to empty doc string. This should be recorded and processed futher, e.g., {'set_params': {}} is not acceptable when doing conversion.
    """
    if len(paras) != 0:
        return True
    return False

def if_has_para_doc():
    pass