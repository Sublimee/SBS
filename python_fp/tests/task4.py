from pymonad.tools import curry
from pymonad.maybe import Just, Nothing
from pymonad.list import ListMonad

# Задание
@curry(2)
def add(x, y):
    return x + y

# def add10(x):
#     return Maybe.apply(add).to_arguments(x, Just(10))
#
# print(add10(Just(3)))

def add10(x):
    return x.map(add(10))

print(add10(Just(3)))
print(add10(Nothing))
print(add10(ListMonad(1,2,3,4)))