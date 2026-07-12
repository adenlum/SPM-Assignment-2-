from dataclasses import dataclass, field
from typing import Optional

from building_types import Building, Commercial, Industry, Park, Residential, Road


@dataclass
class Grid:
    """Initializes a new grid object, with origin as coordinates (0, 0).
    Grid() should only be called once to be assigned to a variable for example: `grid = Grid(size=5)`
    :param size: The size of the grid. Must be an integer value.
    """

    size: int
    # grid data
    data: list[list[Optional[Building]]] = field(init=False)

    # print method
    def __str__(self) -> str:
        cell_width = 3  # width of every cell, including the label cells

        lines = []

        border = "+" + ("-" * cell_width + "+") * (self.size + 1)  # +1 for the label column
        lines.append(border)

        # header row: blank corner cell + column numbers, each in its own bordered cell
        header = "|" + " " * cell_width + "|"
        for col in range(self.size):
            header += f"{col:^{cell_width}}|"
        lines.append(header)
        lines.append(border)

        for row_idx, row in enumerate(self.data):
            row_str = f"|{row_idx:^{cell_width}}|"
            for cell in row:
                symbol = cell.symbol if cell is not None else "."
                row_str += f"{symbol:^{cell_width}}|"
            lines.append(row_str)
            lines.append(border)

        return "\n".join(lines)


    def __post_init__(self):
        self.data = [[None for _ in range(self.size)] for _ in range(self.size)]

    # used in determining building adjacencies by determining whether a building is connected on continuous road
    # please DO NOT use this outside the class
    def __trace_road(self, row: int, col: int, dr: int, dc: int):
        # move a step towards a direction
        row += dr
        col += dc

        # check if cell is a Road
        if not isinstance(self.safe_get(row, col), Road):
            return None

        while True:
            # continue going in the direction
            row += dr
            col += dc

            cell = self.safe_get(row, col)
            # the road has ended, with nothing beyond it
            if cell is None:
                return None

            # the road has not ended
            if isinstance(cell, Road):
                continue

            # the road has ended, with a building at the end of it
            return cell

    # road adjacency
    def road_adjacent(self, row: int, col: int):
        connected = []
        for dr, dc in [
            (0, 1),  # north
            (0, -1),  # south
            (1, 0),  # east
            (-1, 0),  # west
        ]:
            building = self.__trace_road(row, col, dr, dc)

            # check if a Building is actually found
            if building is not None:
                # follow the road to the building and store it
                nr, nc = row + dr, col + dc
                while isinstance(self.get(nr, nc), Road):
                    nr += dr
                    nc += dc

                connected.append((nr, nc, building))
        return connected

    # building directly beside another building
    def direct_adjacent(self, row: int, col: int):
        connected = []
        for dr, dc in [
            (0, 1),  # north
            (0, -1),  # south
            (1, 0),  # east
            (-1, 0),  # west
        ]:
            # check if a Building is located in that direction
            building = self.safe_get(row + dr, col + dc)

            # check if a Building is actually found
            if building is not None:
                connected.append((row + dr, col + dc, building))
        return connected

    def get(self, row: int, col: int) -> Optional[Building]:
        """Gets a value at a specific coordinate. This value can be a Building or None.
        Raises `IndexError` if the coordinates entered are out of bounds.
        :param row: The row (horizontal) value of the coordinate.
        :param col: The column (vertical) value of the coordinate.
        """
        # out of bounds
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError(f"Coordinates ({row}, {col}) are out of bounds.")

        return self.data[row][col]

    def safe_get(self, row: int, col: int) -> Optional[Building]:
        """Returns a building if inside the grid, otherwise returns None.
        This function differs from `get()` because it cannot distinguish between empty tiles and out of bounds.
        :param row: The row (horizontal) value of the coordinate.
        :param col: The column (vertical) value of the coordinate.
        """
        try:
            return self.get(row, col)
        except IndexError:
            return None

    def set(self, row: int, col: int, value: Building | None):
        """Assigns a provided value at a specific coordinate. Building inserted must be a Building object.
        :param row: The row (horizontal) value of the coordinate.
        :param col: The column (vertical) value of the coordinate.
        :param value: The building object to insert. To remove a building, use None.
        """
        # out of bounds
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError(f"Coordinates ({row}, {col}) are out of bounds.")

        self.data[row][col] = value

    def has_building_on_border(self) -> bool:
        """Returns a boolean True or False depending on whether the grid has a building on its borders."""
        return (
            any(cell is not None for cell in self.data[0])
            or any(cell is not None for cell in self.data[-1])
            or any(row[0] is not None for row in self.data)
            or any(row[-1] is not None for row in self.data)
        )

    def is_empty(self) -> bool:
        """Returns a boolean True or False depending on whether there's a building within the grid."""
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
        for row in range(old_size):
            for col in range(old_size):
                self.data[row + increase][col + increase] = old_grid[row][col]

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
        def __cluster_residential(start_row: int, start_col: int):
            stack = [(start_row, start_col)]
            while stack:
                current_row, current_col = stack.pop()
                if (current_row, current_col) in visited_residential:
                    continue

                # get building and check if its Residential
                try:
                    b = self.get(current_row, current_col)
                except IndexError:
                    continue

                if not isinstance(b, Residential):
                    continue

                visited_residential.add((current_row, current_col))
                for next_row, next_col, b in self.direct_adjacent(
                    current_row, current_col
                ):
                    if isinstance(b, Residential):
                        stack.append((next_row, next_col))

        # clusters Roads within the same row
        def __cluster_road(start_row: int, start_col: int):
            stack = [(start_row, start_col)]

            while stack:
                current_row, current_col = stack.pop()
                if (current_row, current_col) in visited_road:
                    continue

                # get building and check if its Road
                try:
                    b = self.get(current_row, current_col)
                except IndexError:
                    continue

                if not isinstance(b, Road):
                    continue

                visited_road.add((current_row, current_col))

                for dr, dc in [
                    (-1, 0),  # north
                    (1, 0),  # south
                    (0, 1),  # east
                    (0, -1),  # west
                ]:
                    stack.append((current_row + dr, current_col + dc))

        for r in range(self.size):
            for c in range(self.size):
                building = self.get(r, c)

                if building is None:
                    continue

                # score
                score += building.score(self, r, c)

                # income & upkeep
                if isinstance(building, Residential):
                    income += 1

                    # 1 upkeep per connected cluster
                    if (r, c) not in visited_residential:
                        __cluster_residential(r, c)
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
                    if (r, c) not in visited_road:
                        __cluster_road(r, c)
                        upkeep += 1
        return score, income - upkeep
