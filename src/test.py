import mssqldb
from pyMSSQL import *

class Users(myModule):
    id = IntegerField('id')
    name = StringField('name')
    email = StringField('email')
    password = StringField('password')
    

db = mssqldb.myMSSQL("localhost",'sa','symantec','test')  ## server ip, user, pwd, DB


"""
def all_members(aClass):
    try:
        #new class
        mro = list(aClass.__mro__)
    except AttributeError:
        #old class
        def getmro(aClass,recurse):
            mro = [aClass]
            for base in aClass.__bases__:
                mro.extend(recurse(base,recurse))
            return mro
        def getmro1(aClass):
            mro = [aClass]
            for base in aClass.__bases__:
                mro.extend(getmro1(base))
            return mro
        mro = getmro(aClass,getmro)

    mro.reverse()
    print aClass.__name__," mro:",mro
    members = {}
    for someClass in mro:
        members.update(vars(someClass))
    return members
all_attr =  all_members(User)
print all_attr
for i in all_attr:
    print i
"""

db.sync(Users)

#u = Users( id=1, name='Yecheng', email='yecheng@123.com', password='password') ## new a record in User table

#u.save(db) # save the change to db

