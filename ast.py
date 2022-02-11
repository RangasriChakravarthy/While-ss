from parser import *

ADD, SUB, MUL, DIV, MOD, LPAREN, RPAREN, GREAT, LESS, EQUAL, NOT, AND, OR, LBRACE, RBRACE = ('+', '-', '*', '/', '%',
                                                                                             '(', ')', '>', '<', '=',
                                                                                             '¬', '∧', '∨', '{', '}')
IF, WHILE, VAR = ('if', 'while', 'variable')

NUMBER, BINOP, UNARYOP = ('INTEGER', 'BINARY', 'UNARY')


def ast_num(input_val):
    res = {}
    token = input_val['curr_token']
    if token.lstrip('-+').isdigit():
        res['type'] = NUMBER
        res['val'] = int(parser_move(input_val))
    elif token == LPAREN:
        parser_move(input_val)
        res = ast_expr(input_val)
        parser_move(input_val)
    elif token == NOT:
        res['type'] = UNARYOP
        res['oper'] = parser_move(input_val)
        res['left'] = ast_expr(input_val)
    elif token in ("true", "false"):
        res['type'] = NUMBER
        res['val'] = (token == "true")
        parser_move(input_val)
    else:
        res['type'] = UNARYOP
        res['oper'] = VAR
        res['left'] = token
        parser_eat(input_val)

    return res


def ast_oper(input_val):
    res = {}
    temp = ast_num(input_val)
    while input_val['curr_token'] in (ADD, SUB, MUL, DIV, MOD, EQUAL, LESS, GREAT):
        token = parser_move(input_val)
        res['left'] = temp
        res['oper'] = token
        res['right'] = ast_num(input_val)
        res['type'] = BINOP
        temp = res
        res = {}
    if not res:
        res = temp

    return res


def ast_expr(input_val):
    res = {}
    temp = ast_oper(input_val)
    while input_val['curr_token'] in (AND, OR):
        token = parser_move(input_val)
        res['left'] = temp
        res['oper'] = token
        res['right'] = ast_oper(input_val)
        res['type'] = BINOP
        temp = res
        res = {}
    if not res:
        res = temp

    return res
