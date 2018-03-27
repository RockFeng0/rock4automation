# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.database.pregresql

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      pyrunner.ext.database.pregresql,v 1.0 2016年3月16日
    FROM:   2016年3月16日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


import psycopg2, re

# postgresql数据库相关操作
class SQL(object):
    def __init__(self):
        self.__conn = None
        self.__cur = None
        self.data = {}

    # 打开数据库连接
    # param config -- 数据库配置信息
    def open(self, config):
        self.__conn = psycopg2.connect(database=config['database'], user=config['user'],
                                       password=config['password'],
                                       host=config['host'],
                                       port=config['port'])

    # 查询单条记录
    # param var -- 存放结果集的变量
    # param sql -- sql语句
    # return -- 返回dict，查询结果存储在全局变量var中
    # execpt -- 异常，如果出现异常(如：sql语句语法错误)则会打印在控制台
    def query(self, var, sql):
        '''Sample usage:
            sql = SQL()
            config = {
                'database': 'aischool',
                'user': 'aischool',
                'password': '15rLSWO4QmBlBntMjuIJeITxM8ZS1t43',
                'host': '192.168.102.241',
                'port': '5432'
            }
            sql.open(config)
            
            sql.query('a', "SELECT userid,usertype,loginname FROM t_e_user_logininfo WHERE loginname='TEST01'")
            print "a:",sql.data['a']
            
            sql.data["c"] = '11'
            sql.query('d', "SELECT userid,loginname FROM t_e_user_logininfo WHERE loginname=#c#")
            print "d:",sql.data['d']
            
            sql.close()
        '''
        try:
            sql = self.presql(sql)
            self.__cur = self.__conn.cursor()
            self.__cur.execute(sql)
            if "select" in sql.lower(): #如果是查询语句在返回结果集
                rows = self.__cur.fetchone()
                if not rows:
                    self.data[var] = []
                self.data[var] = dict(zip([j[0] for j in self.__cur.description], rows))                
            else:
                self.data[var] = []
            self.__cur.close()
        except Exception, msg:
            print "exception: %s(at variable '%s')" %(msg,var)

    # 查询多条记录
    # param var -- 存放结果集的变量
    # param sql -- sql语句
    # return -- 返回[dict]，返回结果存储在全局变量var中
    # execpt -- 异常，如果出现异常(如：sql语句语法错误)则会打印在控制台
    def queryList(self, var, sql):
        '''Sample usage:
            sql = SQL()
            config = {
                'database': 'aischool',
                'user': 'aischool',
                'password': '15rLSWO4QmBlBntMjuIJeITxM8ZS1t43',
                'host': '192.168.102.241',
                'port': '5432'
            }
            sql.open(config)
            
            sql.queryList('b', "SELECT userid,createtime FROM t_e_user_logininfo LIMIT 10")
            print "b:",sql.data['b']
            
            sql.close()            
        '''
        try:
            sql = self.presql(sql)
            self.__cur = self.__conn.cursor()
            self.__cur.execute(sql)
            self.__conn.commit()
            if "select" in sql.lower(): #如果是查询语句在返回结果集
                rows = self.__cur.fetchall()
                if not rows:
                    self.data[var] = []
                self.data[var] = [dict(zip([j[0] for j in self.__cur.description], i)) for i in rows]
            else:
                self.data[var] = []
            self.__cur.close()
        except Exception, msg:
            print "exception: %s(at variable '%s')" %(msg,var)

    # 调试sql
    # param sql -- sql语句
    def debug(self, sql):
        '''Sample usage:
            sql = SQL()
            config = {
                'database': 'aischool',
                'user': 'aischool',
                'password': '15rLSWO4QmBlBntMjuIJeITxM8ZS1t43',
                'host': '192.168.102.241',
                'port': '5432'
            }
            sql.open(config)
            
            sql.data["c"] = '11'
            sql.debug("SELECT userid,loginname FROM t_e_user_logininfo WHERE loginname=#c#")
            
            sql.close()
        '''
        try:
            sql = self.presql(sql)
            self.__cur = self.__conn.cursor()
            self.__cur.execute(sql)
            rows = self.__cur.fetchall()
            self.__cur.close()
            data = [dict(zip([j[0] for j in self.__cur.description], i)) for i in rows]
            print '---- debug start ----'
            print 'runing sql:', sql
            print 'result:', data
            print '---- debug end   ----'
        except Exception, msg:
            print 'exception:', msg

    # 关闭数据库连接
    def close(self):
        self.__conn.close()

    # 对sql进行预处理，替换其中的参数
    # param sql -- 带全局变量的sql(如有的话)
    # return 返回替换后的sql语句
    def presql(self, sql):
        params = re.findall('#(.*?)#', sql)
        for p in params:
            var = self.data[p]
            sql = sql.replace('#' + p + '#', '\''+str(var)+'\'')
        return sql

if __name__=="__main__":
    sql = SQL()
    config = {
        'database': 'aischool',
        'user': 'aischool',
        'password': '15rLSWO4QmBlBntMjuIJeITxM8ZS1t43',
        'host': '192.168.102.241',
        'port': '5432'
    }
    sql.open(config)
    
    sql.data["c"] = '11'
    sql.debug("SELECT userid,loginname FROM t_e_user_logininfo WHERE loginname=#c#")
    
    sql.close()
    


