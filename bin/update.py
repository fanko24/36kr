#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# update the 36kr articles with incremental article id

# standard libraries
import sys
import re
import time
import random
import json

# third party libraries
import pymysql
from collections import deque
from urllib.request import urlopen
from bs4 import BeautifulSoup

# my libraries
import article
from myLog import log
from myConf import conf

# get the max id that have been spidered already
def get_max_id(id_file):
    fin = open(id_file, "r", encoding="utf-8")
    current_id = int(fin.read())    
    fin.close()
    return current_id

# update the max_id to the file
def update_max_id(id_file, max_id):
    fout = open(id_file, "w", encoding="utf-8")
    fout.write(str(max_id)+"\n")
    fout.close()
    return None

# spider a page id
def spider(article_id):
    # download the page and analyze the feature
    dic = get_page(article_id)
    # if get page success, update the page
    if dic:
        log.info("get page success: " + str(article_id))
        ret = update_mysql(dic) # update the dic
        if ret:
            log.info("update page success: " + str(article_id))
        else:
             log.warning("update page fail: " + str(article_id))
        return True
    else:
        log.warning("get page fail: " + str(article_id))
        return False

# download the page and analyze features to dic
def get_page(id):
    dic = {}
    try:
        # download the page
        url = "https://36kr.com/p/"+str(id)
        response = urlopen(url)
        html = response.read().decode("utf-8")
        pattern = re.compile(r'{"id":(\d+),"project_id":.*?,"goods_id":.*?,"domain_id":.*?,"column_id":(\d+),"monographic_id":.*?,"related_company_id":.*?,"related_company_type":.*?,"related_company_name":.*?,"close_comment":.*?,"state":.*?,"title":"(.*?)","catch_title":.*?,"summary":"(.*?)","content":"(.*?)","cover":.*?,"source_type":.*?,"source_urls":.*?,"related_post_ids":"(.*?)","extraction_tags":"(.*?)","extra":.*?,"published_at":"(.*?)","created_at":"(.*?)","updated_at":"(.*?)","counters":{"view_count":(\d+),"pv":(\d+),"pv_mobile":(\d+),"pv_app":(\d+),"favorite":(\d+),"comment":(\d+),"like":(\d+)}.*?}],"user":{"id":(\d+),"name":"(.*?)","avatar_url":".*?","tovc_avatar_url"')
        
        # match the regex pattern and analyze features
        match = pattern.search(html)
        if match:
            column_key = conf.get("column", "spider")
            column_type = conf.get("column", "type")
            key_list = [key.strip() for key in column_key.split(",")]
            type_list = [typ.strip() for typ in column_type.split(",")]
            for i, column in enumerate(key_list):
                if type_list[i] == "int":
                    dic[column] = int(match.group(i + 1))
                else:
                    dic[column] = match.group(i + 1)
    except:
        pass
    
    return dic

# connect the mysql database
def connect_mysql():
    host = conf.get("mysql", "host") 
    user = conf.get("mysql", "user") 
    password = conf.get("mysql", "password") 
    database = conf.get("mysql", "database")
    db = pymysql.connect(host, user, password, database)
    if db:
        log.info("connect db success")
    else:
        log.warning("connect db fail")
    return db
     
# build the insert sql
def build_insert_sql(dic):
    column_key = conf.get("column", "spider")
    column_type = conf.get("column", "type")
    key_list = [key.strip() for key in column_key.split(",")]
    type_list = [typ.strip() for typ in column_type.split(",")]
    str_list = []
    for i, column in enumerate(key_list):
        if type_list[i] == "int":
            str_list.append(str(dic[column]))
        else:
            str_list.append("'"+str(dic[column])+"'")
    
    insert_sql = "insert into article values("+",".join(str_list)+")"
    return insert_sql

# update the result file
def update_mysql(dic):
    # connect the db
    db = connect_mysql()
    
    # fetch the cursor
    cursor = db.cursor()

    # build the sql insert text
    insert_sql = build_insert_sql(dic)
    # excute the insert sql 
    try:
        cursor.execute(insert_sql)
        db.commit()
        log.info("excute sql success: " + insert_sql)
    except:  # if fail, rollback
        db.rollback()
        log.warning("excute sql fail: " + insert_sql)
    
    db.close()
    return None

if __name__ == "__main__":
    # read the max id file
    id_file = conf.get("file", "max_id")
    
    # get the max id that have been spidered
    max_id = get_max_id(id_file)
    fail = 0
    
    # if fail >= threshold, quit; else, random sleep and spider the incremental id
    article_id = max_id + 1
    while fail < 100:
        ret = spider(article_id)
        # if spider success, update fail times and max id
        if ret:
            fail = 0
            max_id = article_id
            update_max_id(id_file, max_id)
        time.sleep(random.randint(1, 3))
        article_id += 1
        fail += 1
