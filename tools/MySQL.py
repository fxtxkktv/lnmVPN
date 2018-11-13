#!/usr/bin/env python
#coding=utf-8
import os,sys,logging,re
import MySQLdb
from Functions import AppServer

config=AppServer()
db_name = AppServer().getConfValue('Databases','MysqlDB')
db_user = AppServer().getConfValue('Databases','MysqlUser')
db_pass = AppServer().getConfValue('Databases','MysqlPass')
db_ip = AppServer().getConfValue('Databases','MysqlHost')
db_port = AppServer().getConfValue('Databases','MysqlPort')

def writeDb(sql,db_data=()):
    """连接mysql数据库（写），并进行写的操作"""
    try:
        conn = MySQLdb.connect(db=db_name,user=db_user,passwd=db_pass,host=db_ip,port=int(db_port),charset="utf8")
        cursor = conn.cursor()
    except Exception,e:
        #print e
        logging.debug('数据库连接失败:%s' % e)
        return False

    try:
        cursor.execute(sql,db_data)
        conn.commit()
    except Exception,e:
        conn.rollback()
        logging.debug('数据写入失败:%s,%s,%s' % (sql,db_data,e))
        return False
    finally:
        cursor.close()
        conn.close()
    return True

def readDb(sql,db_data=()):
    """连接mysql数据库（从），并进行数据查询"""
    try:
        conn = MySQLdb.connect(db=db_name,user=db_user,passwd=db_pass,host=db_ip,port=int(db_port),charset="utf8")
        cursor = conn.cursor()
    except Exception,e:
        #print e
        logging.debug('数据库连接失败:%s' % e)
        return False

    try:
        cursor.execute(sql,db_data)
        data = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    except Exception,e:
        logging.debug('数据执行失败:%s,%s,%s' % (sql,db_data,e))
        return False
    finally:
        cursor.close()
        conn.close()
    return data

def readDb2(sql,db_data=()):
    """连接mysql数据库（从），并进行数据查询"""
    try:
        conn = MySQLdb.connect(db=db_name,user=db_user,passwd=db_pass,host=db_ip,port=int(db_port),charset="utf8")
        cursor = conn.cursor()
    except Exception,e:
        #print e
        logging.debug('数据库连接失败:%s' % e)
        return False

    try:
        cursor.execute(sql,db_data)
        data = cursor.fetchall()
    except Exception,e:
        logging.debug('数据执行失败:%s,%s,%s' % (sql,db_data,e))
        return False
    finally:
        cursor.close()
        conn.close()
    return data

def testDB():
    """ 测试数据库连接 """
    try:
        conn = MySQLdb.connect(db=db_name,user=db_user,passwd=db_pass,host=db_ip,port=int(db_port),charset="utf8")
        cursor = conn.cursor()
    except Exception,e:
        #print e
        logging.debug('数据库连接失败:%s' % e)
        return False
    finally:
        cursor.close()
        conn.close()
    return True

if __name__ == '__main__':
   testDB()
   os._exit(0)
