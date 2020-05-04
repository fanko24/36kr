#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard libraries
import sys
import re

if __name__ == "__main__":
    for line in sys.stdin:
        sentence = line.strip()
        patterns = [("<.*?>", ""), 
                    ("\\\\n", ""),
                    ("&#39;", "'"),
                    ("&amp;", "&"),
                    ("&quot;", ""),
                    ("&nbsp;", ""),
                    ("&nbsp", ""),
                    ("&gt;", ""),
                    ("&lt;", "")
                   ]
        for old, new in patterns:
            sentence = re.sub(old, new, sentence)
        print (sentence)

