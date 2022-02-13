from ast import *


def commands_statement_parser(input_val):
    result = ""
    cur_token = get_curr_token(input_val)
    if cur_token == 'skip':
        input_val['commands_pos'] += 1
        if get_curr_token(input_val) == ";":
            input_val['commands_pos'] += 1
    elif cur_token == 'if':
        if_pos = input_val['commands_pos']
        input_val['commands_pos'] += 1
        expr_cond = commands_expr(input_val)
        input_val['commands_pos'] += 1
        then_st = commands_brace_parse(input_val)
        input_val['commands_pos'] += 1
        else_st = commands_brace_parse(input_val)
        input_val['sub_command'][if_pos] = {}
        input_val['sub_command'][if_pos]['then'] = then_st
        input_val['sub_command'][if_pos]['else'] = else_st
        result = "if" + " " + expr_cond + " then { " + "; ".join(then_st) + " } else { " + "; ".join(else_st) + " }"
    elif cur_token == 'while':
        while_pos = input_val['commands_pos']
        input_val['commands_pos'] += 1
        expr_cond = commands_expr(input_val)
        input_val['commands_pos'] += 1
        do_st = commands_brace_parse(input_val)
        result = "while " + expr_cond + " do { " + "; ".join(do_st) + " }"
        input_val['sub_command'][while_pos] = do_st
    else:
        temp = get_curr_token(input_val)
        input_val['commands_pos'] += 1
        oper = get_curr_token(input_val)
        input_val['commands_pos'] += 1
        assert oper == ":="
        result = temp + " " + oper + " " + commands_expr(input_val)
        if get_curr_token(input_val) == ";":
            input_val['commands_pos'] += 1
    return result


def get_curr_token(input_val):
    if input_val['commands_pos'] < len(input_val['token']):
        return input_val['token'][input_val['commands_pos']]


def commands_brace_parse(input_val):
    res = list()
    curr_token = get_curr_token(input_val)
    if curr_token == LBRACE:
        input_val['commands_pos'] += 1
        while get_curr_token(input_val) != RBRACE:
            temp = commands_statement_parser(input_val)
            if temp:
                res.append(temp)
        input_val['commands_pos'] += 1
    else:
        temp = commands_statement_parser(input_val)
        if temp:
            res.append(temp)
    if get_curr_token(input_val) == ";":
        input_val['commands_pos'] += 1
    return res


def commands_num(input_val):
    res = ""
    token = get_curr_token(input_val)
    if token.lstrip('-+').isdigit():
        res = str(int(increment_token(input_val)))
    elif token == LPAREN:
        input_val['commands_pos'] += 1
        res = commands_expr(input_val)
        input_val['commands_pos'] += 1
    elif token in ("true", "false"):
        res = increment_token(input_val)
    elif token == NOT:
        res = increment_token(input_val) + commands_expr(input_val)
    else:
        res = increment_token(input_val)
    return res


def commands_oper(input_val):
    res = ""
    temp = commands_num(input_val)
    while get_curr_token(input_val) in (ADD, SUB, MUL, DIV, MOD, EQUAL, LESS, GREAT):
        token = increment_token(input_val)
        res = "(" + temp + token + commands_num(input_val) + ")"
        temp = res
        res = ""
    if not res:
        res = temp
    return res


def commands_expr(input_val):
    res = ""
    temp = commands_oper(input_val)
    while get_curr_token(input_val) in (AND, OR):
        token = increment_token(input_val)
        res = "(" + temp + token + commands_oper(input_val) + ")"
        temp = res
        res = ""
    if not res:
        res = temp
    return res


def increment_token(input_val):
    res = input_val['token'][input_val['commands_pos']]
    input_val['commands_pos'] += 1
    return res
