import ast


class DictionaryEncoder:
    def __init__(self, encoding='ascii'):
        self.encoding = encoding

    def encode(self, dictionary):
        return str(dictionary).encode(self.encoding)

    def decode(self, byte):
        return ast.literal_eval(byte.decode(self.encoding))
