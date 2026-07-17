import random
import savegame
from building_types import Commercial, Industry, Park, Residential, Road
from freeplay import fp_demolish_building, fp_place_building
from grid import Grid


def display_menu():
    print("\n========== MAIN MENU ==========")
    print("1. Arcade Mode")
    print("2. Free Play Mode")
    print("3. Load Game")
    print("4. Settings")
    print("5. High Scores")
    print("6. Exit")


def has_adjacent_building(grid, x, y):
    """Check whether the selected cell is directly beside an existing building."""
    try:
        return len(grid.direct_adjacent(x, y)) > 0
    except IndexError:
        return False


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

            # Occupied / out of bounds
            try:
                occupied = grid.get(x, y) is not None
            except IndexError:
                print("Those coordinates are outside the board. Please try again.")
                continue

            if occupied:
                print("That location is already occupied.")
                continue

            # Arcade rule:
            # Turn 1 can build anywhere
            # Turn 2 onwards must be adjacent
            if mode == "arcade" and turn > 1:
                if not has_adjacent_building(grid, x, y):
                    print("Building must be adjacent to an existing building.")
                    continue

            grid.set(x, y, building)

            print("\nBuilding placed successfully!")
            print(grid)

            return building, x, y

        except ValueError:
            print("Please enter valid numbers.")


def arcade_mode(grid=None, coins=16, turn=1, score=0):
    print("\nOpening Arcade Mode...")

    if grid is None:
        # Initialize Arcade Mode starting variables
        grid = Grid(size=20)
        print("\nNew Arcade Game Started!")
    else:
        print("\nResuming Arcade Game!")

    building_types = [Residential, Industry, Commercial, Park, Road]

    while coins > 0:
        selected_buildings = random.sample(building_types, 2)

        print("\n===== ARCADE MODE =====")
        print("Board Size: 20 x 20")
        print("Coins:", coins)
        print("Turn:", turn)
        print("Score:", score)

        print("\nCity Board:")
        print(grid)

        print("\nOptions")
        print("1. Build a Building")
        print("2. Save Game")
        print("3. Exit to Main Menu")

        option = input("\nSelect an option: ")

        if option == "1":
            place_building(grid, selected_buildings, turn, "arcade")

            # Use existing grid.py function to calculate score
            score, _ = grid.calculate_turn()

            # Each building construction costs 1 coin
            coins -= 1
            turn += 1

            print("\nUpdated Score:", score)
            print("Coins Left:", coins)

        elif option == "2":
            filename = input("\nEnter a name to save this game as: ")
            path = savegame.save_game(
                filename, grid, "arcade", coins=coins, turn=turn, score=score
            )
            print(f"\nGame saved to {path}")

        elif option == "3":
            print("\nReturning to main menu...")
            return

        else:
            print("Invalid option. Please try again.")

    print("\nGame Over! You have run out of coins.")
    print("Final Score:", score)
    input("\nPress Enter to return to the main menu...")


def free_play_mode(grid=None, turn=1, score=0, turns_with_coin_loss=0):
    print("\nOpening Free Play Mode...")
    if grid is None:
        # initalize the starting variables
        grid = Grid(size=5)
        print("\nNew Free Play Game Started!")
    else:
        print("\nResuming Free Play Game!")
    while turns_with_coin_loss < 20:
        # print routine
        print("\n===== FREE PLAY =====")
        print(f"Board Size: {grid.size} x {grid.size}")
        print("Turn:", turn)
        print("Score:", score)
        print(f"Turns With Coin Loss: {turns_with_coin_loss} / 20")

        print(grid)

        # turn
        print("\nOptions")
        print("1. Place Building")
        if not grid.is_empty():
            print("2. Demolish Building")
        print("3. Settings")
        print("4. Save Game")
        print("5. End Current Turn")
        print("0. Exit")
        turn_option = input("\nSelect an option (1-5, 0): ")
        if turn_option == "1":
            grid = fp_place_building(grid)
        if turn_option == "2" and not grid.is_empty():
            grid = fp_demolish_building(grid)
        if turn_option == "3":
            print("Feature has not been implemented yet!")
        if turn_option == "4":
            filename = input("\nEnter a name to save this game as: ")
            path = savegame.save_game(
                filename,
                grid,
                "freeplay",
                turn=turn,
                score=score,
                turns_with_coin_loss=turns_with_coin_loss,
            )
            print(f"\nGame saved to {path}")
        if turn_option == "5":
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
        if turn_option == "0":
            return
        else:
            print("Invalid option. Please try again.")
    print("===== Game Over =====")
    print(f"You lasted for {turn} turns.")
    print("Final Score:", score)


def load_game():
    print("\nOpening Load Game...")

    saves = savegame.list_saves()

    if not saves:
        print("No saved games found.")
        return

    print("\nSaved Games:")
    for i, name in enumerate(saves, start=1):
        print(f"{i}. {name}")

    choice = input(f"\nSelect a save to load (1-{len(saves)}), or 0 to cancel: ")

    try:
        choice = int(choice)
    except ValueError:
        print("Please enter a number.")
        return

    if choice == 0:
        print("\nReturning to main menu...")
        return

    if not (1 <= choice <= len(saves)):
        print("Invalid choice.")
        return

    filename = saves[choice - 1]

    try:
        mode, grid, state = savegame.load_game(filename)
    except FileNotFoundError:
        print("Save file not found.")
        return

    if mode == "arcade":
        arcade_mode(grid, **state)
    elif mode == "freeplay":
        free_play_mode(grid, **state)
    else:
        print(f"Unknown save mode: {mode}")


def settings():
    print("\nOpening Settings...")


def high_scores():
    print("\nOpening High Scores...")


def exit_game():
    confirm = input("\nAre you sure you want to exit the game? (y/N): ")

    if confirm.upper() == "Y":
        print("\nThank you for playing!")
        exit()
    else:
        print("\nReturning to main menu...")


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
