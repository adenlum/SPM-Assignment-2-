from dataclasses import dataclass, field

# initializes a grid, with origin as coordinates (0, 0)
# origin is defined as the center of the grid.
@dataclass
class Grid:
    """Initializes a new grid object. Grid() should only be called once to be assigned to a variable for example: `grid = Grid(size=5)`
    :param size: The size of the grid. Must be an integer value.
    :type size: int
    """
    size: int
    # grid data
    data: list[list[str | None]] = field(init=False)

    # origin values, get array index corresponding to origin (coordinates (0, 0))
    origin_x: int = field(init=False)
    origin_y: int = field(init=False)

    # print method
    def __str__(self) -> str:
        rows = []

        for r in self.data:
            rows.append(
                " ".join(
                    str(cell) if cell is not None else "."
                    for cell in r
                )
            )
        return "\n".join(rows)


    def __post_init__(self):
        self.data = [
            [None for _ in range(self.size)]
            for _ in range(self.size)
        ]
        # center the coordinates
        self.origin_x = self.size // 2
        self.origin_y = self.size // 2

    # helper function to make the grid use coordinates instead of index
    # please DO NOT use this outside the class
    def __to_index(self, x: int, y: int) -> tuple[int, int]:
        return (
            self.origin_y - y,
            self.origin_x + x,
        )

    def get_value_at_coord(self, x: int, y: int) -> str | None:
        """Gets a value at a specific coordinate. This value can be a string or None.
        """
        r, c = self.__to_index(x, y)
        return self.data[r][c]

    def set_value_at_coord(self, x: int, y: int, value):
        """Assigns a provided value at a specific coordinate.
        """
        r, c = self.__to_index(x, y)
        self.data[r][c] = value

    def expand_grid(self, increase: int = 1):
        """Expands the grid by a given integer size in all directions.
        :param increase: The size of the increase. Must be an integer value. Defaults to 1 if no value is provided.
        :type increase: int
        """
        # save data on old grid
        old_grid = self.data
        old_size = self.size

        # initialize new grid size
        self.size += increase * 2
        self.data = [
            [None for _ in range(self.size)]
            for _ in range(self.size)
        ]

        # copy data over to the new grid
        for r in range(old_size):
            for c in range(old_size):
                self.data[r + increase][c + increase] = old_grid[r][c]

        # shift origin to match increase in size
        self.origin_x += increase
        self.origin_y += increase

def display_menu():
    print("\n========== MAIN MENU ==========")
    print("1. Arcade Mode")
    print("2. Free Play Mode")
    print("3. Load Game")
    print("4. Settings")
    print("5. High Scores")
    print("6. Exit")


def arcade_mode():
    print("\nOpening Arcade Mode...")
#arcade mode


def free_play_mode():
    print("\nOpening Free Play Mode...")


    # initalize the starting variables
    grid = Grid(size=20)
    # example access
    print(grid)



def load_game():
    print("\nOpening Load Game...")


def settings():
    print("\nOpening Settings...")


def high_scores():
    print("\nOpening High Scores...")


def exit_game():
    print("\nThank you for playing!")
    exit()


def main():
    while True:
        display_menu()

        choice = input("\nSelect an option (1-6): ")

        match choice:
            case "1":
                arcade_mode()
            case "2":
                free_play_mode()
            case "3":
                load_game()
            case "4":
                settings()
            case "5":
                high_scores()
            case "6":
                exit_game()
            case _:
                print("Invalid option. Please try again.")

main()