import os
import json
from DDL import create_table_parser
from DML import command_parser
from DQL import query_parser

PATH_FMT = os.path.join(os.getcwd(), 'sql/tests/{}.{}')


def run(prefix: str, func: callable) -> bool:
    data, text = {}, ''
    for ext in ['json', 'sql']:
        path = PATH_FMT.format(prefix, ext)
        with open(path, 'r') as file:    
            if ext == 'json':
                data = json.load(file)
            else:
                text = file.read()
    return func(text) == data


def test_DDL():
    assert run('DDL', create_table_parser)

def test_DML():
    assert run('DML', command_parser)

def test_DQL():
    assert run('DQL', query_parser)
