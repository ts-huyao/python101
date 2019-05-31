#!/usr/bin/env python  
""" 
@author:Hu Yao 
@license: Apache Licence 
@file: exception_handling.py 
@time: 2019/05/30
@contact: hooyao@gmail.com
@site:  
@software: PyCharm 
"""

import json

import requests
from requests import ReadTimeout

urls = ['http://api6.ipify.org?format=json',
        'http://api6.ipify.org?format=json',
        'http://api6.ipify.org?format=json']

for url in urls:
    try:
        response = requests.get(url=url, timeout=0.18)
        ip_data = json.loads(response.text)
        print(ip_data['ip'])
    except ReadTimeout as toe:
        print("time out")
    except Exception as e:
        print("unexpected error")
