from flask import Flask as fl, request as rq
import sys
sys.path.insert(1, '../functional')

from persistence import sql
import functional as fn
from sql import table
import vector as vc
import json

def get_tables(schema):
    db = sql('information_schema')
    ret = db.query(f'SELECT TABLE_NAME FROM TABLES WHERE TABLE_SCHEMA = \'{schema}\'')
    db.close()
    return ret

def server(api, schema):
    for i in get_tables(schema):
        exec(fn.build('flask', 'crud', [i['TABLE_NAME'], schema]))
    