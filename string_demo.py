#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@author:Hu Yao 
@license: Apache Licence 
@file: string.py 
@time: 2019/05/30
@contact: hooyao@gmail.com
@site:  
@software: PyCharm 
"""

string1 = 'hello my dear friend'
print(string1[0:5])

# string1[0]= 'H'
string2 = '"Special" room service'
print(string2)

string3 = \
    """
Dear friend:

I need to borrow 100 dollars.

Many Thanks and I won't return
"""

print(string3)

string1 += string2  # quite special
print(string1)

list_of_strings = ['I', 'want', 'to', 'drink', 'coca']
print(''.join(list_of_strings))
print(','.join(list_of_strings))

print('room' in string2)

who = 'Pony Ma'

do_what = 'work 996'
print(f'{who} says, you should be happy to {do_what}')
