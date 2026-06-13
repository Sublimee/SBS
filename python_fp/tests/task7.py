from pymonad.tools import curry
from pymonad.state import State
from pymonad.list import ListMonad
from functools import reduce
from operator import add


N = 3
M = 4
L = 2

campaign_init = {
    'days': 1,
    'battalion': [2,2, 3,4]
}

enemies_cells = lambda x: ListMonad(
    (x[0] + 1, x[1]),
    (x[0], x[1] - 1),
    (x[0], x[1] + 1),
    (x[0] - 1, x[1]),
)

if_valid = lambda x: ListMonad( (x[0], x[1]) ) if 1 <= x[0] <= N and 1 <= x[1] <= M else ListMonad()

attack = (lambda pos: ListMonad(pos).bind(enemies_cells).bind(if_valid))


# так как результатом работы compute() в конечном счете должна быть пара (результат, новое состояние), то у нас нет
# вариантов, кроме как делать (и проверять на удовлетворение условию) промежуточные вычисления до тех пор, как не
# получим эту пару (финальный результат). Значит возвращаться из compute() должна либо искомая пара, либо результат
# вызова compute() на значениях очередного шага (return battle(days + 1).run(result_battalion))
@curry(1)
def battle(days):
    def compute(battalion):
        original_battalion = battalion.copy()
        original_cells = list(set(zip(original_battalion[::2], original_battalion[1::2])))

        if len(original_cells) == N * M:
            return days, battalion


        result_cells = list(set(list(ListMonad(*original_cells).bind(attack)) + original_cells))
        result_battalion = list(reduce(add, result_cells, ()))
        return battle(days + 1).run(result_battalion)
    return State(compute)

print(battle(campaign_init['days']).run(campaign_init['battalion']))
