CURD for SQL Server
=================================== 

Simple(maybe stupid...) ORM for SQL Server.

Help to make SQL Server easy to use, avoid executing sql command to do CURD in SQL Server.

It hasn't support complex operation, it just a practice for python...

Sample Code:
-----------------------------------  

###Create table:
```python
>>> import mssqldb
>>> from pyMSSQL import *
>>> class Users(myModule):  ## create table
>>>    id = IntegerField('id',default='NULL')
>>>    name = StringField('name',default='NULL')
>>>    email = StringField('email',default='NULL')
>>>    password = StringField('password',default='NULL')

>>>db = mssqldb.myMSSQL("localhost",'sa','sa','test')  ## creare db instance , parameters: server ip, user, pwd, DB, 

>>>db.sync(Users)  # create table, just like django..
```

###Insert:
```python
>>>u = Users( id=1, name='Yecheng', email='yecheng@123.com', password='password') ## new a record in User table

>>>u.save(db) # save the change to db
```

###Delete:
```python
>>>Users.delete(db,name='Ethan') # == delete from Users where name = 'Ethan'
```


###Update:
```python
>>>Users.update(db, name='Ethan').where(name='ethan') # == Update Users SET email = 'Ethan' WHERE name = 'ethan' 
```
