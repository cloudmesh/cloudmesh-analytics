import sklearn.linear_model
from cloudmesh.analytics.cms_autoapi import SignatureScraper

"""
import sklearn
import sklearn.linear_model
help (sklearn.linear_model.LinearRegression)
"""

def manual(service):
    # Type table
    type_table = {
        'matrix': 'array',
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
    classes = [service]
    # If type table is specified, it will read all classes in the module
    signatures = SignatureScraper().get_signatures(
        module=module,
        classes=classes,
        type_table=type_table)

    content = [
        service,
        len(service) * "=",
        ""
    ]

    for counter, entry in signatures.items():
        #
        # create value manual string
        #
        command = ["analytics {class_name}".format(**entry)]
        for parameter in entry["constructor"]:
            command.append(f"[{parameter}=VALUE]")
        content.append(' '.join(command))
        #
        # create method strings
        #
        for name, parameters in entry['members'].items():
            command = ["analytics {class_name} {name}".format(**entry, name=name)]
            for parameter in parameters:
                command.append(f"[{parameter}=VALUE]")
            content.append(' '.join(command))
        content.append('')

    return "\n".join(content)

