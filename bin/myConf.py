#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import configparser


# read the config file of logging
conf = configparser.ConfigParser()
conf.read("../conf/36kr.conf")


if __name__ == "__main__":
    print (conf.get("url", "homepage"))
