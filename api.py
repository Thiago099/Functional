from flask import Flask as fl, request as rq
import sys
sys.path.insert(1, 'bin')
sys.path.insert(1, 'functional')

from persistence import sql
import functional as fn
from sql_flask import table
import vector as vc
import json
from rest import server


api = fl(__name__)

server(api, 'functional')

@api.route('/build/<id>', methods = ['GET'])
def database(id):
    db = sql('functional')
    cmd = db.query(f'SELECT * FROM command WHERE id = {id}')[0]
    db.close()
    return  fn.build(cmd['class'],cmd['name']), 200, {'Content-Type': 'text/plain; charset=utf-8'}
api.run()