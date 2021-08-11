from flask import Flask as fl, request as rq
import sys
sys.path.insert(1, 'bin')
sys.path.insert(1, 'functional')

from persistence import sql
import functional as fn
from sql import table
import vector as vc
import json
from rest import server


api = fl(__name__)

server(api, 'functional')

@api.route('/build/<id>', methods = ['GET'])
def build(id):
    db = sql('functional')
    cmd = db.query(f'SELECT * FROM command WHERE id = {id}')[0]
    db.close()
    return  fn.build(cmd['class'], cmd['name']), 200, {'Content-Type': 'text/plain; charset=utf-8'}

@api.route('/get_child/<id>', methods = ['GET'])
def get_child(id):
    db = sql('functional')
    result = db.query(f'SELECT id, child FROM sub_command WHERE parent = {id}')
    db.close()
    return  json.dumps(result), 200, {'Content-Type': 'text/json; charset=utf-8'}

api.run()