from ast import *

ASSIGN, IF_THEN, IF_ELSE, WHILE_TT, WHILE_FF = ('ASSIGN', 'IF_THEN', 'IF_ELSE', 'WHILE_TRUE', 'WHILE_FALSE')


def interpreter_create(input_val):
    while input_val['token_pos'] < len(input_val['token']):
        brace_parse(input_val)
    return


def statement_parser(input_val, res=True):
    curr_token = input_val['curr_token']
    if curr_token == 'skip':
        parser_eat(input_val)
        if input_val['curr_token'] == ";":
            parser_eat(input_val)
    elif curr_token == 'if':
        if_pos = input_val['token_pos']
        parser_eat(input_val)
        expr_cond = ast_expr(input_val)
        evaluate_cond = interpreter_eval(input_val, expr_cond)
        then_cond = res
        else_cond = res
        if evaluate_cond:
            interpreter_print(input_val, IF_THEN, if_pos)
        else:
            interpreter_print(input_val, IF_ELSE, if_pos)
        if res:
            then_cond = evaluate_cond
            else_cond = not evaluate_cond
        parser_eat(input_val)
        brace_parse(input_val, then_cond)
        parser_eat(input_val)
        brace_parse(input_val, else_cond)
    elif curr_token == 'while':
        while_pos = input_val['token_pos']
        parser_eat(input_val)
        expr_cond = ast_expr(input_val)
        parser_eat(input_val)
        b_pos = input_val['token_pos']
        while interpreter_eval(input_val, expr_cond) and res and input_val['steps'] < 10000:
            interpreter_print(input_val, WHILE_TT, while_pos)
            brace_parse(input_val)
            parser_settoken(input_val, b_pos)
        if res:
            interpreter_print(input_val, WHILE_FF, while_pos)
        brace_parse(input_val, False)
    else:
        var = parser_move(input_val)
        oper = parser_move(input_val)
        assert oper == ":="
        ans = ast_expr(input_val)
        val = interpreter_eval(input_val, ans)
        if res:
            input_val['results'][var] = val
            interpreter_print(input_val, ASSIGN)
        if input_val['curr_token'] == ";":
            parser_eat(input_val)
    return


def brace_parse(input_val, res=True):
    curr_token = input_val['curr_token']
    if curr_token == LBRACE:
        parser_eat(input_val)
        while input_val['curr_token'] != RBRACE:
            statement_parser(input_val, res)
        parser_eat(input_val)
    else:
        statement_parser(input_val, res)
    if input_val['curr_token'] == ";":
        parser_eat(input_val)
    return


def interpreter_eval(input_val, node):
    result = None
    if node['type'] == NUMBER:
        result = node['val']
    elif node['type'] == UNARYOP:
        oper = node['oper']
        if oper == NOT:
            return not interpreter_eval(input_val, node['left'])
        elif oper == VAR:
            result = 0
            if node['left'] in input_val['results']:
                result = input_val['results'][node['left']]
    elif node['type'] == BINOP:
        result = interpreter_binary(input_val, node)
    return result


def interpreter_binary(input_val, node):
    oper = node['oper']
    result = None
    if oper == ADD:
        return interpreter_eval(input_val, node['left']) + interpreter_eval(input_val, node['right'])
    elif oper == SUB:
        return interpreter_eval(input_val, node['left']) - interpreter_eval(input_val, node['right'])
    elif oper == MUL:
        return interpreter_eval(input_val, node['left']) * interpreter_eval(input_val, node['right'])
    elif oper == DIV:
        return interpreter_eval(input_val, node['left']) / interpreter_eval(input_val, node['right'])
    elif oper == MOD:
        return interpreter_eval(input_val, node['left']) % interpreter_eval(input_val, node['right'])
    elif oper == EQUAL:
        return interpreter_eval(input_val, node['left']) == interpreter_eval(input_val, node['right'])
    elif oper == LESS:
        return interpreter_eval(input_val, node['left']) < interpreter_eval(input_val, node['right'])
    elif oper == GREAT:
        return interpreter_eval(input_val, node['left']) > interpreter_eval(input_val, node['right'])
    elif oper == AND:
        return interpreter_eval(input_val, node['left']) & interpreter_eval(input_val, node['right'])
    elif oper == OR:
        return interpreter_eval(input_val, node['left']) | interpreter_eval(input_val, node['right'])
    return result


def interpreter_print(input_val, cmd, pos=None):
    temp = "{"
    temp += ", ".join(
        list(map(lambda k: "{} → {}".format(k, input_val['results'][k]), sorted(input_val['results'].keys()))))
    temp += "}"
    str_end = ", " + temp
    if input_val['steps'] >= 10000 or not input_val['command']:
        return
    if cmd == ASSIGN:
        input_val['command'].pop(0)
        str_body = "; ".join(['skip'] + input_val['command'])
        input_val['steps'] += 1
        print("⇒ " + str_body + str_end)
    elif cmd == IF_THEN:
        input_val['command'].pop(0)
        sub_command = input_val['sub_command'][pos]['then']
        input_val['command'] = sub_command + input_val['command']
    elif cmd == IF_ELSE:
        input_val['command'].pop(0)
        sub_command = input_val['sub_command'][pos]['else']
        input_val['command'] = sub_command + input_val['command']
    elif cmd == WHILE_TT:
        sub_command = input_val['sub_command'][pos]
        input_val['command'] = sub_command + input_val['command']
    elif cmd == WHILE_FF:
        input_val['command'].pop(0)
        str_body = "; ".join(['skip'] + input_val['command'])
        input_val['steps'] += 1
        print("⇒ " + str_body + str_end)

    if input_val['command']:
        input_val['steps'] += 1
        str_body = "; ".join(input_val['command'])
        print("⇒ " + str_body + str_end)
    return
