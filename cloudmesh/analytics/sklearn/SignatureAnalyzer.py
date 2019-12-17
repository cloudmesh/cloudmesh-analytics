from numpydoc import docscrape

class SignatureAnalyzer:
    """

        analyzer = SignatureAnalyzer(doc_string)
        parameters = analyzer.parameters()
        summary = analyzer.summary()

        print (analyzer)

    """

    def __init__(self, doc_string):
        self.doc_string = docscrape.NumpyDocString(doc_string)

    @staticmethod
    def type_from_string(name):
        _type = {
            'str': str,
            "string": str,
            "dict": dict,
            'int': int,
            'bool': bool,
            'float': float,
            'auto': str
        }
        try:
            return _type[name]
        except:
            return name


    def parameters(self):
        _parameters = {}
        for p in self.doc_string['Parameters']:
            #print (f"Parameter Analysis {p.name}: {p.type}")
            #print()
            default_type = type(eval(p.type.split("default=")[1].replace(")", "")))
            _name = p.name
            _type = default_type
            if default_type is type(None):
                _type = p.type.split(",", 1)[0]
                if "or" in _type:
                    _type = _type.split(" or ")[0].strip()
                string_type = SignatureAnalyzer.type_from_string(_type)
                print (p.name, ":", p.type, default_type, string_type)
                _type = string_type
            _parameters[_name] = _type
        return _parameters

    def summary(self):
        return "\n".join(self.doc_string["Summary"])

    def __str__(self):
        _summary = self.summary()
        result = [
            "",
            _summary,
            len(_summary) *"="
        ]
        for parameter, _type in self.parameters().items():
            result.append (f"    {parameter:20} {_type}")
        result.append("")
        return "\n".join(result)




