from const import (
    NORMALIZE, ELEMENTS, GET_TOKENS
)


AUTO_INC_BY_DATABASES = {
    'IDENTITY': 'MS Sql Server',
    'AUTO_INCREMENT': 'mySql',
    'SERIAL': 'PostgreSql'
}
FIELD_TYPES = 'INTEGER|VARCHAR|CHAR|DATE|FLOAT'
AUTO_INC_TYPES = '|'.join(AUTO_INC_BY_DATABASES.keys())
RELATIONS = 'FOREIGN KEY|REFERENCES'
CONSTRAINTS = 'PRIMARY KEY|NOT NULL|UNIQUE' + '|' + RELATIONS
KEYWORDS = f'{FIELD_TYPES}|{CONSTRAINTS}|{AUTO_INC_TYPES}|\(|,|\)|/\*|\*/'
TO_LIST = lambda types: '{}|{}'.format(types, types.lower()).split('|')


def create_table_parser(query: str) -> dict:
    result = {}
    query = NORMALIZE(query)
    for block in ELEMENTS(query, 'CREATE TABLE'):
        tokens = GET_TOKENS(block, KEYWORDS)
        info, fk_table = {}, False
        table, field = '', ''
        level, params = 0, []
        last_token, comment = '', False
        while tokens:
            token = tokens.pop(0)
            if token == "/*":
                comment = True
            if comment:
                if token == "*/":
                    comment = False
                continue
            match token:
                case "(":
                    if level == 0:
                        if not table:
                            table = last_token
                    elif fk_table:
                        info['fk_table'] = last_token
                    level += 1
                case ",":
                    if level > 1:
                        params.append(last_token)
                    else:
                        result.setdefault(table, {})[field] = info
                        field, params = '', []
                        info, fk_table = {}, False
                case ")":
                    if level > 1:
                        params.append(last_token)
                        info['params'] = params
                    else:
                        result.setdefault(table, {})[field] = info
                    level -= 1           
            if token in TO_LIST(FIELD_TYPES):
                info['type'] = token.upper()
                field = last_token
            elif token in TO_LIST(AUTO_INC_TYPES):
                info['auto_inc'] = True
                info['auto_inc_type'] = AUTO_INC_BY_DATABASES[token.upper()]
            elif token in TO_LIST(CONSTRAINTS):
                if token in TO_LIST(RELATIONS):
                    fk_table = True
                info.setdefault('constraints', []).append(token.upper())
            last_token = token
    return result
