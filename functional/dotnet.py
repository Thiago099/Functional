import sys
sys.path.insert(1, 'bin')
sys.path.insert(1, 'functional')

import functional as fn
from sql import table
from persistence import sql
import vector as vc
import os.path as op
import color as c

def block( name, block):
        return fn.build('programming','decorated block', [name, block])

def return_block(name, block):
    return fn.build('dotnet','return block', [name, block])


def classe(using, namespace, name, menbers):
    return vc.cat(['\n']+[f'using {i};' for i in vc.listfy(using)]) + ('\n\n' if len(using) > 0 else '') + block(
        [' ', 'namespace', namespace],
        ['\n', 
            block(
                [' ', 'class', name],
                ['\n\n'] + vc.listfy(menbers)
            )
        ]
    )
class asp:
    def __init__(self, project, name, parameter):
        self.name = name.capitalize()
        self.sql_obj = {}
        self.csharp_obj = {}
        for i in parameter:
            tn, ts = parameter[i]
            self.sql_obj[i] = ts
            self.csharp_obj[i] = tn
        self.sql = table(name, self.sql_obj,lambda field : '@' + field.capitalize() )
        self.project = project
    def generate(self, path, database):
        db = sql('information_schema')
        repository = path + f'\\Core\\Repositories\\{self.name}Repository.cs'
        entity = path + f'\\Core\\Domain\\{self.name}.cs'
        controller = path + f'\\Controllers\\Restrito\\{self.name}Controller.cs'
        if(not op.isfile(repository) and not op.isfile(entity) and not op.isfile(controller)):
            if(not self.name in [i['TABLE_NAME'] for i in db.query(f'SELECT TABLE_NAME FROM TABLES WHERE table_schema = "{database}"')]):
                f = open(entity, "x")
                f.write(self.entity)
                f.close()
                f = open(controller, "x")
                f.write(self.controller)
                f.close()
                f = open(repository, "x")
                f.write(self.repository)
                f.close()
                if(not database in [i['Database'] for i in db.query('SHOW DATABASES')]):
                    db.run(f'CREATE DATABASE {database}')
                db.close()
                db = sql(database)
                create = self.sql.create
                db.run(create)
                print(create)
                db.close()
            else:
                print(c.red+'Database Already exists.'+c.white)
        else:
            print(c.red+'Files already exists.'+c.white)
    @property
    def repository(self):
        return classe(
            [
                'System',
                'System.Collections.Generic',
                'Dapper', 
                self.project + '.Core.Database',
                self.project + '.Core.Entities',
                self.project + '.Core.Interfaces',
                'MySql.Data.MySqlClient'
            ],
        self.project + '.Core.Repositories',self.name + 'Repository',
        [
            block(f'public List<{self.name}> Get()',
            ['\n',block('using (var connection = new DBConnection().GetConnection())',f'return connection.query<{self.name}>(@"\n{self.sql.select}")')]),
            block(f'public {self.name} Get(int id)',
            ['\n',block('using (var connection = new DBConnection().GetConnection())',f'return connection.query<{self.name}>(@"\n{self.sql.select_id}", new {{Id = id}})')]),
            block(f'public void Insert({self.name} parameter)',
            ['\n',block('using (var connection = new DBConnection().GetConnection())',f'return connection.query<{self.name}>(@"\n{self.sql.insert}", parameter)')]),
            block(f'public void Update({self.name} parameter)',
            ['\n',block('using (var connection = new DBConnection().GetConnection())',f'return connection.query<{self.name}>(@"\n{self.sql.update}", parameter)')])
        ])
    
    @property
    def entity(self):
        capitalized = [i.capitalize() for i in self.csharp_obj]
        types = [self.csharp_obj[i] for i in self.csharp_obj]
        return classe(['System','System.ComponentModel.DataAnnotations'], self.project+'.Core.Domain', self.name, 
        [fn.build('dotnet','proprety',[types[i], capitalized[i]]) for i in range(len(self.csharp_obj))])
    
    @property
    def controller(self):
        using = [
            'System',
                'System.Collections.Generic',
                'Dapper', 
                self.project + '.Core.Domain',
                self.project + '.Core.Repositories',
                'Microsoft.AspNetCore.Authorization',
                'Microsoft.AspNetCore.Mvc'
        ]
        return vc.cat(['\n']+[f'using {i};' for i in vc.listfy(using)]) + ('\n\n' if len(using) > 0 else '') + block(
            [' ', 'namespace', self.project+'.Controllers.Restrito'],
            ['\n', 
                block(
                    ['\n','[Authorize(Policy = "token")]','[Route("api/[controller]")]',f'[ApiExplorerSettings(GroupName = "{self.name}")]', vc.cat([' ', 'class', self.name+'Controller'])],
                    ['\n\n', 
                        return_block(['\n','[httpGet("{id}")]',f'[ProducesResponseType(typeof({self.name}), 200)]',f'public {self.name} Get(int id)'],
                        f'{self.name}Repository.Get(id);'),
                        return_block(['\n','[httpGet]',f'[ProducesResponseType(typeof(List<{self.name}>), 200)]',f'public List<{self.name}> Get()'],
                        f'{self.name}Repository.Get(id);'),
                        block(['\n','[httpPost]',f'public void Post([FromBody] {self.name} parameter)'],
                    ['\n',
                            block('if(parameter.Id == 0)',f'{self.name}Repository.Insert(parameter);'),
                            block('else',f'{self.name}Repository.Update(parameter);')
                    ]),
                    return_block(['\n','[httpDelete("{id}")]',f'public void Delete(int id)'],
                        f'{self.name}Repository.Delete(id);'),
                    ]
                )
            ]
        )
