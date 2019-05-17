# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import json
import re

# load the article from the spider
class Article:
    # init the article from the spider dic
    def __init__(self, dic):
        self.article = {}
        self.article["id"] = self.__get_id(dic)
        self.article["category_id"] = self.__get_category_id(dic)
        self.article["title"] = self.__get_title(dic)
        self.article["content"] = self.__get_content(dic)
        self.article["time"] = self.__get_time(dic)
        self.article["author_id"] = self.__get_author_id(dic)
    
    # get the article id
    def __get_id(self, text_dict):
        if "id" in text_dict:
            return text_dict["id"]

    # get the category id
    def __get_category_id(self, text_dict):
        if "category_id" in text_dict:
            return text_dict["category_id"]

    # get the title
    def __get_title(self, text_dict):
        if "title" in text_dict:
            title = text_dict["title"]
            del_list = [
                        r"\\",
                        r"\"",
                       ]
            for pattern in del_list:
                temp = re.sub(pattern, "", title) 
                title = temp
            return title

    # get the content
    def __get_content(self, text_dict):
        if "content" in text_dict:
            return self.__format(text_dict["content"])

    # get the time
    def __get_time(self, text_dict):
        if "created_time" in text_dict:
            return text_dict["created_time"]

    # get the author id
    def __get_author_id(self, text_dict):
        if "author_id" in text_dict:
            return text_dict["author_id"]

    def __format(self, content):
        del_list = [
                    r"<p>编者按.*?</p>", 
                    r"<em\s*>.*?</em>", 
                    r"<animate\s*>.*?</animate>", 
                    r"<spanlang\s*>.*?</spanlang>", 
                    r"<a .*?>", 
                    r"<br .*?>", 
                    r"<img .*?>",
                    r"<ol .*?>", 
                    r"<p .*?>", 
                    r"<span .*?>", 
                    r"<article .*?>", 
                    r"<strong .*?>", 
                    r"<blockquote .*?>",
                    r"<ul .*?>", 
                    r"<u .*?>", 
                    r"<pre .*?>", 
                    r"<link .*?>", 
                    r"<li .*?>", 
                    r"<embed .*?>", 
                    r"<address .*?>", 
                    r"<h\d* .*?>",  
                    r"<iframe .*?>", 
                    r"</*h\d*\s*>",  
                    r"</*strong\s*>", 
                    r"</*span\s*>", 
                    r"</*spancalibri>", 
                    r"</*spanlang\s*>", 
                    r"</*param\s*>", 
                    r"</*p>", 
                    r"</*up>", 
                    r"</*embed>", 
                    r"</*img/*>", 
                    r"</*address>", 
                    r"</*a>", 
                    r"</*u>", 
                    r"</*b\s*>", 
                    r"</*li>", 
                    r"</*i\s*>", 
                    r"</*ul>", 
                    r"</*ol>", 
                    r"</*pre>", 
                    r"</*iframe>", 
                    r"</*article>", 
                    r"</*blockquote>",
                    r"<br/*>", 
                    r"<hr\s*/*>", 
                    r"</em>", 
                    r"&nbsp;", 
                    r"&amp;", 
                    r"&gt;", 
                    r"&quot;", 
                    r"&nbs", 
                    r"\\t", 
                    r"\\", 
                    r"\"", 
                    r"\\n", 
                   ]
        for pattern in del_list:
            temp = re.sub(pattern, "", content) 
            content = temp
        
        sub_list = [(r"&#39;", "'"), (r"&lt;", "<")]
        for sub, to_sub in sub_list:
            temp = re.sub(sub, to_sub, content)
            content = temp
        return content

    # for printing
    def __str__(self):
        return (json.dumps(self.article, ensure_ascii=False))


if __name__ == "__main__":
    pass
