import random

from building_types import Commercial, Industry, Park, Residential, Road
from grid import Grid


def display_menu():
    print("\n========== MAIN MENU ==========")
    print("1. Arcade Mode")
    print("2. Free Play Mode")
    print("3. Load Game")
    print("4. Settings")
    print("5. High Scores")
    print("6. Exit")


def place_building(grid, available_buildings, turn, mode):
    """Allow the player to choose and place a building."""

    print("\nAvailable Buildings:")

    for i, building in enumerate(available_buildings, start=1):
        print(f"{i}. {building.symbol}")

    # Choose building
    while True:
        try:
            choice = int(input("\nChoose a building: "))

            if 1 <= choice <= len(available_buildings):
                building = available_buildings[choice - 1]()
                break

            print("Invalid choice.")

        except ValueError:
            print("Please enter a number.")

    # Choose location
    while True:
        try:
            x = int(input("Enter X coordinate: "))
            y = int(input("Enter Y coordinate: "))

            # Occupied
            if grid.get(x, y) is not None:
                print("That location is already occupied.")
                continue

            # Arcade rule:
            # Turn 1 can build anywhere
            # Turn 2 onwards must be adjacent
            if mode == "arcade" and turn > 1:
                if len(grid.direct_adjacent(x, y)) == 0:
                    print("Building must be adjacent to an existing building.")
                    continue

            grid.set(x, y, building)

            print("\nBuilding placed successfully!")
            print(grid)

            return building, x, y

        except ValueError:
            print("Please enter valid numbers.")


def arcade_mode():
    print("\nOpening Arcade Mode...")

    # initialize Arcade Mode starting variables
    grid = Grid(size=20)
    coins = 16
    turn = 1
    score = 0

    # Building types available in Arcade Mode
    building_types = [Residential, Industry, Commercial, Park, Road]

    # Randomly select two buildings for the first turn
    selected_buildings = random.sample(building_types, 2)

    print("\nNew Arcade Game Started!")
    print("Board Size: 20 x 20")
    print("Coins:", coins)
    print("Turn:", turn)
    print("Score:", score)

    print("\nCity Board:")
    print(grid)
    building, x, y = place_building(grid, selected_buildings, turn, "arcade")

    score += building.score(grid, x, y)
    coins -= 1

    print("\nScore:", score)
    print("Coins:", coins)

    input("\nPress Enter to return to the main menu...")


def free_play_mode():
    def place_building_fp(g: Grid):
        building_instances = [Residential(), Industry(), Commercial(), Park(), Road()]

        while True:
            print("\nSelect a building type to place:")
            for i, b in enumerate(building_instances):
                print(f"{i + 1}. {b.name} ({b.symbol})")

            option = input("\nSelect an option (1-5, 0): ")
            match option:
                case "1" | "2" | "3" | "4" | "5":
                    building_idx = int(option) - 1
                    building_to_place = building_instances[building_idx]

                    # get user coordinates and check whether it's possible to place building
                    while True:
                        print("\nSelect the coordinates to place the building.")
                        print("To enter the coordinates, type: X, Y")
                        print("The origin (center) of the grid is (0, 0).")
                        print(g)

                        option = input("\nEnter coordinates: ")
                        # handles if decimal or non coordinate values
                        if "." in option or len(option.split(",")) != 2:
                            print("Please enter valid coordinates.")
                            continue
                        option = option.split(",")

                        x, y = int(option[0]), int(option[1])
                        try:
                            b = g.get(x, y)
                            # building present
                            if b is not None:
                                print(
                                    f"There is a {b.name} building at coordinates ({x}, {y})!"
                                )
                                continue
                            g.set(x, y, building_to_place)
                            break 
                        except IndexError as e:
                            # IndexError is raised when x, y are out of bounds
                            print(f"{e}")
                    # check if building on the sides, and that the grid should expand
                    if g.has_building_on_border():
                        g.expand_grid(5)
                    break
                case "0":
                    break
                case _:
                    print("Invalid option. Please try again.")
        return g

    print("\nOpening Free Play Mode...")
    # initalize the starting variables
    grid = Grid(size=5)
    turn = 1
    score = 0
    turns_with_coin_loss = 0
    # init game
    print("\nNew Free Play Game Started!")
    while turns_with_coin_loss < 20:
        # print routine
        print("===== Main Menu =====")
        print(f"\nBoard Size: {grid.size} x {grid.size}")
        print("Turn:", turn)
        print("Score:", score)

        print(grid)

        # turn
        print("\nOptions")
        print("1. Place Building")
        print("2. Demolish Building")
        print("3. Settings")
        print("4. Save Game")
        print("5. End Current Turn")
        print("0. Exit")
        turn_option = input("\nSelect an option (1-5, 0): ")
        match turn_option:
            case "1":
                grid = place_building_fp(grid)
            case "2":
                pass
            case "3":
                pass
            case "4":
                pass
            case "5":
                end_turn_option = input(
                    "Are you sure you want to end the current turn? (y/N): "
                )
                if end_turn_option.upper() == "Y":
                    # end of turn
                    turn_score, profit = grid.calculate_turn()
                    if profit < 0:
                        # if making a loss, add one
                        turns_with_coin_loss += 1
                    else:
                        # profit / even = reset the counter
                        turns_with_coin_loss = 0
                    score += turn_score
                    turn += 1
                continue
            case "0":
                return
            case _:
                print("Invalid option. Please try again.")


def load_game():
    print("\nOpening Load Game...")


def settings():
    print("\nOpening Settings...")


def high_scores():
    print("\nOpening High Scores...")


def exit_game():
    confirm = input("\nAre you sure you want to exit the game? (Y/N): ")

    if confirm.upper() == "Y":
        print("\nThank you for playing!")
        exit()
    elif confirm.upper() == "N":
        print("\nReturning to main menu...")
    else:
        print("\nInvalid input. Returning to main menu...")


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
