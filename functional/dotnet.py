import sys
sys.path.insert(1, 'bin')
sys.path.insert(1, 'functional')

import functional as fn
from sql import table
import vector as vc


class asp:
    def __init__(self, project, name, parameter):
        self.name = name.capitalize()
        self.sql_obj = {}
        self.csharp_obj = {}
        for i in parameter:
            tn, ts = parameter[i]
            self.sql_obj[i] = ts
            self.csharp_obj[i] = tn
        self.sql = table(name,self.sql_obj)
        self.project = project

    def __block(self, name, block):
        return fn.build('programming','decorated block', [name, block])

    def __return_block(self, name, block):
        return fn.build('dotnet','return block', [name, block])


    def __classe(self, using, namespace, name, menbers):
        return vc.cat(['\n']+[f'using {i};' for i in vc.listfy(using)]) + ('\n\n' if len(using) > 0 else '') + self.__block(
            [' ', 'namespace', namespace],
            ['\n', 
                self.__block(
                    [' ', 'class', name],
                    ['\n\n'] + vc.listfy(menbers)
                )
            ]
        )
    @property
    def repository(self):
        return self.__classe(
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
            self.__block(f'public List<{self.name}> Get()',
            ['\n',self.__block('using (var connection = new DBConnection().GetConnection())',f'return connection.query<{self.name}>(@"\n{self.sql.select}")')]),
            self.__block(f'public {self.name} Get(int id)',
            ['\n',self.__block('using (var connection = new DBConnection().GetConnection())',f'return connection.query<{self.name}>(@"\n{self.sql.select_id}", new {{Id = id}})')]),
            self.__block(f'public void Insert({self.name} parameter)',
            ['\n',self.__block('using (var connection = new DBConnection().GetConnection())',f'return connection.query<{self.name}>(@"\n{self.sql.insert}", parameter)')]),
            self.__block(f'public void Update({self.name} parameter)',
            ['\n',self.__block('using (var connection = new DBConnection().GetConnection())',f'return connection.query<{self.name}>(@"\n{self.sql.update}", parameter)')])
        ])
    
    @property
    def entity(self):
        capitalized = [i.capitalize() for i in self.csharp_obj]
        types = [self.csharp_obj[i] for i in self.csharp_obj]
        return self.__classe(['System','System.ComponentModel.DataAnnotations'], self.project+'.Core.Domain', self.name, 
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
        return vc.cat(['\n']+[f'using {i};' for i in vc.listfy(using)]) + ('\n\n' if len(using) > 0 else '') + self.__block(
            [' ', 'namespace', self.project+'.Controllers.Restrito'],
            ['\n', 
                self.__block(
                    ['\n','[Authorize(Policy = "token")]','[Route("api/[controller]")]',f'[ApiExplorerSettings(GroupName = "{self.name}")]', vc.cat([' ', 'class', self.name+'Controller'])],
                    ['\n\n', 
                        self.__return_block(['\n','[httpGet("{id}")]',f'[ProducesResponseType(typeof({self.name}), 200)]',f'public {self.name} Get(int id)'],
                        f'{self.name}Repository.Get(id);'),
                        self.__return_block(['\n','[httpGet]',f'[ProducesResponseType(typeof(List<{self.name}>), 200)]',f'public List<{self.name}> Get()'],
                        f'{self.name}Repository.Get(id);'),
                        self.__block(['\n','[httpPost]',f'public void Post([FromBody] {self.name} parameter)'],
                    ['\n',
                            self.__block('if(parameter.Id == 0)',f'{self.name}Repository.Insert(parameter);'),
                            self.__block('else',f'{self.name}Repository.Update(parameter);')
                    ]),
                    self.__return_block(['\n','[httpDelete("{id}")]',f'public void Delete(int id)'],
                        f'{self.name}Repository.Delete(id);'),
                    ]
                )
            ]
        )
