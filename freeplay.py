from building_types import Blueprint, Commercial, Industry, Park, Residential, Road
from grid import Grid
from settings import freeplay_settings

building_instances = [Residential(), Industry(), Commercial(), Park(), Road()]


def fp_place_building(grid: Grid):
    blueprints_enabled = False
    while True:
        print("\n" + "=" * 25)
        print("\nSelect a building type to place in the city.")
        print("\nTo toggle blueprints, enter `B` / `b`. You can place over blueprints.")
        print(
            f"Blueprints are currently: {'ENABLED' if blueprints_enabled else 'DISABLED'}"
        )
        print("\nEnter the number that corresponds to the building type to choose.")
        for i, b in enumerate(building_instances):
            print(f"{i + 1}. {b.name} ({b.symbol})")
        print("\n0. Exit")

        option = input(f"\nSelect an option (1-{len(building_instances)}, B/b, 0): ")
        match option:
            case "1" | "2" | "3" | "4" | "5":
                building_idx = int(option) - 1
                building_to_place = building_instances[building_idx]
                # get user coordinates and check whether it's possible to place building
                while True:
                    print("\nSelect the coordinates to place the building.")
                    print("\nTo return back to building selection, type: ~")
                    print(grid)

                    try:
                        r = input("\nEnter row coordinate: ")
                        if "~" in r:
                            break
                        r = int(r)
                        c = input("Enter column coordinate: ")
                        if "~" in c:
                            break
                        c = int(c)
                        b = grid.get(r, c)
                        # building present
                        if b is not None and not isinstance(b, Blueprint):
                            print(
                                f"There is a {b.name} building at coordinates ({r}, {c})!"
                            )
                            continue
                        grid.set(
                            r,
                            c,
                            Blueprint(building_to_place)
                            if blueprints_enabled
                            else building_to_place,
                        )
                        break
                    except ValueError:
                        print("Please enter valid coordinates.")
                    except IndexError:
                        # IndexError is raised when x, y are out of bounds
                        print("Coordinates entered are out of bounds.")

                # check if building on the sides, and that the grid should expand
                if grid.has_building_on_border():
                    expansion = freeplay_settings["expansion_amount"]
                    max_size = freeplay_settings["max_map_size"]
                    # Only expand if the maximum size hasn't been reached
                    if grid.size < max_size:
                        if grid.size + (expansion * 2) > max_size:
                            expansion = (max_size - grid.size) // 2
                        if expansion > 0:
                            grid.expand_grid(expansion)
                break
            case "0":
                break
            case "B" | "b":
                blueprints_enabled = not blueprints_enabled
            case _:
                print("Invalid option. Please try again.")
    return grid


def fp_demolish_building(grid: Grid):
    while True:
        print("\nSelect the coordinates to demolish.")
        print("\nTo return back to the Main Menu, type: ~")
        print(grid)

        try:
            r = input("\nEnter row coordinate: ")
            if "~" in r:
                break
            r = int(r)
            c = input("Enter column coordinate: ")
            if "~" in c:
                break
            c = int(c)
            b = grid.get(r, c)
            # building present
            if b is None:
                print(f"The coordinates ({r}, {c}) are empty!")
                continue
            grid.set(r, c, None)
            break
        except IndexError as e:
            # IndexError is raised when x, y are out of bounds
            print(f"{e}")
    return grid
