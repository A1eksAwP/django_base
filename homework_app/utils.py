from random import choice
import re


class SwitchCase:
    def __init__(self, text: str, case: str = 'default'):
        self.base_text = text.strip()
        self.case = case
        self.text = self.set_case

    def __str__(self):
        return self.text

    @property
    def set_case(self):
        match self.case:
            case 'default': return self.default_case()
            case 'sentence': return self.sentence_case()
            case 'upper': return self.upper_case()
            case 'lower': return self.lower_case()
            case 'each_word': return self.each_word_case()
            case 'toggle': return self.toggle_case()
            case 'kebab': return self.kebab_case()
            case 'snake': return self.snake_case()
            case 'camel': return self.camel_case()
            case 'random': return self.random_case()
            case 'rot13': return self.rot13_case()
            case 'cipher': return self.random_cipher()
            case _: return self.default_case()

    def default_case(self):
        return self.base_text

    def sentence_case(self):
        return self.base_text.capitalize()

    def upper_case(self):
        return self.base_text.upper()

    def lower_case(self):
        return self.base_text.lower()

    def each_word_case(self):
        return self.base_text.title()

    def toggle_case(self):
        return ''.join(c.upper() if c.islower() else c.lower() for c in self.base_text)

    def kebab_case(self):
        return re.sub(r'\s', r'-', re.sub(r'\d', '', self.base_text)).lower()

    def snake_case(self):
        return re.sub(r'\s', r'_', re.sub(r'\d', '', self.base_text)).lower()

    def camel_case(self):
        return re.sub(r'\d', '', self.base_text).title().replace(' ', '')

    def random_case(self):
        return ''.join(choice([c.upper(), c.lower()]) for c in self.base_text)

    def rot13_case(self):
        enc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        dec = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM"
        return ''.join(dec[enc.find(ch)] if ch.isalpha() else ch for ch in self.base_text)

    def random_cipher(self):
        enc = '~#@$%^&*_-+=?<>`"'
        return ''.join(choice([c, choice(enc)]) for c in self.base_text)
