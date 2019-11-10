import re

class TypeScraper:
    """Scrape types from a string.
        Using  the regular expression to match the keywords that imply the types.
        
        A type table for matching the types from the string is required

        Examples:
            'boolean, optional, default True' = bool
            'int or None, optional (default=None)' = int
            'array-like or sparse matrix, shape (n_samples, n_features)' = list
            'numpy array of shape [n_samples]' 'boolean, optional' = list
 """
    def __init__(self, type_table):
        """The Constructor function

            Parameters:
                type_table: A dictionary indicates the matching rules
        """
        self.type_table = type_table

    def scrap(self, literal_type):
        """Match types from the string

            Parameters:
                literal_type: A string that defines a type
        """

        res = []

        # Traverse all known mappings to check which key of the table matches the string
        for table_key in self.type_table.keys(): 
            if re.search(table_key, literal_type,re.IGNORECASE):
                res.append(self.type_table[table_key])
        
        # For testing purpose, if more than one is machted, it should report
        if len(res) == 1:
            return res[0]
        else:
            return None