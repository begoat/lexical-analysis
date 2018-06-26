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
    is_single_comment = False
    is_double_comment = False
    single_quote = False
    double_quote = False
    for index in range(len(raw_data)):
        ch = raw_data[index]
        ch_prev = raw_data[index - 1] if index > 1 else None
        # TODO: ignore comment and quote
        if ch == '\'' and ch_prev != '\\':
            if not single_quote:
                single_quote = True
            else:
                single_quote = False
            continue
        elif ch == '\"' and ch_prev != '\\':
            if not double_quote:
                double_quote = True
            else:
                double_quote = False
            continue
        if not double_quote and not single_quote:
            print(ch, end='')

    # TODO: lexical_extract_token()
    # print(raw_data)


if __name__ == '__main__':
    main()