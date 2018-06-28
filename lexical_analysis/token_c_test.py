import unittest
from lexical_analysis.token_c import Token


class TokenTest(unittest.TestCase):
    def setUp(self):
        self.token = Token()

    def test_whitespace(self):
        true_list = [
            ' ', '   ', '  ', '\t', '\n', '\t ', '\t   ', '\t      ', '\n '
        ]
        false_list = [
            ' s \n s ', 'sd sdasd\n\s', '\t     s', 's', ' (', '人'
        ]
        for i in true_list:
            self.assertEqual(True, self.token.is_whitespace(i))
        for i in false_list:
            self.assertEqual(False, self.token.is_whitespace(i))

    def test_constant(self):
        """
        constant: int|float|scientific notation|string|character
        :return:
        """
        true_list = [
            '1e+1.0', '+1.0e+1.0', '-1.0e-1.0', '1e+10', '1e+1.0', '1e+10.0',
            '1.0e+10', '\"I AM A TESTSTRING\"', '\'s\'', '+2e1'
        ] + [str(i) for i in range(-100000, 100000)]
        false_list = [
            '???', 'test', '\'test\'', 's1e+1.0', '1e+1.0s', '+2e-1\n', '+2e1\n'
        ]
        # TODO: float test case
        for i in true_list:
            self.assertEqual(True, self.token.is_constant(i))
        for i in false_list:
            self.assertEqual(False, self.token.is_constant(i))

    def test_identifier(self):
        true_list = [
            '_123', '_asd123', 'AaC123', 'AC_123'
        ]
        false_list = [
            '123sd', 'if', 'sizeof', 'printf\n', 'aa$%@%', 'aa bb', '人', '。', '。'
        ]
        for i in true_list:
            self.assertEqual(True, self.token.is_identifier(i))
        for i in false_list:
            self.assertEqual(False, self.token.is_identifier(i))

    def test_keyword(self):
        true_list = [
            'auto', 'double', 'int', 'struct', 'break', 'else',
            'long', 'switch', 'case', 'enum', 'register', 'typedef',
            'char', 'extern', 'return', 'union', 'const', 'float',
            'short', 'unsigned', 'continue', 'for', 'signed', 'void',
            'default', 'goto', 'sizeof', 'volatile', 'do', 'if',
            'static', 'while'
        ]
        false_list = [
            'test', 'test2', '_test1213'
        ]
        for i in true_list:
            self.assertEqual(True, self.token.is_keyword(i))
        for i in false_list:
            self.assertEqual(False, self.token.is_keyword(i))

    def test_operator(self):
        true_list = [
            '+', '-', '*', '==', '!=', '<', '&', '&&',
        ]
        false_list = [
            '?'
        ]
        for i in true_list:
            self.assertEqual(True, self.token.is_operator(i))
        for i in false_list:
            self.assertEqual(False, self.token.is_operator(i))

    def test_categorize_token(self):
        self.assertEqual('operator', self.token.categorize_token('='))
        self.assertEqual('keyword', self.token.categorize_token('if'))
        self.assertEqual('keyword', self.token.categorize_token('int'))
        self.assertEqual(None, self.token.categorize_token('int '))
        self.assertEqual(None, self.token.categorize_token('?'))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
