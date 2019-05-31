#!/usr/bin/env python  
""" 
@author:Hu Yao 
@license: Apache Licence 
@file: file_io.py 
@time: 2019/05/30
@contact: hooyao@gmail.com
@site:  
@software: PyCharm 
"""

with open('textfile.txt') as f:
    for line in f:
        print(line)

with open('textfile_new.txt', 'w+') as f:
    f.write('你好,\n')
    f.write('这是一个新的文件')

import csv

with open('csvfile.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0:
            print(f'{row[4]} needs to to do task "{row[3]}"')
        line_count += 1

with open('csvfile_new.csv', 'w+') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['huyao', 'rebase backend', 'Open'])
    csv_writer.writerow(['yaohua', 'rebase frontend', 'Open'])
    csv_writer.writerow(['ruiyang', 'rebase proxy', 'Open'])
    csv_writer.writerow(['less', 'rebase tradeshift-it', 'Open'])
    csv_writer.writerow(['Leal', 'rebase apps', 'Open'])
    csv_writer.writerow(['sunrry', 'rebase apps-backend', 'Open'])
