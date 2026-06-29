import random

from building_types import (
    Residential, Industry, Commercial, Park, Road
)
from grid import Grid


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

    print("\nAvailable buildings for this turn:")
    print("1.", selected_buildings[0].symbol)
    print("2.", selected_buildings[1].symbol)

    print("\nCity Board:")
    print(grid)

    input("\nPress Enter to return to the main menu...")


def free_play_mode():
    print("\nOpening Free Play Mode...")
    # initalize the starting variables
    grid = Grid(size=5)
    grid.expand_grid() # should be a 7x7
    # example use below
    grid.set(0, 0, Commercial())
    print(grid)


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
