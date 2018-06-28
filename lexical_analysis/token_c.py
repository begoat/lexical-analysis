import re


class Token:
    """
    constant: int|float|scientific notation|string|character
    whitespace: \n \t \s
    keyword: { key: value }
    identifier:
    operator:
    """
    def __init__(self):
        self.whitespace_regex = re.compile('^[\s]+$')
        self.constant_regex = re.compile('^[+-]?[0-9]+$|^".*"$|^\'[a-zA-Z0-9]\'$|^[-+]?[\d]+\.?[\d]*[Ee](?:[-+]?[\d]+\.?[\d]*)$')
        self.keyword = [
            'auto', 'double', 'int', 'struct', 'break', 'else',
            'long', 'switch', 'case', 'enum', 'register', 'typedef',
            'char', 'extern', 'return', 'union', 'const', 'float',
            'short', 'unsigned', 'continue', 'for', 'signed', 'void',
            'default', 'goto', 'sizeof', 'volatile', 'do', 'if',
            'static', 'while'
        ]
        self.identifier_regex = re.compile("^[a-zA-Z_][a-zA-Z0-9_]*\Z", re.UNICODE)
        # https://stackoverflow.com/questions/5474008/regular-expression-to-confirm-whether-a-string-is-a-valid-identifier-in-python/5474290#5474290
        self.operator = {
            '+', '-', '*', '/', '%', '++', '==',
            '==', '!=', '<', '>', '>=', '<=',
            '&&', '||', '!',
            '&', '|', '^', '<<', '>>',
            '=', '+=', '-=', '*=', '/*', '%/',
            '.', '->', '~', '!~',
        }
        self.separator = [
            '[', ']', '(', ')', '{', '}', ';', ','
        ]

    def is_whitespace(self, token):
        return bool(self.whitespace_regex.match(token))

    def is_constant(self, token):
        return bool(self.constant_regex.match(token))

    def is_keyword(self, token):
        return token in self.keyword

    def is_identifier(self, token):
        return bool(token not in self.keyword and self.identifier_regex.match(token))

    def is_operator(self, token):
        return token in self.operator

    def is_separator(self, token):
        return token in self.separator

    def categorize_token(self, token):
        if self.is_whitespace(token):
            return 'whitespace'
        elif self.is_identifier(token):
            return 'identifier'
        elif self.is_keyword(token):
            return 'keyword'
        elif self.is_constant(token):
            return 'constant'
        elif self.is_operator(token):
            return 'operator'
        elif self.is_separator(token):
            return 'separator'
        else:
            return None

