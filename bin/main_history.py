#!/usr/bin/env python3
# -*- coding: utf-8
#download, analyze and store the 36kr articel from the min id tO 0 

# my libraries
import spider
from myLog import log

# get the min id of articles that have spidered
def get_min_id():
    return 5293032

# update the success content of the article
def update_success(cid):
    return 0

# update the fail message of the article
def update_fail(cid):
    return 0

if __name__ == "__main__":
    # get the min id of articles that have spidered
    min_id = get_min_id()
    log.info("The min id is " + str(min_id))

    current_id = min_id - 1
    cnt = 0
    while current_id > 5290000:
        ret = spider.spider(current_id)

        # if spider success, update the article to mysql; or update the fail message
        if not ret:
            update_success(current_id)
            log.info("Update success: " + str(current_id))
            cnt = 0
        else:
            update_fail(current_id)
            log.warning("Update fail: " + str(current_id))
            cnt += 1
            if cnt > 100:
                break

        current_id -= 1
