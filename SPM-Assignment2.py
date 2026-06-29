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


def free_play_mode():
    print("\nOpening Free Play Mode...")


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

        if choice == "1":
            arcade_mode()

        elif choice == "2":
            free_play_mode()

        elif choice == "3":
            load_game()

        elif choice == "4":
            settings()

        elif choice == "5":
            high_scores()

        elif choice == "6":
            exit_game()

        else:
            print("Invalid option. Please try again.")


main()