from building_types import Residential, Industry, Commercial, Park, Road
from grid import Grid

building_instances = [Residential(), Industry(), Commercial(), Park(), Road()]

def fp_place_building(grid: Grid):
    while True:
        print("\nSelect a building type to place in the city.")
        print("Enter the number that corresponds to the building type to choose.")
        for i, b in enumerate(building_instances):
            print(f"{i + 1}. {b.name} ({b.symbol})")
        print("\n0. Exit")

        option = input(f"\nSelect an option (1-{len(building_instances)}, 0): ")
        match option:
            case "1" | "2" | "3" | "4" | "5":
                building_idx = int(option) - 1
                building_to_place = building_instances[building_idx]

                # get user coordinates and check whether it's possible to place building
                while True:
                    print("\nSelect the coordinates to place the building.")
                    print("To enter the coordinates, type: X, Y")
                    print("The origin (center) of the grid is (0, 0).")
                    print("\nTo return back to building selection, type: ~")
                    print(grid)

                    option = input("\nEnter coordinates: ")
                    # back to building selection
                    if "~" in option:
                        break
                    # handles if decimal or non coordinate values
                    if "." in option or len(option.split(",")) != 2:
                        print("Please enter valid coordinates.")
                        continue
                    option = option.split(",")

                    x, y = int(option[0]), int(option[1])
                    try:
                        b = grid.get(x, y)
                        # building present
                        if b is not None:
                            print(
                                f"There is a {b.name} building at coordinates ({x}, {y})!"
                            )
                            continue
                        grid.set(x, y, building_to_place)
                        break
                    except IndexError as e:
                        # IndexError is raised when x, y are out of bounds
                        print(f"{e}")
                # check if building on the sides, and that the grid should expand
                if grid.has_building_on_border():
                    grid.expand_grid(5)
                break
            case "0":
                break
            case _:
                print("Invalid option. Please try again.")
    return grid


def fp_demolish_building(grid: Grid):
    while True:
        print("\nSelect the coordinates to demolish.")
        print("To enter the coordinates, type: X, Y")
        print("The origin (center) of the grid is (0, 0).")
        print("\nTo return back to the Main Menu, type: ~")
        print(grid)

        option = input("\nEnter coordinates: ")
        # back to building selection
        if "~" in option:
            break
        # handles if decimal or non coordinate valuesd
        if "." in option or len(option.split(",")) != 2:
            print("Please enter valid coordinates.")
            continue
        option = option.split(",")

        x, y = int(option[0]), int(option[1])
        try:
            b = grid.get(x, y)
            # building present
            if b is None:
                print(
                    f"The coordinates ({x}, {y}) are empty!"
                )
                continue
            grid.set(x, y, None)
            break
        except IndexError as e:
            # IndexError is raised when x, y are out of bounds
            print(f"{e}")
    return grid