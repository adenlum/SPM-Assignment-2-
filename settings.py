settings = {
    "confirm_demolish": True,
    "confirm_end_turn": True
}
def settings_menu(): #printing out settings menu. 
    while True:
        print("\n========== SETTINGS ==========")
        print(f"1. Confirm Before Demolishing : {'ON' if settings['confirm_demolish'] else 'OFF'}")
        print(f"2. Confirm Before Ending Turn : {'ON' if settings['confirm_end_turn'] else 'OFF'}")
        print("3. Reset to Default")
        print("0. Back")