#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# download, analyze and store the 36kr article

# standard libraries
import re
import time
import random

# third party libraries
from urllib import request

# my libraries
import article
from myLog import log
from myConf import conf

# spider an article
def spider(article_id):
    # download the article
    html = download(article_id)
    if not html:
        log.info("Download fail: " + str(article_id))
        return -1
    log.info("Download success: " + str(article_id))
    
    # analyze the article
    dic = analyze(html)
    if not dic:
        log.info("Analyze fail: " + str(article_id))
        return -2
    log.info("Analyze success: " + str(article_id))
    
    # store the article
    ret = store(dic)
    if not ret:
        log.info("Store fail: " + str(article_id))
        return -3
    log.info("Store success: " + str(article_id))
     
    return 0

# download a page
def download(article_id):
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
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.2.13) Gecko/20101203 iPhone",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13; ) Gecko/20101203",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1b3) Gecko/20090305",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-TW; rv:1.9.0.9) Gecko/2009040821",
        "Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.0.8) Gecko/2009032711",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.7) Gecko/2009032803",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.7) Gecko/2009021910 MEGAUPLOAD 1.0",
        "Mozilla/5.0 (Windows; U; BeOS; en-US; rv:1.9.0.7) Gecko/2009021910",
        "Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.6) Gecko/2009020911",
        "Mozilla/5.0 (X11; U; Linux i686; en; rv:1.9.0.6) Gecko/20080528",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.6) Gecko/2009020409",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.3) Gecko/2008092814 (Debian-3.0.1-1)",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092816",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008090713"
        ]
    ua = random.choice(ua_list)
    headers = {"user-agent": ua, "cookie": "acw_tc=2760827c15819210341097078ed3e82132c1f91b59f1cc36f0ff20d1366570; Hm_lvt_1684191ccae0314c6254306a8333d090=1581921035; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216f68f38b17823-03884ccb04109b-1d376b5b-1296000-16f68f38b18235%22%2C%22%24device_id%22%3A%2216f68f38b17823-03884ccb04109b-1d376b5b-1296000-16f68f38b18235%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; Hm_lvt_713123c60a0e86982326bae1a51083e1=1581921035; krnewsfrontss=4e190253810f3323b0c2596a59156c61; M-XSRF-TOKEN=147fb35e9519f3e6c86ec126fbf2a22f5009c49855a16596f02c1ca5325e8a88; acw_sc__v2=5e4b633553604e82f627aee9d03ccca1cca23700; Hm_lpvt_1684191ccae0314c6254306a8333d090=1581999238; SERVERID=6754aaff36cb16c614a357bbc08228ea|1581999238|1581988240; Hm_lpvt_713123c60a0e86982326bae1a51083e1=1581999238"}
    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    html = response.read().decode("utf-8")
    
    time.sleep(random.randint(1000,3000)/1000.0) 
    return html

# analyze a html
def analyze(html):
    dic = {}
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
    return dic

# store the article
def store(dic):
    print(dic)
    return True


if __name__ == "__main__":
    article_id = 7
    ret = spider(article_id)
    if not ret:
        log.info("Spider success: " + str(article_id))
    else:
        log.info("Spider fail: " + str(article_id))