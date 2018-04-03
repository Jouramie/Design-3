from .stylized_flag import StylizedFlag


class Country(object):
    def __init__(self, name: str, code: int, stylized_flag: StylizedFlag):
        self.name = name
        self.code = code
        self.stylized_flag = stylized_flag

    def __str__(self) -> str:
        return str({'name': self.name, 'code': self.code})
