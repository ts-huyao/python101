#!/usr/bin/env python  
""" 
@author:Hu Yao 
@license: Apache Licence 
@file: control_flow.py 
@time: 2019/05/30
@contact: hooyao@gmail.com
@site:  
@software: PyCharm 
"""

# condition

print(1 > 2)

a = 3
b = 4

print(a < b)
print(a < b and 1 > 2)

if a > 2:
    print('a>2')
else:
    print('a<=2')

person=0
while person < 100:
    print("hello buddy")
    person+=1

for i in range(5):
    print(i)

print(range(5))
print(list(range(5)))

dict1 = {'a': 1, 'b': 2, 'c': 3}

for key, value in dict1.items():
    print(f'key:{key}  value:{value}')

list1 = ['a', 'b', 'c']

for idx, value in enumerate(list1):
    print(f'idx:{idx} value:{value}')
