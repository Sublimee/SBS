from functools import reduce
from collections import deque


def second_max(nums):
    if len(nums) > 1:
        return reduce(insert, nums, deque(maxlen=2))[1]
    return None

def insert(d, x):
    if len(d) == 0:
        d.appendleft(x)
        return d
    if x >= d[0]:
        d.appendleft(x)
        return d
    if len(d) == 1:
        d.append(x)
        return d
    if x >= d[1]:
        d[1] = x
    return d


print(second_max([1, 2, 3, 4, 5]))  # 4
print(second_max([5, 4, 3, 2, 1]))  # 4
print(second_max([1, 1, 1, 1, 1]))  # 1
print(second_max([5, 4, 3, 2, 5]))  # 5
print(second_max([5, 3, 4]))  # 3
print(second_max([5]))  # None