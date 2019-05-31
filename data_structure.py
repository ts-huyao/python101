#!/usr/bin/env python  
""" 
@author:Hu Yao 
@license: Apache Licence 
@file: data_structure.py 
@time: 2019/05/30
@contact: hooyao@gmail.com
@site:  
@software: PyCharm 
"""

# Variables
import heapq

a = 1
b = 1
c = a
d = b * 2

print(f"a={a} b={b} c={c} d={d}")

tp = (1, 2, 3, 4)
lst = [1, 2, 3, 4]

# index starts from 0
print(str(tp[0]))
print(str(lst[0]))

tp1 = (1, 2, '3', '4')
print(str(tp1))

lst1 = [1, 2, '3', '4']
print(str(lst1))

print(tp1[2])
print(lst1[2])

# immutable
# tp1[2] = 1
lst1[2] = '3333'

print(str(lst1))

# slicing

lst2 = [1, 2, 3, 4, 5, 6]
print(lst2[1:4])
print(lst2[-1])
print(lst2[3:])

lst4 = [2, 3, 4, 5, 9, 7, 8]
print(sorted(lst4))
print(lst4)
lst4.sort()  # in place sort
print(lst4)

# heap

min_heap = []
heapq.heappush(min_heap, 4)
heapq.heappush(min_heap, 3)
heapq.heappush(min_heap, 5)
heapq.heappush(min_heap, 8)
heapq.heappush(min_heap, 6)

print(min_heap)
print(heapq.heappop(min_heap))
print(heapq.heappop(min_heap))
print(heapq.heappop(min_heap))
print(heapq.heappop(min_heap))
print(heapq.heappop(min_heap))

# dict
dict1 = {'huyao': 1000, 'tim': 2000, 'lewis': 3000}
print(dict1['tim'])
print(dict1.get('chris'))
#print(dict1['f'])
#dict1[0]

# set

set_a = set()
set_a.add("the")
set_a.add("quick")
set_a.add("brown")
set_a.add("fox")

set_b = set()
set_b.add("jumps")
set_b.add("over")
set_b.add("the")
set_b.add("lazy")
set_b.add("dog")

print(set_a.union(set_b))
print(set_a.intersection(set_b))
