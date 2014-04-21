'''
Created on Apr 15, 2014

Description:
ORM for Microsoft SQL Server 

@author: Yecheng
'''

"""
interface design, like other ORMs:

class User(myModule):
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')


u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')

u.save()
"""


#import mssqldb
import types

class Field(object):
    def __init__(self,name,column_type):
        self.name = name
        self.column_type = column_type
        
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)
    
class StringField(Field):
    def __init__(self,name):
        super(StringField,self).__init__(name,'varchar(100)')

class IntegerField(Field):       
    def __init__(self,name):
        super(IntegerField,self).__init__(name,"bigint")

class myModuleMetaclass(type):
    def __new__(cls,name,bases,attrs):
        if name == "myModule":
            return type.__new__(cls,name,bases,attrs)
        mapping = dict()
        for k,v in attrs.iteritems():
            if isinstance(v,Field):
                print('Found mapping: %s==>%s' % (k,v))
                mapping[k] = v
            """
            if isinstance(v,mssqldb.myMSSQL):
                attrs["__database__"] = v
                print('Connect to DB and get myMSSQL to do DB operations')
            """    
        for k in mapping.iterkeys():
            attrs.pop(k)
        attrs["__table__"] = name
        attrs["__mapping__"] = mapping
        return type.__new__(cls, name, bases, attrs)
    
class myModule(dict):
    __metaclass__ = myModuleMetaclass
    
    def __init__(self,**kw):
        super(myModule,self).__init__(**kw)
    
    def __getattr__(self,key):
        try:
            return self[key]
        except:
            raise AttributeError(r"myModule do not have attr %s" % key)
    
    def __setarr__(self,key,value):
        self[key] = value
    
    def save(self):
        fields = []
        values = []
        
        for k,v in self.__mapping__.iteritems():
            fields.append(v.name)
            values.append(getattr(self,k))
        
        fields_num = []
        fields_str = []
        values_num = []
        values_str = []
        
        for k,v in self.__mapping__.iteritems():
            if type(getattr(self,k)) is types.StringType:
                values_str.append(getattr(self,k))
                fields_str.append(v.name)
            elif type(getattr(self,k)) in (types.IntType, types.LongType, types.FloatType, types.ComplexType):
                values_num.append(getattr(self,k))
                fields_num.append(v.name)
            elif type(getattr(self,k)) is types.BooleanType:
                values_str.append(getattr(self,k))
                fields_str.append(v.name)
        self.sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields_str) + ',' + ','.join(fields_num), ','.join([('"%s"' % str(i)) for i in values_str]) + ',' + ','.join([str(j) for j in values_num]))
        print self.sql
        


"""

class User(myModule):
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')
    
if __name__ == "__main__":
    
    db = mssqldb.myMSSQL("localhost",'sa','symantec','test')
    db.sync(User)
    u = User(db=db, id=1, name='Yecheng', email='yecheng@123.com', password='password') ## new a record in User table
    u.save()        
"""