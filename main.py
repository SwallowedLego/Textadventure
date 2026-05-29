"""Basic text adventure main menu."""


def print_menu() -> None:
    border = "+" + "-" * 32 + "+"
    print(border)
    print("|{:^32}|".format("TEXT ADVENTURE"))
    print("|{:^32}|".format("Main Menu"))
    print(border)
    print("| 1) Start Game                  |")
    print("| 2) Help                        |")
    print("| 3) Quit                        |")
    print(border)


def run_menu() -> None:
    while True:
        print_menu()
        choice = input("Choose an option (1-3): ").strip()
        if choice == "1":
            print("Your adventure begins soon...")
        elif choice == "2":
            print("Pick options by typing their number and pressing Enter.")
        elif choice == "3":
            print("Goodbye, adventurer!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
        print()


if __name__ == "__main__":
    run_menu()
