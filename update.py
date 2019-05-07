#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import time
import random
import json
from collections import deque
from urllib.request import urlopen
from bs4 import BeautifulSoup

# get tag from str like "[[\"人工智能\",\"rengongzhineng\",1],[\"消费\",\"xiaofei\",1],[\"阿里巴巴\",\"alibaba\",2]]"
def get_tag_list(tag):
    res = []
    lst = tag.split(",")
    for id in range(len(lst)):
        if id % 3 == 0:
            key = lst[id].strip(r'[\"')
            res.append(key.upper())
    return res

# get article id from str like "[\"5140043\",\"5145650\",\"5149297\"]"
def get_article_list(article_str):
    article_list = []
    if not article_str:
        return article_list
    new_article_str = article_str.strip("[]")
    lst = new_article_str.split(r',')
    if lst:
        article_list = [int(item.strip(r'\"')) for item in lst]
    return article_list

# download the page and analyze important features to dic
def get_page(id):
    dic = {}
    try:
        url = "https://36kr.com/p/"+str(id)
        response = urlopen(url)
        html = response.read().decode("utf-8")
        pattern = re.compile(r'{"id":(\d+),"project_id":.*?,"goods_id":.*?,"domain_id":.*?,"column_id":(\d+),"monographic_id":.*?,"related_company_id":.*?,"related_company_type":.*?,"related_company_name":.*?,"close_comment":.*?,"state":.*?,"title":"(.*?)","catch_title":.*?,"summary":"(.*?)","content":"(.*?)","cover":.*?,"source_type":.*?,"source_urls":.*?,"related_post_ids":"(.*?)","extraction_tags":"(.*?)","extra":.*?,"published_at":"(.*?)","created_at":"(.*?)","updated_at":"(.*?)","counters":{"view_count":(\d+),"pv":(\d+),"pv_mobile":(\d+),"pv_app":(\d+),"favorite":(\d+),"comment":(\d+),"like":(\d+)}.*?}],"user":{"id":(\d+),"name":"(.*?)","avatar_url":".*?","tovc_avatar_url"')
        # match and analyze all import features
        match = pattern.search(html)
        if match:
            dic["id"] = match.group(1)
            dic["category_id"] = match.group(2)
            dic["title"] = match.group(3)
            dic["summary"] = match.group(4)
            dic["content"] = match.group(5)
            dic["relate_article"] = get_article_list(match.group(6))
            dic["tag"] = get_tag_list(match.group(7))
            dic["created_time"] = match.group(9)
            dic["pv_pc"] = match.group(12)
            dic["pv_mobile"] = match.group(13)
            dic["pv_app"] = match.group(14)
            dic["author_id"] = match.group(18)
            dic["author_name"] = match.group(19)
    except:
        pass
    
    return dic

# get the max id that have been spidered already
def get_max(file):
    max_id = float("-inf")
    fin = open(file, "r", encoding="utf-8")
    for line in fin:
        dic = json.loads(line)
        if "id" in dic:
            id = int(dic["id"])
            if id > max_id:
                max_id = id
    fin.close()
    return max_id

# update the result file
def update_result(dic, result_file):
    fout = open(result_file, "a", encoding="utf-8")
    fout.write(json.dumps(dic, ensure_ascii=False)+"\n")
    fout.close()
    return None

def update_error(id, error_file):
    fout = open(error_file, "a", encoding="utf-8")
    fout.write(str(id)+"\n")
    fout.close()
    return None    

# update the id to result_file or error_file
def update(id, result_file, error_file):
    # get the first id from head of the queue
    print ("-"*30)
    
    # download the page and analyze the feature
    dic = get_page(id)

    # if the page is not blank, normal update; or else record the id in error
    if dic:
        # update result
        update_result(dic, result_file)
        print ("page done: ", id)
        return True
    else:
        update_error(id, error_file)
        print ("page error: ", id)
        return False


if __name__ == "__main__":
    error_file = "update.error"
    result_file = "update.36kr"
    
    # get the smallest id from result and error
    begin_id = get_max(result_file) + 1
    retry = 0

    # while the 
    while retry < 100:
        update_success = update(begin_id, result_file, error_file)
        if update_success:
            retry = 0
        sleeptime=random.randint(1, 3)
        time.sleep(sleeptime)
        begin_id += 1
        retry += 1
