from enum import Enum
from typing import List, Optional

class CellType(Enum):
    LAND = "land"
    WATER = "water"

class Cell:
    def __init__(self, x: int, y: int, cell_type: CellType):
        self.__x = x
        self.__y = y
        self._cell_type = cell_type

    def get_coords(self) -> tuple[int, int]:
        return self.__x, self.__y

    def get_type(self) -> CellType:
        return self._cell_type


class WaterCell(Cell):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, CellType.WATER)


class LandCell(Cell):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, CellType.LAND)

class GameMap:
    def __init__(self, name: str, width: int, height: int, cells: List[Cell], description: str):
        self.__name = name
        self.__width = width
        self.__height = height
        self.__cells = cells
        self.__description = description

    def get_optional_cell(self, x: int, y: int) -> Optional[Cell]:
        for cell in self.__cells:
            coords = cell.get_coords()
            if coords[0] == x and coords[1] == y:
                return cell
        return None

    def get_cell(self, x: int, y: int) -> Cell:
        cell = self.get_optional_cell(x, y)
        if cell is None:
            raise ValueError(f"No cell at ({x}, {y})")
        return cell

    def get_area(self) -> int:
        return self.__width * self.__height

    def is_water(self, x: int, y: int) -> bool:
        return self.get_cell(x, y).get_type() == CellType.WATER

    def is_land(self, x: int, y: int) -> bool:
        return self.get_cell(x, y).get_type() == CellType.LAND

    def print_map(self):
        for y in range(self.__height):
            for x in range(self.__width):
                if self.__cells[y * self.__width + x].get_type() == CellType.LAND:
                    print('L', end='')
                else:
                    print('W', end='')
            print('')
