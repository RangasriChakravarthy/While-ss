from ast import *


def sswhile_statement_parser(input_val):
    result = ""
    cur_token = get_curr_token(input_val)
    if cur_token == 'skip':
        input_val['commands_pos'] += 1
        if get_curr_token(input_val) == ";":
            input_val['commands_pos'] += 1
    elif cur_token == 'if':
        if_pos = input_val['commands_pos']
        input_val['commands_pos'] += 1
        expr_cond = sswhile_expr(input_val)
        input_val['commands_pos'] += 1
        then_st = sswhile_brace_parse(input_val)
        input_val['commands_pos'] += 1
        else_st = sswhile_brace_parse(input_val)
        input_val['sub_command'][if_pos] = {}
        input_val['sub_command'][if_pos]['then'] = then_st
        input_val['sub_command'][if_pos]['else'] = else_st
        result = "if" + " " + expr_cond + " then { " + "; ".join(then_st) + " } else { " + "; ".join(else_st) + " }"
    elif cur_token == 'while':
        while_pos = input_val['commands_pos']
        input_val['commands_pos'] += 1
        expr_cond = sswhile_expr(input_val)
        input_val['commands_pos'] += 1
        do_st = sswhile_brace_parse(input_val)
        result = "while " + expr_cond + " do { " + "; ".join(do_st) + " }"
        input_val['sub_command'][while_pos] = do_st
    else:
        temp = get_curr_token(input_val)
        input_val['commands_pos'] += 1
        oper = get_curr_token(input_val)
        input_val['commands_pos'] += 1
        assert oper == ":="
        result = temp + " " + oper + " " + sswhile_expr(input_val)
        if get_curr_token(input_val) == ";":
            input_val['commands_pos'] += 1
    return result


def get_curr_token(input_val):
    if input_val['commands_pos'] < len(input_val['token']):
        return input_val['token'][input_val['commands_pos']]


def sswhile_brace_parse(input_val):
    res = list()
    curr_token = get_curr_token(input_val)
    if curr_token == LBRACE:
        input_val['commands_pos'] += 1
        while get_curr_token(input_val) != RBRACE:
            temp = sswhile_statement_parser(input_val)
            if temp:
                res.append(temp)
        input_val['commands_pos'] += 1
    else:
        temp = sswhile_statement_parser(input_val)
        if temp:
            res.append(temp)
    if get_curr_token(input_val) == ";":
        input_val['commands_pos'] += 1
    return res


def sswhile_num(input_val):
    res = ""
    token = get_curr_token(input_val)
    if token.lstrip('-+').isdigit():
        res = str(int(increment_token(input_val)))
    elif token == LPAREN:
        input_val['commands_pos'] += 1
        res = sswhile_expr(input_val)
        input_val['commands_pos'] += 1
    elif token in ("true", "false"):
        res = increment_token(input_val)
    elif token == NOT:
        res = increment_token(input_val) + sswhile_expr(input_val)
    else:
        res = increment_token(input_val)
    return res


def sswhile_oper(input_val):
    res = ""
    temp = sswhile_num(input_val)
    while get_curr_token(input_val) in (ADD, SUB, MUL, DIV, MOD, EQUAL, LESS, GREAT):
        token = increment_token(input_val)
        res = "(" + temp + token + sswhile_num(input_val) + ")"
        temp = res
        res = ""
    if not res:
        res = temp
    return res


def sswhile_expr(input_val):
    res = ""
    temp = sswhile_oper(input_val)
    while get_curr_token(input_val) in (AND, OR):
        token = increment_token(input_val)
        res = "(" + temp + token + sswhile_oper(input_val) + ")"
        temp = res
        res = ""
    if not res:
        res = temp
    return res


def increment_token(input_val):
    res = input_val['token'][input_val['commands_pos']]
    input_val['commands_pos'] += 1
    return res
