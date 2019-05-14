#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

# my own libraries
import article
from myLog import log
from myConf import conf

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
            column_list = [key.strip() for key in column_key.split(",")]
            for i, column in enumerate(column_list):
                dic[column] = match.group(i + 1)
    except:
        pass
    
    return dic

# build the insert sql
def build_insert_sql(dic):
    column_key = conf.get("column", "spider")
    column_list = [key.strip() for key in column_key.split(",")]
    value_str = ", ".join([dic[key] for key in column_list])
    insert_sql = "replace into table (" + column_key + ") value (" + value_str + ")"
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
        cursor.excute(insert_sql)
        db.commit()
        log.info("excute sql success: " + insert_sql)
    except:  # if fail, rollback
        db.rollback()
        log.info("excute sql fail: " + insert_sql)

    db.close()
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

# get the max id that have been spidered already
def get_current_id(file):
    fin = open(file, "r", encoding="utf-8")
    current_id = int(fin.read())    
    fin.close()
    return current_id

if __name__ == "__main__":
    id_file = "../data/current_id"
    
    # get the begin_id
    begin_id = get_current_id(id_file) + 1
    fail = 0
    
    # if fail >= threshold, quit; else, random sleep and spider the next id
    while fail < 100:
        ret = spider(begin_id)
        if ret:
            fails = 0
        time.sleep(random.randint(1, 3))
        begin_id += 1
        fail += 1
