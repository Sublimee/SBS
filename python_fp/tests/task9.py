from functools import reduce


def odometer(oksana):
    def add(state, pair):
        current_speed, current_time = pair
        last_distance, last_time = state
        return last_distance + current_speed * (current_time - last_time), current_time

    distance, _ = reduce(add, list(zip(oksana[::2], oksana[1::2])), (0, 0))
    return distance


print(odometer([10,1,20,2])) # 30
print(odometer([15,1,25,2,30,3,10,5])) # 90
