"""Basic text adventure main menu."""

MENU_WIDTH = 38


def print_button(label: str) -> None:
    print("  ╭" + "─" * MENU_WIDTH + "╮")
    print(f"  │{label:^{MENU_WIDTH}}│")
    print("  ╰" + "─" * MENU_WIDTH + "╯")


def print_menu() -> None:
    print("╭" + "═" * MENU_WIDTH + "╮")
    print(f"│{'TEXT ADVENTURE':^{MENU_WIDTH}}│")
    print(f"│{'Main Menu':^{MENU_WIDTH}}│")
    print("╰" + "═" * MENU_WIDTH + "╯")
    print()
    print_button("1. Start New Game")
    print_button("2. Continue")
    print_button("3. Quit")


def run_menu() -> None:
    while True:
        print_menu()
        choice = input("Choose an option (1-3): ").strip()
        if choice == "1":
            print("Starting a new adventure...")
        elif choice == "2":
            print("No saved adventure was found yet.")
        elif choice == "3":
            print("Goodbye, adventurer!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
        print()


if __name__ == "__main__":
    run_menu()
