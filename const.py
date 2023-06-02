import re

CLEAN_STR = lambda txt: re.sub('\(|\)', '', txt.strip())
NORMALIZE = lambda txt: re.sub(' +', ' ', re.sub('\n|\t', ' ', txt))
ELEMENTS = lambda expr, sep=',': [f.strip() for f in re.split(sep, expr) if f]
FLD_VALUES = lambda fields, values: {
    f.strip(): eval(CLEAN_STR(v)) for f, v in zip(fields, values)
}
FIND_TOKEN = lambda tokens, search: [i for i, t in enumerate(tokens) if t.upper() == search]
PATTERN = lambda txt: f'{txt}|{txt.lower()}'
VALID = lambda txt, sep='\(\),/\*': re.findall(f'[A-Za-z1-9{sep}]', txt)
GET_TOKENS = lambda block, keywords: [
    t.strip() for t in re.split(f'({keywords})', block) if VALID(t)
]
LOGICAL_SEPARATORS = PATTERN('AND|OR')
WHERE_INFO = lambda expr: {'WHERE': GET_TOKENS(expr, LOGICAL_SEPARATORS)}