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
    while index < data_length:
        # FIXME: line number miss understanding when use /* \n*/
        ch = raw_data[index]
        ch_prev = raw_data[index - 1] if index > 1 else None
        # ch_next = raw_data[index + 1] if index < data_length -1 else None
        # TODO: ignore comment and quote
        print('current ch is', [ch])
        if ch == '\'' and ch_prev != '\\':
            if not single_quote:
                single_quote = True
            else:
                single_quote = False
            index = index + 1
            continue
        elif ch == '\"' and ch_prev != '\\':
            if not double_quote:
                double_quote = True
            else:
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

        if not double_quote and not single_quote and not is_double_comment and not is_single_comment:
            token = Token()
            offset = 1
            while True:
                # TODO test $ or some weird sign
                # TODO: avoid the overflow of the raw_data
                tokenize = token.categorize_token(raw_data[index:index+offset])
                # print('tokenize', [raw_data[index:index+offset]], 'result', tokenize)
                if index + offset >= data_length:
                    break
                if tokenize:
                    offset = offset + 1
                    continue
                print('token', [raw_data[index:index+offset-1]], end='')
                break

            # if index + offset - 1 <= data_length - 1:
            #     break
            if index + offset - 1 < data_length - 1:
                index = index + offset - 1
                continue

        index = index + 1
    # print('line_number', line_number)
    # TODO: lexical_extract_token()
    # print(raw_data)


if __name__ == '__main__':
    main()