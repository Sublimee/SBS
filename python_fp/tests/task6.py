from pymonad.tools import curry
from pymonad.state import State

warehouse_init = {
    'orders': [],
    'stock': {
        'laptop': 3,
        'phone': 5,
        'headphones': 10,
        'keyboard': 4
    }
}

prices = {
    'laptop': 1200,
    'phone': 800,
    'headphones': 150,
    'keyboard': 100
}

warehouse_state = State.insert(warehouse_init['orders'])

@curry(2)
def order(item_key, orders):
    def count_computation(stock):
        new_orders = orders.copy()

        basket_index = next(
            (index for index, order in enumerate(new_orders) if order[0] == item_key),
            None
        )

        if basket_index is None:
            new_orders = new_orders + [(item_key, prices[item_key], 1)]
        else:
            name, price, count = new_orders[basket_index]
            new_orders[basket_index] = (name, price, count + 1)

        new_stock = stock.copy()
        new_stock[item_key] = new_stock[item_key] - 1
        return new_orders, new_stock
    return State(count_computation)


finale = warehouse_state.then(order('phone')).then(order('headphones')).then(order('keyboard')).then(order('phone'))
print(finale.run(warehouse_init['stock']))