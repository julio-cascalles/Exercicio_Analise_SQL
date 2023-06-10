from const import (
    LOGICAL_SEPARATORS, ELEMENTS,
    NORMALIZE, GET_TOKENS,
)

KEYWORDS = 'SELECT|FROM|WHERE|GROUP BY|ORDER BY'
NESTED = {
    'WHERE': LOGICAL_SEPARATORS,
    'FROM': 'TABLE|JOIN'
}
LOWER_OPERATORS = 'not|like|in|on|left|right'.split('|')


def query_parser(query: str, keywords=None) -> dict:
    def fmt_operators(item: str) -> str:
        if item in LOWER_OPERATORS:
            item = item.upper()
        return item
    if not keywords:
        keywords = KEYWORDS
        query = NORMALIZE(query)
    tokens = GET_TOKENS(query, keywords)
    result = {}
    for k, v in zip(tokens[::2], tokens[1::2]):
        k = k.upper()
        if k in NESTED:
            result[k] = query_parser('{} {}'.format(
                NESTED[k].split('|')[0], v
            ), keywords=NESTED[k])
        else:
            v = list(map(fmt_operators, ELEMENTS(v, ' |,')))
            if k in ['AND', 'OR', 'JOIN']:
                result.setdefault(k, []).append(v)
            else:
                result[k] = v
    return result
