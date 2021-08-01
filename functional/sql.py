import functional as fn
import color as c
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
        field = fn.merge(self.field, self.type)
        if(self.id):
            field.append('PRIMARY KEY (id)')
        
        return fn.build('sql', 'create', [
            self.table,
            field
        ]) + ';'
    
    @property
    def insert(self):
        return fn.build('sql', 'insert values', [
            self.table,
            self.field[1::] if self.id else self.field,
            self.value[1::] if self.id else self.value
        ]) + ';'
    
    @property
    def select(self):
        return fn.build('sql', 'select from', [
            self.field,
            self.table
        ]) + ';'
    
    @property
    def update(self):
        if(not self.id):
            print(c.red + 'no criterion' + c.white)
            return
        return fn.build('sql', 'update set where', [
            self.table,
            fn.merge
            (
                self.field[1::] if self.id else self.field,
                self.value[1::] if self.id else self.field,
                ' = '
            ),
            fn.merge
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
            return
        return fn.build('sql', 'delete where', [
            self.table,
            fn.merge
            (
                self.field[:1],
                self.value[:1],
                ' = '
            )
        ])+ ';'