from persistence import sql
import vector as vc


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

def build(classe, name, parameter = {}):
    db = sql('functional')
    
    
    base = get_command((classe, name))

    if(not base):
        return 'command not found'
    
    scope = []

    def next(id_child, padding):
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

            cur_child = i['child']
            id = i['id']

            data = db.query(f'''
                SELECT
                    *
                FROM
                    command
                WHERE
                    id = {cur_child}
            ''')[0]

            cur = next(cur_child, padding) + data['value']
            
            parameter = db.query(f'''
                SELECT
                    *
                FROM
                    sub_command_parameter
                WHERE
                    sub_command = {id}
            ''')    
            for i in parameter:

                i['parameter'] = '{{'+i['parameter']+'}}'

            
            cur_parameter = parameter.copy()
            temp = cur
            j = 0
            spaces = 0
            start = 0
            diference = 0
            for i in range(len(cur)):
                found = False
                for k in cur_parameter:
                    if(j >= len(k['parameter'])-1):
                        cur_padding =  (' ' * (spaces))
                        command = k['command']
                        if(command):
                            base = db.query(f'''
                                SELECT
                                    *
                                FROM
                                    command
                                WHERE
                                    id = {command}
                                ''')[0]
                            value = base['value'] + next(command, cur_padding)
                        else:
                            value = k['value']

                        value = cur_padding + value.replace('\n','\n'+cur_padding)
                        temp = temp[0:start-spaces] + value + temp[i+1-diference:len(temp)]
                        diference += j + 1 - len(value)+spaces
                        found = True
                        break
                if(not found):
                    cur_parameter = [k for k in cur_parameter if k['parameter'][j] == cur[i]]
                    j += 1
                if(len(cur_parameter) == 0 or found):
                    if cur[i] == ' ':
                        spaces += 1
                    else:
                        spaces = 0
                    j = 0
                    start = i - diference + 1
                    cur_parameter = parameter.copy()

            ret += temp + '\n'

        ret = ret[0:-1]

        

        return ret

    ret = next(base['id'], '') + base['value']

    unique_scope = []
    if(type(parameter) is dict):
        for i in parameter:
            unique_scope.append({'parameter':'{{'+i+'}}','value':parameter[i]})
    else:
        count = 0
        scope = []
        i = 0
        while (i < len(ret)):
            if(ret[i] == '{'):
                count += 1
            else:
                count = 0
            if(count == 2):
                count = 0
                i += 1
                start = i
                while(i < len(ret)):
                    i += 1
                    if(ret[i] == '}'):
                        count += 1
                    else:
                        count = 0
                    if(count == 2):
                        cur = ret[start:i-1]
                        if(cur not in scope):
                            scope.append(cur)
                        count = 0
                        break
            i += 1
        for i in range(len(scope)):
            if(i >= len(parameter)):
                value = '{{'+str(i)+'}}'
            else:
                value = parameter[i]
            if({'parameter':scope[i],'value':value} not in unique_scope):
                unique_scope.append({'parameter':'{{'+scope[i]+'}}','value':value})
    cur_parameter = unique_scope.copy()

    temp = ret
    j = 0
    spaces = 0
    start = 0
    diference = 0
    for i in range(len(ret)):
        found = False
        for k in cur_parameter:
            if(j >= len(k['parameter'])-1):
                cur_padding =  (' ' * (spaces))
                if(type(k['value']) is tuple):
                    command = get_command(k['value'])
                    value = next(command['id'], scope, '') + command['value']
                else:
                    if(type(k['value']) is list):
                        value = vc.cat(k['value'])
                    else:
                        value = k['value']
                value = cur_padding + value.replace('\n','\n'+cur_padding)
                temp = temp[0:start-spaces] + value + temp[i+1-diference:len(temp)]
                diference += j + 1 - len(value) + spaces
                found = True
                break
        if(not found):
            cur_parameter = [k for k in cur_parameter if k['parameter'][j] == ret[i]]
            j += 1
        if(len(cur_parameter) == 0 or found):
            if ret[i] == ' ':
                spaces += 1
            else:
                spaces = 0
            j = 0
            start = i - diference + 1
            cur_parameter = unique_scope.copy()
    ret = temp
    
    db.close()
    return ret

def create_command(classe, name, value = '',  _parameter = []):
    db = sql('functional')
    id = db.run(build('sql','insert values',
    {
        'table': 'command',
        'field': [',\n', 'class', 'name', 'value'],
        'value':  f"'{classe}', '{name}', '{value}'"
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
    id = db.run(build('sql','insert values',
    {
        'table': 'sub_command',
        'field': [',\n','parent', 'child'],
        'value': f"'{parent['id']}', '{child['id']}'"
    }))    
   
    if(parameter):
        for i in parameter:
            com = '\''
            db.run(build('sql','insert values',{
                'table': 'sub_command_parameter',
                'field': [',\n', 'sub_command', 'parameter', 'value', 'command'],
                'value': f"{id}, '{i}', {('null, '+ com + str(get_command(parameter[i])['id']) + com) if type(parameter[i]) is tuple else (com + (vc.cat(parameter[i]) if type(parameter[i]) is list else parameter[i]) + com + ', null')}"
            }))
    
    db.close()

