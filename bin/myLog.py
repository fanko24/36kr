#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import logging.config

# read the config file of logging
logging.config.fileConfig('../conf/log.conf')

# create a logger
log = logging.getLogger('root')


if __name__ == "__main__":
    # test log
    log.debug('debug message')
    log.info('info message')
    log.warning('warn message')
    log.error('error message')
    log.critical('critical message')
