'''
Created on Apr 15, 2014

Description:
ORM for Microsoft SQL Server 

@author: Yecheng
'''

"""
interface design, like other ORMs:

class User(Model):
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')


u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')

u.save()
"""
class Field(object):
    def __init__(self,name,colum_type):
        self.name = name
        self.colum_type = colum_type
        
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)
    
class StringField(Field):
    def __init__(self,name):
        super(StringField,self).__init__(name,'varchar(100)')

class IntegerField(Field):       
    def __init__(self,name):
        super(IntegerField,self).__init__(name,"bigint")

class ModelMetaclass(type):
    def __new__(cls,name,bases,attrs):
        if name == "Model":
            return type.__new__(cls,name,bases,attrs)
        mapping = dict()
        for k,v in attrs.iteritems():
            if isinstance(v,Field):
                print('Found mapping: %s==>%s' % (k,v))
                mapping[k] = v
        for k in mapping.iterkeys():
            attrs.pop(k)
        attrs["__table__"] = name
        attrs["__mapping__"] = mapping
        return type.__new__(cls, name, bases, attrs)
    
class Model(dict):
    __metaclass__ = ModelMetaclass
    
    def __init__(self,**kw):
        super(Model,self).__init__(**kw)
    
    def __getattr__(self,key):
        try:
            return self[key]
        except:
            raise AttributeError(r"Model do not have attr %s" % key)
    
    def __setarr__(self,key,value):
        self[key] = value
    
    def save(self):
        fields = []
        values = []
        
        for k,v in self.__mapping__.iteritems():
            fields.append(v.name)
            values.append(getattr(self,k))

        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join([str(i) for i in values]))
        print sql
class User(Model):
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')
    
if __name__ == "__main__":
    
    u = User(id=1, name='Yecheng', email='yecheng@123.com', password='password')
    u.save()        
