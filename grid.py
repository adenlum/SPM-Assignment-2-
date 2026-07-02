from dataclasses import dataclass, field
from typing import Optional, Tuple

from building_types import Building, Residential, Industry, Commercial, Park, Road


@dataclass
class Grid:
    """Initializes a new grid object, with origin as coordinates (0, 0).
    Grid() should only be called once to be assigned to a variable for example: `grid = Grid(size=5)`
    :param size: The size of the grid. Must be an integer value.
    """

    size: int
    # grid data
    data: list[list[Optional[Building]]] = field(init=False)

    # origin values, get array index corresponding to origin (coordinates (0, 0))
    origin_x: int = field(init=False)
    origin_y: int = field(init=False)

    # print method
    def __str__(self) -> str:
        rows = []

        for r in self.data:
            rows.append(
                " ".join(cell.symbol if cell is not None else "." for cell in r)
            )
        return "\n".join(rows)

    def __post_init__(self):
        self.data = [[None for _ in range(self.size)] for _ in range(self.size)]
        # center the coordinates
        self.origin_x = self.size // 2
        self.origin_y = self.size // 2

    # helper function to make the grid use coordinates instead of index
    def __to_index(self, x: int, y: int) -> tuple[int, int]:
        return (
            self.origin_y - y,
            self.origin_x + x,
        )

    # used in determining building adjacencies
    # please DO NOT use this outside the class
    def __trace_road(self, x: int, y: int, dx: int, dy: int):
        # returns first building reachable in direction (dx, dy)
        x += dx
        y += dy

        # cell must be road
        if not isinstance(self.get(x, y), Road):
            return None

        while True:
            x += dx
            y += dy

            cell = self.get(x, y)
            if cell is None:
                return None

            if isinstance(cell, Road):
                continue

            return cell

    # road adjacency
    def road_adjacent(self, x: int, y: int):
        connected = []
        for dx, dy in [
            (0, 1),  # north
            (0, -1),  # south
            (1, 0),  # east
            (-1, 0),  # west
        ]:
            building = self.__trace_road(x, y, dx, dy)
            if building is not None:
                nx, ny = x + dx, y + dy
                # follows road
                while isinstance(self.get(nx, ny), Road):
                    nx += dx
                    ny += dy

                connected.append((nx, ny, building))
        return connected

    # building next to building
    def direct_adjacent(self, x: int, y: int):
        connected = []
        for dx, dy in [
            (0, 1),  # north
            (0, -1),  # south
            (1, 0),  # east
            (-1, 0),  # west
        ]:
            building = self.get(x + dx, y + dy)
            if building is not None:
                connected.append((x + dx, y + dy, building))
        return connected

    def get(self, x: int, y: int) -> Optional[Building]:
        """Gets a value at a specific coordinate. This value can be a Building or None.
        Returns None if the coordinates entered are out of bounds.
        :param x: The x-coordinate of the grid coordinate.
        :param y: The y-coordinate of the grid coordinate.
        """
        r, c = self.__to_index(x, y)

        # out of bounds
        if not (0 <= r < self.size and 0 <= c < self.size):
            raise IndexError(f"Coordinates ({x}, {y}) are out of bounds.")

        return self.data[r][c]
        

    def set(self, x: int, y: int, value: Building | None):
        """Assigns a provided value at a specific coordinate. Building inserted must be a Building object.
        :param x: The x-coordinate of the grid coordinate.
        :param y: The y-coordinate of the grid coordinate.
        :param value: The building object to insert. To remove a building, use None.
        """
        r, c = self.__to_index(x, y)

        # out of bounds
        if not (0 <= r < self.size and 0 <= c < self.size):
            raise IndexError(f"Coordinates ({x}, {y}) are out of bounds.")

        self.data[r][c] = value

    def has_building_on_border(self) -> bool:
        """Returns a boolean True or False depending on whether the grid has a building on its borders.
        """
        return (
            any(cell is not None for cell in self.data[0])
            or any(cell is not None for cell in self.data[-1])
            or any(row[0] is not None for row in self.data)
            or any(row[-1] is not None for row in self.data)
        )

    def is_empty(self) -> bool:
        """Returns a boolean True or False depending on whether there's a building within the grid.
        """
        return all(cell is None for row in self.data for cell in row)

    def expand_grid(self, increase: int = 1):
        """Expands the grid by a given integer size in all directions. An increase of 1 increase the grid from a 5x5 to a 7x7.
        :param increase: The size of the increase. Must be an integer value. Defaults to 1 if no value is provided.
        """
        # save data on old grid
        old_grid = self.data
        old_size = self.size

        # initialize new grid size
        self.size += increase * 2
        self.data = [[None for _ in range(self.size)] for _ in range(self.size)]

        # copy data over to the new grid
        for r in range(old_size):
            for c in range(old_size):
                self.data[r + increase][c + increase] = old_grid[r][c]

        # shift origin to match increase in size
        self.origin_x += increase
        self.origin_y += increase

    def calculate_turn(self) -> tuple[int, int]:
        """Calculates the total score and profit (coins) generated from all buildings in a turn.
        The profit can be a negative value if the upkeep of buildings is greater than the income generated.
        :returns: (score, profit)
        """
        score = 0
        income = 0
        upkeep = 0

        visited_residential = set()
        visited_road = set()

        # clusters Residentials within the same cluster
        def __cluster_residential(ix: int, iy: int):
            stack = [(ix, iy)]
            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in visited_residential:
                    continue

                # get building and check if its Residential
                try:
                    b = self.get(cx, cy)
                except IndexError:
                    continue

                if not isinstance(b, Residential):
                    continue

                visited_residential.add((cx, cy))
                for nx, ny, b in self.direct_adjacent(cx, cy):
                    if isinstance(b, Residential):
                        stack.append((nx, ny))

        # clusters Roads within the same row
        def __cluster_road(ix: int, iy: int):
            stack = [(ix, iy)]

            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in visited_road:
                    continue

                # get building and check if its Road
                try:
                    b = self.get(cx, cy)
                except IndexError:
                    continue

                if not isinstance(b, Road):
                    continue

                visited_road.add((cx, cy))
                for dx, dy in [(1, 0), (-1, 0)]:
                    stack.append((cx + dx, cy))

        for r in range(self.size):
            for c in range(self.size):
                # Translate array index back to coordinates safely
                x = c - self.origin_x
                y = self.origin_y - r

                try:
                    building = self.get(x, y)
                except IndexError:
                    continue

                if building is None:
                    continue

                # score
                score += building.score(self, x, y)

                # income & upkeep
                if isinstance(building, Residential):
                    income += 1

                    # 1 upkeep per connected cluster
                    if (x, y) not in visited_residential:
                        __cluster_residential(x, y)
                        upkeep += 1
                elif isinstance(building, Industry):
                    income += 2
                    upkeep += 1
                elif isinstance(building, Commercial):
                    income += 3
                    upkeep += 2
                elif isinstance(building, Park):
                    upkeep += 1
                elif isinstance(building, Road):
                    if (x, y) not in visited_road:
                        __cluster_road(x, y)
                        upkeep += 1
        return score, income - upkeep
