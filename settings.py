print("SETTINGS FILE IS RUNNING")
FREEPLAY_DEFAULTS = {
    "starting_coins": -1,
    "residential_income": 1,
    "industry_income": 2,
    "commercial_income": 3,
    "expansion_amount": 5,
    "max_map_size": 50,
    "coin_loss_limit": 20
}

freeplay_settings = FREEPLAY_DEFAULTS.copy()

def settings_menu():
    while True:
        print("\n===== FREE PLAY SETTINGS =====")
        print(f"1. Starting Coins : {'Unlimited' if freeplay_settings['starting_coins'] == -1 else freeplay_settings['starting_coins']}")
        print("2. Start Game")

        option = input("Select option: ")

        if option == "1":
            try:
                value = int(input("Enter starting coins (-1 = Unlimited): "))

                if value >= -1:
                    freeplay_settings["starting_coins"] = value
                else:
                    print("Enter -1 or a positive number.")

            except ValueError:
                print("Invalid input.")

        elif option == "2":
            return

        else:
            print("Invalid option.")

print("freeplay_settings exists?", "freeplay_settings" in globals())
print(globals())