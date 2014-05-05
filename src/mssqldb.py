"""
Created on Apr 15, 2014

Description:
Basic method of sql server db operation, including connect to DB and execute some sqls

@author: Yecheng

"""

import pymssql ## official ms sql server lib
import pyMSSQL
import functools
import types


def sql_error_log_handler(text):
    def decorator(func):
        @functools.wraps(func)
        def print_sql(*args, **kw):
            print "Error occur when executing %s action" % text
            return func(*args, **kw)

        return print_sql

    return decorator


class myMSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def _GetConnect(self):
        """
        connect to db
        return conn.cursor()
        """
        if not self.db:
            raise ("No such DB")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()

        if not cur:
            raise (NameError, "Connet to DB " + self.db + " failed")
        else:
            return cur


    def ExecQuery(self, sql):
        """
        execute query 
        return a tuple list
        """
        cur = self._GetConnect()

        cur.execute(sql)
        resList = cur.fetchall()
        #close the connection after query
        self.conn.close()
        return resList


    def ExecNoQuery(self, sql):
        """
        execute none-query 
        return affect rows
        """
        cur = self._GetConnect()
        try:
            cur.execute(sql)
            self.conn.commit()  # important
        except:
            self.conn.close()
            raise "%s error" % sql.strip().split(" ")[0]

        self.conn.close()
        return True

    def sync(self, table_class):

        column_str = []
        create_table_sql = 'create table %s ' % str(table_class.__name__)
        if issubclass(table_class, pyMSSQL.myModule):
            #print table_class
            mapping_attr = vars(table_class)['__mapping__']  # get all columns

            for attr_name in mapping_attr.keys():
                if isinstance(mapping_attr[attr_name], pyMSSQL.Field):
                    #print "yes"
                    #print mapping_attr[attr_name].column_type
                    column_str.append(mapping_attr[attr_name].name + ' ' + mapping_attr[attr_name].column_type)
            create_table_sql += "(%s)" % ",".join(column_str)
        print "Creating table using sql --%s--" % create_table_sql

        try:
            self.ExecNoQuery(create_table_sql)
        except:
            if isinstance(self.ExecQuery("select * from %s" % str(table_class.__name__)), types.ListType):
                print "Info: Table %s may already exists" % str(table_class.__name__)
            else:
                print "Info: Other unknown error" 
        