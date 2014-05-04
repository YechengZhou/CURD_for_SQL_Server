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



import types

    
class Field(object):
    def __init__(self,name,column_type,**kwar):
        self.name = name
        self.column_type = column_type
        
        if kwar.has_key("default"):
            self.default = kwar["default"]
            #print "%s have no default value" % self.name
    
    def has_key(self,attr):
        for i in dir(self):
            if i == attr:
                return True
        return False
        
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)
    
class StringField(Field):
    def __init__(self,name,**kwar):
        print kwar
        if kwar.has_key("default"):
            super(StringField,self).__init__(name,'varchar(100)',default = kwar["default"])
        else:
            super(StringField,self).__init__(name,'varchar(100)')

class IntegerField(Field):       
    def __init__(self,name,**kwar):
        super(IntegerField,self).__init__(name,"bigint",**kwar)

class myModuleMetaclass(type):
    def __new__(cls,name,bases,attrs):
        if name == "myModule":
            return type.__new__(cls,name,bases,attrs)
        mapping = dict()
        for k,v in attrs.iteritems():
            if isinstance(v,Field):
                print('Found mapping: %s==>%s' % (k,v))
                mapping[k] = v
            """elif isinstance(v,mssqldb.myMSSQL):
                attrs["__database__"] = v
                print 'Connect to DB and get myMSSQL to do DB operations'
            else:
                print "#"
                print k,v """
        for k in mapping.iterkeys():
            attrs.pop(k)
        attrs["__table__"] = name
        attrs["__mapping__"] = mapping
        print "mapping", mapping
        return type.__new__(cls, name, bases, attrs)
    
class myModule(dict):
    __metaclass__ = myModuleMetaclass
    
    def __init__(self,**kw):
        super(myModule,self).__init__(**kw)
    
    def __getattr__(self,key):
        try:
            return self[key]
        except:
            if self.__mapping__.has_key(key) and isinstance(self.__mapping__[key],Field): ## find this arrt in __mapping__ and get default value
                if self.__mapping__[key].has_key('default'):
                    if self.__mapping__[key].default == 'NULL':
                        self.__setarr__(key,None)
                    else:
                        self.__setarr__(key, self.__mapping__[key].default)
                    return self[key]
            raise AttributeError(r"myModule do not have attr %s" % key)
    
    def __setarr__(self,key,value):
        self[key] = value
    
    def save(self, db):
        fields = []
        values = []
        
        print "in save %s" % self.__mapping__
        # assemble SQL query to execute 
        for k,v in self.__mapping__.iteritems():
            fields.append(v.name)
            values.append(getattr(self,k))
                
        fields_num = []
        fields_str = []
        values_num = []
        values_str = []
        
        for k,v in self.__mapping__.iteritems():
            

            this_value  = getattr(self,k)
            
            if type(this_value) is types.StringType:
                values_str.append(this_value)
                fields_str.append(v.name)
            elif type(this_value) in (types.IntType, types.LongType, types.FloatType, types.ComplexType):
                values_num.append(this_value)
                fields_num.append(v.name)
            elif type(this_value) is types.BooleanType:
                values_str.append(this_value)
                fields_str.append(v.name)
            elif this_value is None:  ## add to num list because NULL has no "", just like numbers
                values_num.append('NULL')
                fields_num.append(v.name)
                
        self.sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields_str) + ',' + ','.join(fields_num), ','.join([("'%s'" % str(i)) for i in values_str]) + ',' + ','.join([str(j) for j in values_num]))
        
        print self.sql
        
        db.ExecNoQuery(self.sql)
        
    
        
        
        