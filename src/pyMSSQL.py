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
    def __init__(self, name, column_type, **kwar):
        self.name = name
        self.column_type = column_type

        if kwar.has_key("default"):
            self.default = kwar["default"]
            #print "%s have no default value" % self.name

    def has_key(self, attr):
        for i in dir(self):
            if i == attr:
                return True
        return False

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)


class StringField(Field):
    def __init__(self, name, **kwar):
        print kwar
        if kwar.has_key("default"):
            super(StringField, self).__init__(name, 'varchar(100)', default=kwar["default"])
        else:
            super(StringField, self).__init__(name, 'varchar(100)')


class IntegerField(Field):
    def __init__(self, name, **kwar):
        super(IntegerField, self).__init__(name, "bigint", **kwar)


class myModuleMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == "myModule":
            return type.__new__(cls, name, bases, attrs)
        mapping = dict()
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                print('Found mapping: %s==>%s' % (k, v))
                mapping[k] = v
        for k in mapping.iterkeys():
            attrs.pop(k)
        attrs["__table__"] = name
        attrs["__mapping__"] = mapping
        print "mapping", mapping
        return type.__new__(cls, name, bases, attrs)


class myModule(dict):
    __metaclass__ = myModuleMetaclass

    def __init__(self, **kw):
        super(myModule, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except:
            if self.__mapping__.has_key(key) and isinstance(self.__mapping__[key],
                                                            Field):  # find this arrt in __mapping__ and get default value
                if self.__mapping__[key].has_key('default'):
                    if self.__mapping__[key].default == 'NULL':
                        self.__setarr__(key, None)
                    else:
                        self.__setarr__(key, self.__mapping__[key].default)
                    return self[key]
            raise AttributeError(r"myModule do not have attr %s" % key)

    def __setarr__(self, key, value):
        self[key] = value

    def save(self, db):
        fields = []
        values = []

        print "in save %s" % self.__mapping__
        # assemble SQL query to execute 
        for k, v in self.__mapping__.iteritems():
            fields.append(v.name)
            values.append(getattr(self, k))

        fields_num = []
        fields_str = []
        values_num = []
        values_str = []

        for k, v in self.__mapping__.iteritems():


            this_value = getattr(self, k)

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

        self.sql = 'insert into %s (%s) values (%s)' % (
            self.__table__, ','.join(fields_str) + ',' + ','.join(fields_num),
            ','.join([("'%s'" % str(i)) for i in values_str]) + ',' + ','.join([str(j) for j in values_num]))

        print self.sql

        db.ExecNoQuery(self.sql)

    @classmethod
    def check_options(self, kw_dict):  # including check NULL values
        condition_list = []
        for k, v in kw_dict.iteritems():
            if k not in self.__mapping__.iterkeys():
                raise AttributeError("Do not have column %s in %s table" % k, self.__name__)
            else:
                condition_list.append("%s = '%s'" % (k, v)) if v != None else condition_list.append(
                    "%s = %s" % (k, 'NULL'))
        return condition_list

    @classmethod
    def delete(cls, db, **kw):
        try:
            delete_condition_list = cls.check_options(kw)
        except AttributeError:
            raise AttributeError(AttributeError.message + ',' + " you can not delete this time")

        delete_condition_str = ','.join(delete_condition_list)
        cls.delete_sql = "delete from %s where %s " % (cls.__name__, delete_condition_str)
        print cls.delete_sql
        delete_result = db.ExecNoQuery(cls.delete_sql)
        print "execution result: %s" % delete_result

    @classmethod
    def update(cls, db, **kw):

        try:
            set_condition_list = cls.check_options(kw)
        except AttributeError:
            raise AttributeError(AttributeError.message + ',' + " you can not delete this time")

        #print update_condition_list
        #cls.update_sql = "Update %s Set %s Where %s" % (cls.__name__, )


        class update_TEMP():
            def __init__(self, db, table_name, set_condition_list):
                self.db = db
                self.table_name = table_name
                self.set_condition_list = set_condition_list

            def where(self, **kwargs):
                try:
                    self.where_condition_list = cls.check_options(kwargs)
                except AttributeError:
                    raise AttributeError(AttributeError.message + ',' + " you can not delete this time")
                #return self.where_condition_list
                self.db_operator()

            def sql_generator(self):
                print self.set_condition_list
                set_str = ",".join(self.set_condition_list)
                where_str = ",".join(self.where_condition_list)
                print set_str, where_str
                self.update_sql = "Update {0:s} Set {1:s} Where {2:s}".format(self.table_name, set_str, where_str)
                try:
                    set_str = ",".join(self.set_condition_list)
                    where_str = ",".join(self.where_condition_list)
                    self.update_sql = "Update {0:s} Set {1:s} Where {2:s}".format(self.table_name, set_str, where_str)
                except:
                    raise AttributeError("Generating sql for update failed")
            update_sql = property(sql_generator)

            def db_operator(self):
                print self.update_sql
                db.ExecNoQuery(self.update_sql)

        temp_update = update_TEMP(db, cls.__name__, set_condition_list)

        return temp_update