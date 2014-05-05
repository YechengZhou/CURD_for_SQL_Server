CRUD_for_SQL_Server

Simple ORM for SQL Server
Help to make SQL Server easy to use, avoid executing sql command to do CRUD in SQL Server

=====

Sample


Create tabble:

class Users(myModule):  ## create table
    id = IntegerField('id',default='NULL')
    name = StringField('name',default='NULL')
    email = StringField('email',default='NULL')
    password = StringField('password',default='NULL')

db = mssqldb.myMSSQL("localhost",'sa','sa','test')  ## server ip, user, pwd, DB

db.sync(Users)  # create table, just like django..


Insert:

u = Users( id=1, name='Yecheng', email='yecheng@123.com', password='password') ## new a record in User table

u.save(db) # save the change to db


Delete:

Users.delete(db,name='Ethan') # == delete from User where name = 'Ethan'
