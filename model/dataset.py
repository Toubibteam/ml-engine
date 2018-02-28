import unicodedata

class CodeDataset:
    """Loads codes and their description with some preprocessing"""

    """ Class attributes """
    # (int) number of instances created
    _instances = 0
    # (dict) contains all the ccam codes
    _ccam_codes = {}
    # (dict) contains all the cim codes
    _cim_codes = {}

    def __init__(self, db, vocab=None):
        self._vocab = vocab
        self.__class__.loadCodes(db)
        self.__class__._instances += 1
        print "dataset loaded"


    @classmethod
    def formatCCAMCode(cls, code):
        """ Format a CCAM code from database to the expected format for processing

        Args:
            cls: (object) the class itself
            code: (object) ccam code from database

        Returns:
            key: (string) key to refer to in dictionnary
            value: (object) formated ccam code

        """
        key = code["code"]
        value = {
            "description": code["description"],
            "keywords": code["keywords"],
            "tarif": code["tarif"]
        }
        return key, value


    @classmethod
    def formatCIMCode(cls, code):
        """ Format a CIM code from database to the expected format for processing

        Args:
            cls: (object) the class itself
            code: (object) cim code from database

        Returns:
            key: (string) key to refer to in dictionnary
            value: (object) formated cim code

        """
        key = code["code"]
        value = {
            "description": code["description"],
            "keywords": code["keywords"],
            "tarif": code["tarif"]
        }
        return key, value


    @classmethod
    def loadCodes(cls, db):
        """ Load ccam and cim codes from database

        Args:
            cls: (object) the class itself
            db: (object) connection to the database

        Returns:
            none

        """
        if cls._instances == 0:
            for code in db.ccam.find():
                key, value = cls.formatCCAMCode(code)
                cls._ccam_codes[key] = value

            for code in db.cim.find():
                key, value = cls.formatCIMCode(code)
                cls._cim_codes[key] = value


    def get_description(self, code_id, type_code):
        """ Get the details of a code

        Args:
            self: (object) class instance
            code_id: (string, object) id of the code
            type_code: (string) either "CCAM" or "CIM"

        Returns:
            (object) details of the code, None if not in the dict

        """
        codes = self.__class__._ccam_codes if type_code == "CCAM" else self.__class__._cim_codes

        if code_id not in codes:
            return None
        else:
            return codes[code_id]


    def build_descriptions(self, type_code):
        """ Build descriptions for a specific set of codes

        Args:
            self: (object) class instance
            type_code: (string) either "CCAM" or "CIM"

        Returns:
            (object) a generator to process descriptions one after an other that returns
                code: (string, array) id of the code
                descriptions: (array) preprocessed descriptions

        """
        codes = self.__class__._ccam_codes if type_code == "CCAM" else self.__class__._cim_codes

        for code in codes:
            details = codes[code]

            keywords = {}
            for kw in details["keywords"]:
                keywords[self._vocab.tok_to_id(kw["word"])] = kw["w"]

            if keywords is not None:
                yield code, keywords
