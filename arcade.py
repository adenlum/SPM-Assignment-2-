from building_types import Blueprint


def arcade_place_building(grid, available_buildings, turn, mode):
    """Allow the player to choose and place a building."""

    print("\nAvailable Buildings:")

    for i, building in enumerate(available_buildings, start=1):
        print(f"{i}. {building.name} ({building.symbol})")

    # Choose building
    while True:
        try:
            choice = int(input(f"\nChoose a building (1-{len(available_buildings)}): "))

            if 1 <= choice <= len(available_buildings):
                building = available_buildings[choice - 1]
                break

            print("Invalid choice.")

        except ValueError:
            print("Please enter a number.")

    # Choose location
    while True:
        try:
            r = int(input("Enter row coordinate: "))
            c = int(input("Enter column coordinate: "))

            # Occupied / out of bounds
            try:
                occupied = grid.get(r, c)
            except IndexError:
                print("Those coordinates are outside the board. Please try again.")
                continue

            if occupied is not None and not isinstance(occupied, Blueprint):
                print("That location is already occupied.")
                continue

            # Arcade rule:
            # Only allow placement anywhere if there's no buildings present
            # otherwise only allow direct adjacent placements
            if grid.has_real_buildings():
                if not grid.direct_adjacent(r, c):
                    print("Building must be adjacent to an existing building.")
                    continue

            grid.set(r, c, building)

            print("\nBuilding placed successfully!")
            print(grid)

            return building, r, c

        except ValueError:
            print("Please enter valid numbers.")


def arcade_demolish_building(grid, coins):
    """Allow the player to demolish an existing building in Arcade Mode for 1 coin."""

    if grid.is_empty():
        print("\nThere are no buildings to demolish.")
        return coins, False

    if coins <= 0:
        print("\nYou do not have enough coins to demolish a building.")
        return coins, False

    while True:
        print("\n===== DEMOLISH BUILDING =====")
        print(grid)
        print("\nEnter the coordinates of the building you want to demolish.")
        print("Type ~ to cancel and return to Arcade Mode.")

        row_input = input("Enter row coordinate: ").strip()
        if row_input == "~":
            print("\nDemolish cancelled.")
            return coins, False

        col_input = input("Enter column coordinate: ").strip()
        if col_input == "~":
            print("\nDemolish cancelled.")
            return coins, False

        try:
            row = int(row_input)
            col = int(col_input)

            building = grid.get(row, col)

            if building is None:
                print(
                    "\nThere is no building at this location. Please choose a cell with a building."
                )
                continue

            if isinstance(building, Blueprint):
                print(
                    "\nThis is a blueprint, not an actual building. Please choose an existing building."
                )
                continue

            while True:
                confirm = (
                    input(
                        f"\nDemolish {building.name} at ({row}, {col}) for 1 coin? (y/N): "
                    )
                    .strip()
                    .upper()
                )

                if confirm == "Y":
                    break

                elif confirm == "N" or confirm == "":
                    print("\nDemolish cancelled.")
                    return coins, False

                else:
                    print("\nInvalid input. Please enter Y to confirm or N to cancel.")

            grid.set(row, col, None)
            coins -= 1

            print(f"\n{building.name} demolished successfully.")
            print("Coins Left:", coins)
            print(grid)

            return coins, True

        except ValueError:
            print("\nPlease enter valid numbers for row and column.")
        except IndexError:
            print("\nThose coordinates are outside the board. Please try again.")
