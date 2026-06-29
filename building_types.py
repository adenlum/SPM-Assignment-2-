from abc import ABC, abstractmethod


class Building(ABC):
    symbol: str

    @abstractmethod
    def score(self, grid, x: int, y: int):
        pass

    def coins(self, grid, x: int, y: int):
        return 0


class Residential(Building):
    symbol = "R"

    def score(self, grid, x, y):
        # if Residential is adjacent to Industry
        if any(isinstance(b, Industry) for b in grid.direct_adjacent(x, y)):
            return 1

        score = 0
        # Buildings adjacent via Road
        for b in grid.road_adjacent(x, y):
            if isinstance(b, (Residential, Commercial)):
                score += 1
            elif isinstance(b, Park):
                score += 2

        return score


class Industry(Building):
    symbol = "I"

    def score(self, grid, x, y):
        return 1

    def coins(self, grid, x, y):
        return sum(isinstance(b, Residential) for b in grid.road_adjacent(x, y))


class Commercial(Building):
    symbol = "C"

    def score(self, grid, x, y):
        return sum(isinstance(b, Commercial) for b in grid.road_adjacent(x, y))

    def coins(self, grid, x, y):
        return sum(isinstance(b, Residential) for b in grid.road_adjacent(x, y))


class Park(Building):
    symbol = "O"

    def score(self, grid, x, y):
        return sum(isinstance(b, Park) for b in grid.road_adjacent(x, y))


class Road(Building):
    symbol = "*"

    def score(self, grid, x, y):
        score = 1

        # these will loop until there isn't any more road
        # left
        x_left = x - 1
        while isinstance(grid.get(x_left, y), Road):
            score += 1
            x_left -= 1

        # right
        x_right = x + 1
        while isinstance(grid.get(x_right, y), Road):
            score += 1
            x_right += 1

        return score
