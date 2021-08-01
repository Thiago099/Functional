
import functional as fn
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
    def create(self):
        field = fn.merge(self.field, self.type)
        if(self.id):
            field.append('PRIMARY KEY (id)')
        
        return fn.build('sql', 'create', [
            self.table,
            field
        ]) + ';\n'
    
    @property
    def insert(self):
        return fn.build('sql', 'insert values', [
            self.table,
            self.field[1::] if self.id else self.field,
            self.value[1::] if self.id else self.value
        ]) + ';\n'
    
    @property
    def select(self):
        return fn.build('sql', 'select from', [
            self.field,
            self.table
        ]) + ';\n'
    
    @property
    def update(self, condition = None):
        if(not self.id and not condition):
            return c.red + 'condition required' + c.white
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
            ) if self.id else condition
        ])+ ';\n'
