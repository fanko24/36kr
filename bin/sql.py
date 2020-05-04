#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# download, analyze and store the 36kr article


# standard libraries
import pymysql


# my libraries
from myConf import conf
from myLog import log


# update the article
def store(article_id, dic):
    ret = 0
    value_str = get_value_str(dic, article_id)
    update_str = get_update_str(dic, article_id)
    column_key = conf.get("column", "keys")

    db = pymysql.connect("localhost","root","fanofkobe","36kr" ) 
    sql = "insert into article_success (" + column_key + ", old_id) values (" + value_str + ") on duplicate key update " + update_str
    print (sql)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        ret = -1

    db.close()
    return ret


# get insert value string
def get_value_str(dic, article_id):
    str_list = []
    column_key = conf.get("column", "keys")
    column_type = conf.get("column", "types")
    key_list = [key.strip() for key in column_key.split(",")]
    type_list = [typ.strip() for typ in column_type.split(",")]
    for i, key in enumerate(key_list):
        typ = type_list[i]
        if dic[key] == None:
            str_list.append("null")
        elif typ == "char":
            str_list.append("'"+dic[key].replace("'", "-").strip(",\\")+"'")
        else:
            str_list.append(str(dic[key]))
    str_list.append(str(article_id))
    return ",".join(str_list)


# get update string
def get_update_str(dic, article_id):
    str_list = []
    column_key = conf.get("column", "keys")
    column_type = conf.get("column", "types")
    key_list = [key.strip() for key in column_key.split(",")]
    type_list = [typ.strip() for typ in column_type.split(",")]
    for i, key in enumerate(key_list):
        typ = type_list[i]
        if dic[key] == None:
            str_list.append(key + "=null")
        elif typ == "char":
            str_list.append(key + "='"+dic[key].replace("'", "-").strip(",\\")+"'")
        else:
            str_list.append(key + "=" + str(dic[key]))

    str_list.append("old_id" + "=" + str(article_id))
    return ",".join(str_list)


# update mysql article_fail
def update_fail(article_id, error_type):
    ret = 0
    db = pymysql.connect("localhost","root","fanofkobe","36kr" ) 
    sql = "insert into article_fail (old_id, type) values (" + str(article_id) + "," + str(error_type) + ") on duplicate key update type =" + str(error_type) 
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        log.warning("update_fail fail: " + sql)
        db.rollback()
        ret = -1

    db.close()
    return ret


# update mysql article_pass
def update_pass(article_id):
    ret = 0
    db = pymysql.connect("localhost","root","fanofkobe","36kr" ) 
    sql = "insert into article_pass (old_id) values (" + str(article_id) + ") on duplicate key update old_id =" + str(article_id) 
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        log.warning("update_pass fail: " + sql)
        db.rollback()
        ret = -1

    db.close()
    return ret


def get_min_id():
    min_id = 0
    db = pymysql.connect("localhost","root","fanofkobe","36kr" ) 
    sql = "select min(old_id) from article_success"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        min_id = int(result[0])
        db.commit()
    except:
        db.rollback()

    return min_id 


def get_max_id():
    max_id = 0
    db = pymysql.connect("localhost","root","fanofkobe","36kr" ) 
    sql = "select max(old_id) from article_success"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        max_id = int(result[0])
        db.commit()
    except:
        db.rollback()

    return max_id 

if __name__ == "__main__":
    min_id = get_min_id()
    print (min_id)
