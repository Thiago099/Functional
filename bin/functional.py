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

def build(classe, name, parameter = []):
    db = sql('functional')
    
    
    base = get_command((classe, name))

    if(not base):
        return 'command not found'
    
    scope = set()

    def next(id_child, scope):
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

            

            cur = next(child, scope) + data['value']

            
            parameter = db.query(f'''
                SELECT
                    *
                FROM
                    sub_command_parameter
                WHERE
                    sub_command = {id}
            ''')    

            for i in parameter:

                if i['parameter'] in scope:
                    scope.remove(i['parameter'])
                
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
                    cur = cur.replace('{{'+i['parameter']+'}}', base['value'] + next(command, scope))
                else:
                    cur = cur.replace('{{'+i['parameter']+'}}', i['value'])

            ret += cur + '\n'
        command_parameter = db.query(f'''
            SELECT
                *
            FROM
                command_parameter
            WHERE
                command = {id_child}
        ''')

        for i in command_parameter:
            scope.add(i['parameter'])
        return ret
    
    ret = next(base['id'], scope) + base['value']
    if(type(parameter) is dict):
        for i in parameter:
            if(type(parameter[i]) is tuple):
                command = get_command(parameter[i])
                ret = ret.replace('{{'+i+'}}', next(command['id']) + command['value'], scope)
            else:
                ret = ret.replace('{{'+i+'}}', parameter[i])
    else:
        scope = list(scope)
        for i in range(len(scope)):
                if(i >= len(parameter)):
                    ret = ret.replace('{{'+scope[i]+'}}', '{{'+str(i)+'}}')
                else:
                    if(type(parameter[i]) is tuple):
                        command = get_command(parameter[i])
                        ret = ret.replace('{{'+scope[i]+'}}', next(command['id']) + command['value'], scope)
                    else:
                        ret = ret.replace('{{'+scope[i]+'}}', parameter[i])
    db.close()
    return ret

def create_command(classe, name, value = '', parameter = None):
    db = sql('functional')
    id = db.run(build('sql','insert into',
    {
        'table': 'command',
        'field': 'class, name, value',
        'value':  f"'{classe}', '{name}', '{value}'"
    }))    
    if(parameter):
        for i in parameter:
            db.run(build('sql','insert into',{
                'table':'command_parameter',
                'field':'command, parameter',
                'value': f"{id}, {i}"
            }))
    db.close()

def set_child(command, child, parameter = None, new_parameter = None):
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
            db.run(build('sql','insert into',{
                'table': 'sub_command_parameter',
                'field': 'sub_command, parameter, value, command',
                'value': f"{id}, '{i}', null, {get_command(parameter[i])['id'] if type(parameter[i]) is tuple else parameter[i]}"
            }))
    
    db.close()