#!/usr/bin/env python3
# -*- coding: utf-8

# third party libraries
import pymysql

# my libraries
# from myLog import log

# connect db
def mysql_connect(host, user, password, database):
    db = pymysql.connect(host, user, password, database)
    return db

# close db
def mysql_close(db):
    db.close()
    return 0

# insert mysql
def mysql_execute(db, sql):
    cursor = db.cursor()
    try:
       cursor.execute(sql)
       db.commit()
    except:
        db.rollback()
        return -1

    return 0

# select mysql
def mysql_select(db, sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except:
        result = None

    return result
    
