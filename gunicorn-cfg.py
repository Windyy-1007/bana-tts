# -*- encoding: utf-8 -*-

import os

bind = '0.0.0.0:10011'
workers = os.cpu_count()
accesslog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True