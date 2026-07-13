from abc import ABC, abstractmethod


# abstract class that buildings used, should NOT be initialized on its own
class Building(ABC):
    name: str
    symbol: str

    @abstractmethod
    def score(self, grid, row: int, col: int):
        pass

    def income(self, grid, row: int, col: int):
        return 0


class Residential(Building):
    name = "Residential"
    symbol = "R"

    def score(self, grid, row, col):
        # if Residential is adjacent to Industry, force score to 1 point
        if any(isinstance(b, Industry) for _, _, b in grid.direct_adjacent(row, col)):
            return 1

        score = 0
        # Buildings adjacent via Road, 1 point per Residential / Commerical and 2 points per Park
        for _, _, b in grid.road_adjacent(row, col):
            if isinstance(b, (Residential, Commercial)):
                score += 1
            elif isinstance(b, Park):
                score += 2

        return score


class Industry(Building):
    name = "Industry"
    symbol = "I"

    # Each industry scores 1 point multiplied by the number of Industry buildings in the grid
    def score(self, grid, row, col):
        return sum(
            isinstance(b, Industry)
            for row in grid.data
            for b in row
        )

    # Each Industry generates 1 coin per Residential building adjacent
    def income(self, grid, row, col):
        return sum(isinstance(b, Residential) for _, _, b in grid.road_adjacent(row, col))


class Commercial(Building):
    name = "Commercial"
    symbol = "C"

    # Commerical scores 1 point per adjacent Commercial building
    def score(self, grid, row, col):
        return sum(isinstance(b, Commercial) for _, _, b in grid.road_adjacent(row, col))

    # Each Commerical generates 1 coin per Residential building adjacent
    def income(self, grid, row, col):
        return sum(isinstance(b, Residential) for _, _, b in grid.road_adjacent(row, col))


class Park(Building):
    name = "Park"
    symbol = "O"

    # Park scores 1 point per adjacent Park building
    def score(self, grid, row, col):
        return sum(isinstance(b, Park) for _, _, b in grid.road_adjacent(row, col))


class Road(Building):
    name = "Road"
    symbol = "*"

    # Roads score 1 point per connected road within the same row.
    def score(self, grid, row, col):
        score = 1

        # these will loop until there isn't any more road
        # left
        x_left = row - 1
        while isinstance(grid.safe_get(x_left, col), Road):
            score += 1
            x_left -= 1

        # right
        x_right = row + 1
        while isinstance(grid.safe_get(x_right, col), Road):
            score += 1
            x_right += 1

        return score
