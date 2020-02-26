#!/usr/bin/env python3
# -*- coding: utf-8

# third party libraries
import pymysql

# my libraries
# from myLog import log

# connect mysql
def mysql_connect(host, user, password, database):
    db = pymysql.connect(host, user, password, database)
    return db

def mysql_close(db):
    db.close()
    return 0

