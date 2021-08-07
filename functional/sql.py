import functional as fn
import vector as vc
class table:
    def __init__(self, table, field, id = True):
        self.table = table
        self.field = []
        self.type = []

        self.id = id
        if(id):
            self.field.append('id')
            self.type.append('INT NOT NULL AUTO_INCREMENT')
        
        for i in field:
            self.field.append(i)
            self.type.append(field[i])
        
        
        
        self.value = []
        for i in self.field:
            self.value.append('@' + i.capitalize()) 
    
    @property
    def drop(self):
        return 'DROP TABLE ' + self.table + ';'
    
    @property
    def create(self):
        field = vc.merge(self.field, self.type)
        if(self.id):
            field.append('PRIMARY KEY (id)')
        
        return fn.build('sql', 'create', [
            self.table,
            [',\n'] + field
        ]) + ';'
    
    @property
    def insert(self):
        return fn.build('sql', 'insert values', [
            self.table,
            [',\n'] + (self.field[1::] if self.id else self.field),
            [',\n'] + (self.value[1::] if self.id else self.value)
        ]) + ';'
    
    @property
    def select(self):
        return fn.build('sql', 'select from', [
            [',\n'] + self.field,
            self.table
        ]) + ';'
    
    @property
    def select_id(self):
        return vc.cat(['\n',fn.build('sql', 'select from', [
            [',\n'] + self.field[1::],
            self.table
        ]),fn.build('sql','where',['id = @Id'])])+ ';'
    
    @property
    def update(self):
        if(not self.id):
            print(c.red + 'no criterion' + c.white)
            return ''
        return fn.build('sql', 'update set where', [
            self.table,
            [',\n'] + vc.merge
            (
                self.field[1::],
                self.value[1::],
                ' = '
            ),
            [',\n'] + vc.merge
            (
                self.field[:1],
                self.value[:1],
                ' = '
            )
        ])+ ';'
    
    @property
    def delete(self):
        if(not self.id):
            print(c.red + 'no criterion' + c.white)
            return ''
        return fn.build('sql', 'delete where', [
            self.table,
            [',\n'] + vc.merge
            (
                self.field[:1],
                self.value[:1],
                ' = '
            )
        ])+ ';'