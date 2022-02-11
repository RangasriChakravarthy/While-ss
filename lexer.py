def lexer_create(input_val):
    input_val['curr_pos'] = 0
    input_val['curr_char'] = input_val['str'][0]
    input_val['exp_len'] = len(input_val['str'])
    return


def lexer_next_char(input_val):
    input_val['curr_pos'] += 1
    if input_val['curr_pos'] >= input_val['exp_len']:
        input_val['curr_char'] = None
    else:
        input_val['curr_char'] = input_val['str'][input_val['curr_pos']]
    return


def lexer_nexttoken(input_val):
    result = ""
    while input_val['curr_pos'] < input_val['exp_len'] and not input_val['curr_char'].isspace():
        result += input_val['curr_char']
        lexer_next_char(input_val)
    if input_val['curr_char']:
        if input_val['curr_char'].isspace():
            lexer_next_char(input_val)
    return result
