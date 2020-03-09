#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: 8137125@qq.com

# standard libraries
import sys
import re
import time
import random

# third party libraries
from urllib import request

# my libraries
import sql
from myLog import log
from myConf import conf


# if crawler return fail, update article_fail
def spider(article_id):
    ret = crawler(article_id)
    if ret:
        sql.update_fail(article_id, ret)
    
    return ret


# return: -1, urlopen error; -2, decode error; -3, analyze error; -4, store error
def crawler(article_id):
    dic = {}
    # download the article
    html, ret = download(article_id)
    if ret:
        log.warning("Download fail: " + str(article_id))
        return ret
    log.info("Download success: " + str(article_id))
    
    # analyze the article
    dic = analyze(html)
    if not dic:
        log.warning("Analyze fail: " + str(article_id))
        return -3
    log.info("Analyze success: " + str(article_id))
    
    # store the article
    ret = sql.store(article_id, dic)
    if ret:
        log.warning("Store fail: " + str(article_id))
        return -4
    log.info("Store success: " + str(article_id))

    return 0


# download a page
def download(article_id):
    time.sleep(random.randint(1000,5000)/1000.0) 
    html = None

    # download the page
    url = "https://36kr.com/p/"+str(article_id)
    
    ua_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; it; rv:2.0b4) Gecko/20100818",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330",
        "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.9.2a1pre) Gecko",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; pl; rv:1.9.2.3) Gecko/20100401 Lightningquail/3.6.3",
        "Mozilla/5.0 (X11; ; Linux i686; rv:1.9.2.20) Gecko/20110805",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) Gecko/2009020409",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.3) Gecko/2008092814 (Debian-3.0.1-1)",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092816",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008090713"
        ]
    ua = random.choice(ua_list)
    headers = {"user-agent": ua}
    try:
        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
    except:
        log.warning("Urlopen fail: " + str(article_id))
        return html, -1

    try:
        html = response.read().decode("utf-8")
    except:
        log.warning("Decode fail: " + str(article_id))
        time.sleep(120.0) 
        return html, -2
    
    return html, 0


# analyze a html
def analyze(html):
    dic = {}
    pattern = re.compile(r'{"id":(.*?),"project_id":(.*?),"goods_id":(.*?),"domain_id":.*?,"column_id":(.*?),"monographic_id":(.*?),"related_company_id":.*?,"related_company_type":.*?,"related_company_name":.*?,"close_comment":.*?,"state":(.*?),"title":(.*?),"catch_title":.*?,"summary":(.*?),"content":(.*?),"cover":(.*?),"source_type":(.*?),"source_urls":(.*?),"related_post_ids":(.*?),"extraction_tags":(.*?),"extra":.*?,"user_id":(.*?),"published_at":(.*?),"created_at":(.*?),"updated_at":(.*?),"counters":(.*?),"related_company_counters":.*?,"related_posts":.*?,"is_free":.*?,"has_rights_goods":(.*?),"is_tovc":.*?,"image_source":(.*?),"company_info":.*?,"company_contact_info":.*?,"company_fund_info":.*?,"share_data":.*?,"title_mobile":.*?,"cover_mobile":.*?,.*?"audios":\[(.*?)\],.*?"db_counters":\[(.*?)\],.*?"user":.*?,"motifs"')
        
    # match the regex pattern and analyze features
    match = pattern.search(html)
    if match:
        column_key = conf.get("column", "keys")
        column_type = conf.get("column", "types")
        key_list = [key.strip() for key in column_key.split(",")]
        type_list = [typ.strip() for typ in column_type.split(",")]
        for i, column in enumerate(key_list):
            if type_list[i] == "int":
                if match.group(i + 1).isdigit():
                    dic[column] = int(match.group(i + 1))
                else:
                    dic[column] = None
            else:
                if match.group(i + 1) != "null":
                    dic[column] = match.group(i + 1).strip('"')
                else:
                    dic[column] = None
    return dic


if __name__ == "__main__":
    article_id = sys.argv[1]
    ret = spider(article_id)
    if not ret:
        log.info("Spider success: " + str(article_id))
    else:
        log.warning("Spider fail: " + str(article_id))
