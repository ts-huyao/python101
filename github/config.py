#!/usr/bin/env python  
""" 
@author:Hu Yao 
@license: Apache Licence 
@file: config.py.py 
@time: 2019/06/24
@contact: hooyao@gmail.com
@site:  
@software: PyCharm 
"""
import logging
import os
from logging.handlers import WatchedFileHandler

from coloredlogs import ColoredFormatter

from utils import TqdmHandler

ACCESS_TOKEN = '553eb4454779955c5e8de0b2dc2f1d1faa3e112c'
WORKING_DIR_TSCN = os.path.expanduser('~/GithubMover/')
LOG_FILE_PATH = os.path.join(WORKING_DIR_TSCN, 'mover.log')

if not os.path.exists(WORKING_DIR_TSCN):
    os.makedirs(WORKING_DIR_TSCN)

logformat = '%(name)s - %(levelname)s - %(message)s'
formatter = ColoredFormatter(logformat)
stream = TqdmHandler()
stream.setLevel(logging.INFO)
stream.setFormatter(formatter)

file_handler = WatchedFileHandler(filename=os.path.join(WORKING_DIR_TSCN, "githubmover.log"))
file_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO,
                    format=logformat,
                    handlers=[stream, file_handler])
