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
    while index < data_length:
        # FIXME: line number error because of /* \n*/
        ch = raw_data[index]
        ch_prev = raw_data[index - 1] if index > 1 else None
        """ ignore comments and quote
        """
        if ch == '\'' and ch_prev != '\\' and not double_quote:
            if not single_quote:
                quote_start = index
                single_quote = True
            else:
                token_list.append({
                    'token': raw_data[quote_start:index+1],
                    'category': None
                })
                single_quote = False
            index = index + 1
            continue
        elif ch == '\"' and ch_prev != '\\' and not single_quote:
            if not double_quote:
                quote_start = index
                double_quote = True
            else:
                token_list.append({
                    'token': raw_data[quote_start:index+1],
                    'category': 'constant'
                })
                double_quote = False
            index = index + 1
            continue
        elif raw_data[index:index+2] in ['//', '/*'] and not is_single_comment and not is_double_comment:
            if raw_data[index:index+2] == '//':
                is_single_comment = True
            else:
                is_double_comment = True
            index = index + 2
            continue
        elif is_single_comment and ch == '\n':
            is_single_comment = False
            index = index + 1
            line_number = line_number + 1
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
                # FIXME: for loop regex may broke. 2e is invalid but 2e1 is valid and is what we want, maybe need a patch for this case
                # FIXME: test $ or some weird signs， how to handle error correctly
                tokenize = token.categorize_token(raw_data[index:index+offset])
                # print('tokenize', [raw_data[index:index+offset]], 'result', tokenize)
                if index + offset >= data_length:
                    break
                if tokenize:
                    offset = offset + 1
                    continue
                token_list.append({
                    'token': [raw_data[index:index+offset-1]],
                    'category': token.categorize_token(raw_data[index:index+offset-1])
                })
                break

            if index + offset - 1 < data_length - 1:
                index = index + offset - 1
                continue

        index = index + 1
    # print('line_number', line_number)
    for i in token_list:
        if not i['category']:
            i['category'] = token.categorize_token(i['token'])
        if i['category'] != 'whitespace':
            print(i)


if __name__ == '__main__':
    main()