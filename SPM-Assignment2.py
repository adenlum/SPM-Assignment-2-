import random

import savegame
from arcade import arcade_demolish_building, arcade_place_building
from building_types import Blueprint, Commercial, Industry, Park, Residential, Road
from freeplay import fp_demolish_building, fp_place_building
from grid import Grid
from settings import freeplay_settings, settings_menu


def display_menu():
    print("\n========== MAIN MENU ==========")
    print("1. Arcade Mode")
    print("2. Free Play Mode")
    print("3. Load Game")
    print("4. Settings")
    print("5. High Scores")
    print("0. Exit")


def arcade_mode(grid=None, coins=16, turn=1, score=0):
    print("\nOpening Arcade Mode...")

    if grid is None:
        # Initialize Arcade Mode starting variables
        grid = Grid(size=20)
        print("\nNew Arcade Game Started!")
    else:
        print("\nResuming Arcade Game!")

    building_instances = [Residential(), Industry(), Commercial(), Park(), Road()]

    game_saved = False

    while coins > 0:
        selected_buildings = random.sample(building_instances, 2)

        print("\n===== ARCADE MODE =====")
        print("Board Size: 20 x 20")
        print("Coins:", coins)
        print("Turn:", turn)
        print("Score:", score)

        print("\nCity Board:")
        print(grid)

        print("\nOptions")
        print("1. Place Building")
        if not grid.is_empty():
            print("2. Demolish Building")
        print("3. Place Blueprint")
        if not grid.is_empty():
            print("4. Show Turn Score Preview")
        print("5. Save Game")
        print("0. Exit to Main Menu")

        option = input("\nSelect an option (1-5, 0): ")

        if option == "1":
            arcade_place_building(grid, selected_buildings, turn, "arcade")

            # Use existing grid.py function to calculate score
            score, _ = grid.calculate_turn()

            # Each building construction costs 1 coin
            coins -= 1
            turn += 1

            print("\nUpdated Score:", score)
            print("Coins Left:", coins)
        elif option == "2" and not grid.is_empty():
            coins, demolished = arcade_demolish_building(grid, coins)

            if demolished:
                score, _ = grid.calculate_turn()
                print("\nUpdated Score:", score)
                print("Coins Left:", coins)

        elif option == "3":
            print("\nEnter the number that corresponds to the building type to choose.")
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
                            grid.set(r, c, Blueprint(building_to_place))
                            break
                        except ValueError:
                            print("Please enter valid coordinates.")
                        except IndexError:
                            # IndexError is raised when r, c are out of bounds
                            print("Coordinates entered are out of bounds.")
                case "0":
                    break
        elif option == "4":
            current_score, current_profit = grid.calculate_turn()
            preview = grid.calculate_turn_preview()

            print("\n===== Projected Turn =====")
            print(f"Coins Required: {preview.coins}")
            print(f"Score: {current_score:+} (w/ Blueprints: {preview.score:+})")
            print(f"Profit: {current_profit:+} (w/ Blueprints: {preview.profit:+})")

            if preview.contributions:
                print("\n=== Score Contributions ===")

                for contribution in preview.contributions:
                    name = (
                        f"{contribution['name']} {contribution['status']}"
                        if contribution["status"] == "Blueprint"
                        else f"{contribution['status']} {contribution['name']} "
                    )
                    print(
                        f"{name} ({contribution['row']}, {contribution['col']}) +{contribution['score']}"
                    )

            _ = input("\nPress Enter to continue...")
        elif option == "5":
            filename = input("\nEnter a name to save this game as: ")
            path = savegame.save_game(
                filename, grid, "arcade", coins=coins, turn=turn, score=score
            )
            print(f"\nGame saved to {path}")
            game_saved = True
        elif option == "0":
            print("\nReturning to main menu...")

            if not game_saved:
                name = input("\nEnter your name for the high score board: ")
                savegame.save_high_score(name, score, "arcade")

            return
        else:
            print("Invalid option. Please try again.")

    print("\nGame Over! You have run out of coins.")
    print("Final Score:", score)

    name = input("\nEnter your name for the high score board: ")
    savegame.save_high_score(name, score, "arcade")

    input("\nPress Enter to return to the main menu...")


def free_play_mode(grid=None, turn=1, score=0, turns_with_coin_loss=0, coins=None):
    print("\nOpening Free Play Mode...")
    if grid is None:
        result = settings_menu()
        if result == "exit":
            print("\nReturning to main menu...")
            return
        # initalize the starting variables
        coins = freeplay_settings["starting_coins"]
        grid = Grid(size=5)
        print("\nNew Free Play Game Started!")
    else:
        print("\nResuming Free Play Game!")

    while turns_with_coin_loss < freeplay_settings["coin_loss_limit"]:
        # print routine
        print("\n===== FREE PLAY =====")
        print(f"Board Size: {grid.size} x {grid.size}")
        print("Turn:", turn)
        if coins == -1:
            print("Coins: Unlimited")
        else:
            print("Coins:", coins)
        print("Score:", score)

        current_income, current_profit = grid.calculate_turn(freeplay_settings)
        print(
            "Current Profit:",
            f"{current_profit:+}" if current_profit > 0 else current_profit,
        )
        print(f"Total Upkeep: {current_income - current_profit}")
        print(
            f"Turns With Coin Loss: {turns_with_coin_loss} / {freeplay_settings['coin_loss_limit']}"
        )

        if current_profit < 0:
            print("\n⚠ Warning: Your city is currently losing money!")

        print(grid)
        # turn
        print("\nOptions")
        print("1. Place Building")
        if not grid.is_empty():
            print("2. Demolish Building")
            print("3. Show Turn Score Preview")
        print("4. Save Game")
        print("5. End Current Turn")
        print("0. Exit To Main Menu")
        turn_option = input("\nSelect an option (1-5, 0): ")
        if turn_option == "1":
            if coins == 0:
                print("\nYou don't have enough coins to place a building.")
            else:
                grid = fp_place_building(grid)
                if coins != -1:
                    coins -= 1
        elif turn_option == "2" and not grid.is_empty():
            grid = fp_demolish_building(grid)
        elif turn_option == "3" and not grid.is_empty():
            current_score, current_profit = grid.calculate_turn()
            preview = grid.calculate_turn_preview()

            print("\n===== Projected Turn =====")
            print(f"Coins Required: {preview.coins}")
            print(f"Score: {current_score:+} (w/ Blueprints: {preview.score:+})")
            print(f"Profit: {current_profit:+} (w/ Blueprints: {preview.profit:+})")

            if preview.contributions:
                print("\n=== Score Contributions ===")

                for contribution in preview.contributions:
                    name = (
                        f"{contribution['name']} {contribution['status']}"
                        if contribution["status"] == "Blueprint"
                        else f"{contribution['status']} {contribution['name']} "
                    )
                    print(
                        f"{name} ({contribution['row']}, {contribution['col']}) +{contribution['score']}"
                    )

            _ = input("\nPress Enter to continue...")
        elif turn_option == "4":
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
        elif turn_option == "5":
            end_turn_option = input(
                "Are you sure you want to end the current turn? (y/N): "
            )
            if end_turn_option.upper() == "Y":
                # end of turn
                turn_score, profit = grid.calculate_turn(freeplay_settings)
                print(f"\nProfit this turn: {profit}")
                if coins != -1:
                    coins += profit
                if profit < 0:
                    # if making a loss, add one
                    turns_with_coin_loss += 1
                else:
                    # profit / even = reset the counter
                    turns_with_coin_loss = 0
                score += turn_score
                turn += 1
            continue
        elif turn_option == "0":
            print("\nReturning to main menu...")
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
    print("\n===== TOP 10 HIGH SCORES =====")

    scores = savegame.get_high_scores()

    if not scores:
        print("No high scores recorded yet.")
        return

    for i, entry in enumerate(scores, start=1):
        print(f"{i}. {entry['name']} - {entry['score']} points ({entry['mode']})")

    input("\nPress Enter to return to the main menu...")


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

        choice = input("\nSelect an option (1-5, 0): ")

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
            case "0":
                exit_game()
            case _:
                print("Invalid option. Please try again.")


main()
