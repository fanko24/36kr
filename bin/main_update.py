#!/usr/bin/env python3
# -*- coding: utf-8
# author: 8137125@qq.com

# my libraries
import spider
import sql
from myLog import log


if __name__ == "__main__":
    # get the max id of article that have spidered
    current_id = sql.get_max_id()

    cnt = 0
    while cnt < 30:
        current_id += 1
        ret = spider.spider(current_id)
        if not ret:
            log.info("Update success: " + str(current_id))
            cnt = 0
        else:
            log.warning("Update fail: " + str(current_id))
            cnt += 1
