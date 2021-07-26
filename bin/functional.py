from persistence import sql

def get_command(command):
    db = sql('functional')
    classe, name = command
    result = db.query(f'''
        SELECT
            *
        FROM
            command
        WHERE
            class = '{classe}'
        AND
            name = '{name}'
    ''')
    if(len(result) == 0):
        return False
    db.close()
    return result[0]

def build(classe, name, parameter = None):
    db = sql('functional')
    
    
    base = get_command((classe, name))

    if(not base):
        return 'command not found'
    def next(id_child):
        child = db.query(f'''
            SELECT
                *
            FROM
                sub_command
            WHERE
                parent = {id_child}
        ''')
        
        ret = ''
        for i in child:

            child = i['child']
            id = i['id']

            data = db.query(f'''
                SELECT
                    *
                FROM
                    command
                WHERE
                    id = {child}
            ''')[0]

            cur = next(child) + data['value']

            
            parameter = db.query(f'''
                SELECT
                    *
                FROM
                    sub_command_parameter
                WHERE
                    sub_command = {id}
            ''')

            for i in parameter:
                command = i['command']
                if(command):
                    base = db.query(f'''
                        SELECT
                            *
                        FROM
                            command
                        WHERE
                            id = {command}
                        ''')[0]
                    cur = cur.replace('{{'+i['parameter']+'}}', base['value'] + next(command))
                else:
                    cur = cur.replace('{{'+i['parameter']+'}}', i['value'])

            ret += cur + '\n'
        return ret
    
    ret = next(base['id']) + base['value']

    if(parameter):
        for i in parameter:
            if(type(parameter[i]) is tuple):
                command = get_command(parameter[i])
                ret = ret.replace('{{'+i+'}}', next(command['id']) + command['value'])
            else:
                ret = ret.replace('{{'+i+'}}', parameter[i])
    db.close()
    return ret

def create_command(classe, name, value = ''):
    db = sql('functional')
    db.run(build('sql','insert into',
    {
        'table':'command',
        'field':'class, name, value',
        'value': f"'{classe}', '{name}', '{value}'"
    }))    
    db.close()

def set_child(command, child, parameter = None):
    parent = get_command(command)
    child = get_command(child)
    error = False

    if(not parent):
        error = "parent"

    if(not child):
        if(not parent):
            error += ", "
        error += 'child'

    if(error):
        return error + ' command not found'
    db = sql('functional')
    id = db.run(build('sql','insert into',
    {
        'table': 'sub_command',
        'field': 'parent, child',
        'value': f"'{parent['id']}', '{child['id']}'"
    }))    
    if(parameter):
        for i in parameter:
            if(type(parameter[i]) is tuple):
                db.run(build('sql','insert into',{
                    'table': 'sub_command_parameter',
                    'field': 'sub_command, parameter, value, command',
                    'value': f"{id}, '{i}', null, {get_command(parameter[i])['id']}"
                }))
            else:
                db.run(build('sql','insert into',{
                    'table': 'sub_command_parameter',
                    'field': 'sub_command, parameter, value, command',
                    'value': f"{id}, '{i}', '{parameter[i]}', null"
                }))
    db.close()