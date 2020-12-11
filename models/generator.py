import random
import string

class Generator:
    def __init__(self, pattern):
        self._pattern = pattern

    def generate(self):
        code = ''
        for char in self._pattern:
            if char == '#':
                code += random.choice(string.digits)
            elif char == '*':
                code += random.choice(string.ascii_uppercase)
            elif char == '@':
                code += random.choice(string.digits + string.ascii_uppercase)
            else:
                code += char
        return code