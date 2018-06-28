"""
ignore the comment and string char
print line_number
locate and print the error type
"""
from lexical_analysis.token_c import Token
import os


def lexical_extract_token():
    pass


def main():
    with open(os.path.dirname(__file__) + '/demo1.c') as f:
        raw_data = f.read()
    f.close()
    index = 0
    line_number = 1
    is_single_comment = False
    is_double_comment = False
    single_quote = False
    double_quote = False
    data_length = len(raw_data)
    token_list = []
    quote_start = 0
    token = Token()
    # print('raw data', [raw_data])
    while index < data_length:
        ch = raw_data[index]
        if ch == '\n':
            line_number = line_number + 1
        ch_prev = raw_data[index - 1] if index > 1 else None
        """ ignore comments and quote
        """
        if ch == '\'' and ch_prev != '\\' and not double_quote and not is_single_comment and not is_double_comment:
            if not single_quote:
                quote_start = index
                single_quote = True
            else:
                token_list.append({
                    'token': raw_data[quote_start:index+1],
                    'category': None,
                    'line_number': line_number
                })
                single_quote = False
            index = index + 1
            continue
        elif ch == '\"' and ch_prev != '\\' and not single_quote and not is_single_comment and not is_double_comment:
            if not double_quote:
                quote_start = index
                double_quote = True
            else:
                token_list.append({
                    'token': raw_data[quote_start:index+1],
                    'category': 'constant',
                    'line_number': line_number
                })
                double_quote = False
            index = index + 1
            continue
        elif raw_data[index:index+2] in ['//', '/*'] and not is_single_comment and not is_double_comment and not single_quote and not double_quote:
            if raw_data[index:index+2] == '//':
                is_single_comment = True
            else:
                is_double_comment = True
            index = index + 2
            continue
        elif is_single_comment and ch == '\n':
            is_single_comment = False
            index = index + 1
            continue
        elif is_double_comment and raw_data[index:index+2] == '*/':
            is_double_comment = False
            index = index + 2
            continue

        """ only handle useful string
        """
        if not double_quote and not single_quote and not is_double_comment and not is_single_comment:
            offset = 1
            while True:
                # FIXME: test $ or some weird signs， how to handle error correctly
                tokenize = token.categorize_token(raw_data[index:index+offset])
                # print('tokenize', [raw_data[index:index+offset]], 'result', tokenize)
                # print('current index:', index, 'current offset', offset)
                if tokenize:
                    """ [:right boundary exceed the length is not ok]
                    """
                    if index + offset >= data_length:
                        token_list.append({
                            'token': raw_data[index:index + offset],
                            'category': token.categorize_token(raw_data[index:index + offset]),
                            'line_number': line_number
                        })
                        break
                    offset = offset + 1
                    continue
                # FIXME: still need patch for 2.0e ...
                elif raw_data[index+offset-1] == 'e':
                    """ patch for scientific notation
                    """
                    if index+offset <= data_length - 1:
                        if raw_data[index+offset] in ['+', '-']:
                            offset = offset + 3
                        elif raw_data[index+offset] in [str(i) for i in range(0, 10)]:
                            offset = offset + 2
                        continue
                """ patch for single char not match
                """
                right_boundary = index + offset - 1 if offset > 1 else index + offset
                token_list.append({
                    'token': raw_data[index:right_boundary],
                    'category': token.categorize_token(raw_data[index:right_boundary]),
                    'line_number': line_number
                })
                for character in range(1, len(raw_data[index:right_boundary])):
                    if raw_data[index:right_boundary][character] == '\n':
                        line_number = line_number + 1
                break

            if offset > 1:
                index = index + offset - 1
                continue

        index = index + 1
    for i in token_list:
        if not i['category']:
            i['category'] = token.categorize_token(i['token'])
        if i['category'] != 'whitespace':
            print(i)


if __name__ == '__main__':
    main()