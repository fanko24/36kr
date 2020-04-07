#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: 8137125@qq.com

# standard libraries
import sys

# third party libraries
import jieba
import jieba.analyse
import jieba.posseg

# my libraries
from myLog import log
from myConf import conf


if __name__ == "__main__":
    dic = {}
    for line in sys.stdin:
        sentence = line.strip()
        seg_list = jieba.analyse.extract_tags(sentence, topK=100, withWeight=False, allowPOS=())
        for word in seg_list:
            if word not in dic:
                dic[word] = 1
            else:
                dic[word] += 1
    sort_list = sorted(dic.items(), key=lambda d:d[1], reverse=True)
    for k, v in sort_list:
        print ("{}: {:.3f}".format(k,v))
