from lexer import *


def parser_create(input_val):
    input_val['token'] = list()
    while input_val['curr_pos'] < input_val['exp_len']:
        cur_token = lexer_nexttoken(input_val)
        input_val['token'].append(cur_token)
    input_val['token_pos'] = 0
    input_val['curr_token'] = parser_gettoken(input_val, 0)
    return


def parser_gettoken(cache, pos):
    return cache['token'][pos]


def parser_settoken(cache, pos):
    cache['token_pos'] = pos
    cache['curr_token'] = parser_gettoken(cache, pos)
    return


def parser_move(cache):
    rv = cache['curr_token']
    parser_eat(cache)
    return rv


def parser_eat(cache):
    cache['token_pos'] += 1
    if cache['token_pos'] < len(cache['token']):
        cache['curr_token'] = parser_gettoken(cache, cache['token_pos'])
    return


def while_parse(cache):
    total = len(cache['token'])
    start = 0
    s = ""
    while start < total:
        if ((cache['token'][start] == "while") or (cache['token'][start] == "do") or
                (cache['token'][start] == "if") or (cache['token'][start] == "else") or
                (cache['token'][start] == "then")):
            s += cache['token'][start] + " "
        else:
            s += cache['token'][start]
        start = start + 1
    return
