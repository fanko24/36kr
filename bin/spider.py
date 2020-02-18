#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# download, analyze and store the 36kr article

# standard libraries
import re
import time
import random

# standard libraries
import sys

# third party libraries
from urllib import request

# my libraries
import article
from myLog import log
from myConf import conf

# spider an article; return: -1, if urlopen error; -2, if decode error; -3, if analyze error; -4, if store error
def spider(article_id):
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
    ret = store(dic)
    if not ret:
        log.warning("Store fail: " + str(article_id))
        return -4
    log.info("Store success: " + str(article_id))
     
    return 0

# download a page
def download(article_id):
    time.sleep(random.randint(1000,2000)/1000.0) 
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
    #headers = {"user-agent": ua, "cookie": "acw_tc=2760827c15819210341097078ed3e82132c1f91b59f1cc36f0ff20d1366570; Hm_lvt_1684191ccae0314c6254306a8333d090=1581921035; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216f68f38b17823-03884ccb04109b-1d376b5b-1296000-16f68f38b18235%22%2C%22%24device_id%22%3A%2216f68f38b17823-03884ccb04109b-1d376b5b-1296000-16f68f38b18235%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; Hm_lvt_713123c60a0e86982326bae1a51083e1=1581921035; krnewsfrontss=4e190253810f3323b0c2596a59156c61; M-XSRF-TOKEN=147fb35e9519f3e6c86ec126fbf2a22f5009c49855a16596f02c1ca5325e8a88; acw_sc__v2=5e4b633553604e82f627aee9d03ccca1cca23700; Hm_lpvt_1684191ccae0314c6254306a8333d090=1581999238; SERVERID=6754aaff36cb16c614a357bbc08228ea|1581999238|1581988240; Hm_lpvt_713123c60a0e86982326bae1a51083e1=1581999238"}
    try:
        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
    except:
        log.warning("urlopen fail: " + str(article_id))
        return html, -1

    try:
        html = response.read().decode("utf-8")
    except:
        log.warning("decode fail: " + str(article_id))
        return html, -2
        
    return html, 0

# analyze a html
def analyze(html):
    dic = {}
    pattern = re.compile(r'{"id":(.*?),"project_id":(.*?),"goods_id":(.*?),"domain_id":(.*?),"column_id":(.*?),"monographic_id":(.*?),"related_company_id":(.*?),"related_company_type":"(.*?)","related_company_name":"(.*?)","close_comment":(.*?),"state":"(.*?)","title":"(.*?)","catch_title":"(.*?)","summary":"(.*?)","content":"(.*?)","cover":"(.*?)","source_type":"(.*?)","source_urls":"(.*?)","related_post_ids":"(.*?)","extraction_tags":"(.*?)","extra":(.*?),"user_id":(.*?),"published_at":"(.*?)","created_at":"(.*?)","updated_at":"(.*?)","counters":(.*?),"related_company_counters":(.*?),"related_posts":(.*?),"is_free":(.*?),"has_rights_goods":(.*?),"is_tovc":(.*?),"image_source":(.*?),"company_info":(.*?),"company_contact_info":(.*?),"company_fund_info":(.*?),"share_data":(.*?),"title_mobile":(.*?),"cover_mobile":(.*?),"ban_eclub":(.*?),"audios":(.*?),.*?"db_counters":(.*?),.*?"user":(.*?)}}')
        
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
                    dic[column] = match.group(i + 1)
                else:
                    dic[column] = None
    return dic

# store the article
def store(dic):
    print(dic)
    return True


if __name__ == "__main__":
    article_id = sys.argv[1]
    ret = spider(article_id)
    if not ret:
        log.info("Spider success: " + str(article_id))
    else:
        log.warning("Spider fail: " + str(article_id))
