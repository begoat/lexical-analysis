"""
ignore the comment and string char
print line_number
locate and print the error type
constant: int|float|scientific notation|string|character
whitespace: \n \t \s
keyword: { key: value }
identifier:
operator:
"""


def lexical_extract_token():
    pass


def main():
    with open('./demo1.c') as f:
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
        # TODO: ignore comment and quote
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

        index = index + 1
        if not double_quote and not single_quote and not is_double_comment and not is_single_comment:
            print(ch, end='')

    # print('line_number', line_number)
    # TODO: lexical_extract_token()
    # print(raw_data)


if __name__ == '__main__':
    main()