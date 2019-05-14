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

from myLog import log
from myConf import conf


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

