from flask import Flask as fl, request as rq
import sys
sys.path.insert(1, '../functional')

from persistence import sql
import functional as fn
from sql_flask import table
import vector as vc
import json

def server(database):
    global api
    api = fl(__name__)
    db = sql('information_schema')
    for i in db.query(f'SELECT TABLE_NAME FROM TABLES WHERE TABLE_SCHEMA = \'{database}\''):
        exec(fn.build('flask', 'crud', [i['TABLE_NAME'], database]))
    db.close()
    api.run()