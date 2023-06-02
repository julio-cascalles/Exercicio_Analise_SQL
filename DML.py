from const import (
    FLD_VALUES, ELEMENTS, FIND_TOKEN, VALID,
    PATTERN, NORMALIZE, GET_TOKENS, WHERE_INFO
)

INS_KEYWORDS = PATTERN('INSERT|INTO|VALUES')
UPD_KEYWORDS = PATTERN('UPDATE|SET|WHERE')
DEL_KEYWORDS = PATTERN('DELETE|FROM|WHERE')


def parse_insert(tokens: list, target: dict):
    import json
    table, fields, values = [
        t for t in tokens if t not in INS_KEYWORDS and VALID(t, '')
    ]
    target.setdefault(table, {}).setdefault('INSERT', []).append(
        FLD_VALUES(ELEMENTS(fields), ELEMENTS(values))
    )

def parse_update(tokens: list, target: dict):
    table = tokens[1]
    field_list = ELEMENTS(tokens[3], '=|,')
    result = [FLD_VALUES(field_list[::2], field_list[1::2])]
    found = FIND_TOKEN(tokens, 'WHERE')
    if found:
        i = found[0] + 1
        result.append(WHERE_INFO(tokens[i]))
    target.setdefault(table, {}).setdefault('UPDATE', []).extend(result)

def parse_delete(tokens: list, target: dict):
    table = tokens[2]
    result = []
    found = FIND_TOKEN(tokens, 'WHERE')
    if found:
        i = found[0] + 1
        result.append(WHERE_INFO(tokens[i]))
    target.setdefault(table, {}).setdefault('DELETE', []).extend(result)

DML_COMMANDS = {
    'INSERT': (INS_KEYWORDS + '|\(|\)', parse_insert),
    'UPDATE': (UPD_KEYWORDS, parse_update),
    'DELETE': (DEL_KEYWORDS, parse_delete),
}

def command_parser(query: str, commands: dict=DML_COMMANDS) -> dict:
    result = {}
    query = NORMALIZE(query)
    for block in query.split(';'):
        keywords = PATTERN('|'.join(commands.keys()))
        tokens = GET_TOKENS(block, keywords)
        cmd = tokens[0].upper()
        keywords, parse_func = commands[cmd]
        tokens = GET_TOKENS(block, keywords)
        parse_func(tokens, result)
    return result
