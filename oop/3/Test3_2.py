from typing import Optional

class Vehicle:
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

class Car(Vehicle):
    def __init__(self, name: str, seats: int):
        super().__init__(name)
        self._seats = seats
        self._air_conditioner_on = False
        self._trunk_open = False

    def is_air_conditioner_on(self) -> bool:
        return self._air_conditioner_on

    def is_trunk_open(self) -> bool:
        return self._trunk_open

    def turn_on_air_conditioner(self) -> None:
        if not self._air_conditioner_on:
            self._air_conditioner_on = True

    def turn_off_air_conditioner(self) -> None:
        if self._air_conditioner_on:
            self._air_conditioner_on = False

    def open_trunk(self) -> None:
        if not self._trunk_open:
            self._trunk_open = True

    def close_trunk(self) -> None:
        if self._trunk_open:
            self._trunk_open = False

class Bicycle(Vehicle):
    def __init__(self, name: str):
        super().__init__(name)
        self._folded = False

    def is_folded(self) -> bool:
        return self._folded

    def ring(self) -> None:
        print(f"{self._name}: дзынь!")

    def fold(self) -> None:
        if not self._folded:
            self._folded = True

    def unfold(self) -> None:
        if self._folded:
            self._folded = False

class ParkingPlace:
    def __init__(self, identifier: str):
        self._identifier = identifier
        self._occupied_by: Optional[Vehicle] = None

    def park(self, vehicle: Vehicle) -> None:
        if self._occupied_by is None:
            self._occupied_by = vehicle

    def leave(self) -> None:
        if self._occupied_by is not None:
            self._occupied_by = None

class Garage(ParkingPlace):
    def __init__(self, identifier: str, has_heating: bool):
        super().__init__(identifier)
        self._has_heating = has_heating
        self._door_open = False

    def open_door(self) -> None:
        if not self._door_open:
            self._door_open = True

    def close_door(self) -> None:
        if self._door_open:
            self._door_open = False

    def toggle_heating(self) -> None:
        if self._has_heating:
            self._has_heating = False
        else:
            self._has_heating = True

class BikeRack(ParkingPlace):
    def __init__(self, identifier: str, color: str):
        super().__init__(identifier)
        self._locked = False
        self._color = color

    def lock_bike(self) -> None:
        if not self._locked:
            self._locked = True

    def unlock_bike(self) -> None:
        if self._locked:
            self._locked = False

    def get_color(self) -> str:
        return self._color