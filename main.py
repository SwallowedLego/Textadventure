"""Text adventure with locations, encounters, combat, and inventory."""

from __future__ import annotations

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


def show_help() -> None:
    print("Commands: travel, map, fight, inventory, use potion, status, help, quit")


def print_map(current_location: str, locations: dict[str, dict[str, object]]) -> None:
    print("Known locations:")
    for name in locations:
        marker = "(you are here)" if name == current_location else ""
        print(f"- {name} {marker}".rstrip())


def show_inventory(inventory: dict[str, int]) -> None:
    print("Inventory:")
    if not inventory:
        print("- (empty)")
        return
    for item, amount in inventory.items():
        print(f"- {item}: {amount}")


def add_item(inventory: dict[str, int], item: str, amount: int = 1) -> None:
    inventory[item] = inventory.get(item, 0) + amount


def consume_item(inventory: dict[str, int], item: str, amount: int = 1) -> bool:
    current = inventory.get(item, 0)
    if current < amount:
        return False
    if current == amount:
        del inventory[item]
    else:
        inventory[item] = current - amount
    return True


def run_combat(enemy: dict[str, object], stats: dict[str, int], inventory: dict[str, int]) -> bool:
    enemy_name = str(enemy["name"])
    enemy_hp = int(enemy["hp"])
    enemy_attack = int(enemy["attack"])

    print(f"Combat started against {enemy_name}!")

    while enemy_hp > 0 and stats["hp"] > 0:
        print(f"Your HP: {stats['hp']} | {enemy_name} HP: {enemy_hp}")
        action = input("Choose [attack/use potion/run]: ").strip().lower()

        if action == "attack":
            enemy_hp -= stats["attack"]
            print(f"You strike for {stats['attack']} damage.")
        elif action == "use potion":
            if consume_item(inventory, "potion"):
                stats["hp"] = min(stats["max_hp"], stats["hp"] + 12)
                print("You recover 12 HP.")
            else:
                print("You do not have a potion.")
                continue
        elif action == "run":
            print("You cannot escape this fight.")
            continue
        else:
            print("Invalid combat action.")
            continue

        if enemy_hp <= 0:
            print(f"You defeated {enemy_name}!")
            return True

        stats["hp"] -= enemy_attack
        print(f"{enemy_name} hits you for {enemy_attack} damage.")

    print("You were defeated. The adventure ends here.")
    return False


def trigger_location_events(
    location_name: str,
    locations: dict[str, dict[str, object]],
    state: dict[str, set[str]],
    stats: dict[str, int],
    inventory: dict[str, int],
) -> bool:
    location = locations[location_name]
    print(f"\nYou arrive at {location_name}.")
    print(str(location["description"]))

    encounter_id = str(location["encounter_id"])
    if encounter_id not in state["encounters"]:
        print(str(location["encounter_text"]))
        reward = location.get("encounter_reward")
        if reward:
            item_name, amount = reward
            add_item(inventory, str(item_name), int(amount))
            print(f"You obtained {amount} {item_name}.")
        state["encounters"].add(encounter_id)

    combat_id = str(location.get("combat_id", ""))
    if combat_id and combat_id not in state["combats"]:
        if run_combat(dict(location["enemy"]), stats, inventory):
            state["combats"].add(combat_id)
            reward = location.get("combat_reward")
            if reward:
                item_name, amount = reward
                add_item(inventory, str(item_name), int(amount))
                print(f"You looted {amount} {item_name}.")
            return True
        return False

    return True


def play_game() -> None:
    locations: dict[str, dict[str, object]] = {
        "Village Gate": {
            "description": "The safe village edge where your journey starts.",
            "encounter_id": "villager",
            "encounter_text": "A villager hands you supplies before you leave.",
            "encounter_reward": ("potion", 1),
        },
        "Whispering Forest": {
            "description": "Twisted trees and fog hide danger between the roots.",
            "encounter_id": "forest_herbs",
            "encounter_text": "You gather healing herbs under a moonlit oak.",
            "encounter_reward": ("potion", 1),
            "combat_id": "wolf_pack",
            "enemy": {"name": "Wolf Pack", "hp": 18, "attack": 4},
        },
        "Old Bridge": {
            "description": "A cracked bridge stretches over a dark river.",
            "encounter_id": "bridge_cache",
            "encounter_text": "You find a hidden satchel tied under the railing.",
            "encounter_reward": ("bomb", 1),
            "combat_id": "bridge_bandit",
            "enemy": {"name": "Bridge Bandit", "hp": 20, "attack": 5},
        },
        "Crystal Cave": {
            "description": "Blue crystals reflect your lantern light in every direction.",
            "encounter_id": "cave_key",
            "encounter_text": "Behind a crystal pillar you discover an ancient key.",
            "encounter_reward": ("ancient key", 1),
        },
        "Ruined Keep": {
            "description": "Broken stone walls surround the final chamber.",
            "encounter_id": "keep_warning",
            "encounter_text": "Old runes warn: only the prepared survive here.",
            "combat_id": "stone_guardian",
            "enemy": {"name": "Stone Guardian", "hp": 28, "attack": 6},
        },
    }

    stats = {"hp": 30, "max_hp": 30, "attack": 7}
    inventory = {"potion": 1}
    state = {"encounters": set(), "combats": set()}
    current_location = "Village Gate"

    print("Starting a new adventure...")
    if not trigger_location_events(current_location, locations, state, stats, inventory):
        return

    show_help()
    while stats["hp"] > 0:
        if "stone_guardian" in state["combats"] and "ancient key" in inventory:
            print("\nYou unlock the keep's vault with the ancient key and claim victory!")
            return

        command = input("\nWhat do you do? ").strip().lower()

        if command == "help":
            show_help()
        elif command == "map":
            print_map(current_location, locations)
        elif command == "inventory":
            show_inventory(inventory)
        elif command == "status":
            print(f"HP: {stats['hp']}/{stats['max_hp']} | Attack: {stats['attack']}")
        elif command == "use potion":
            if consume_item(inventory, "potion"):
                stats["hp"] = min(stats["max_hp"], stats["hp"] + 12)
                print("You drink a potion and recover 12 HP.")
            else:
                print("You do not have a potion.")
        elif command == "travel":
            print_map(current_location, locations)
            destination = input("Where to? ").strip()
            if destination not in locations:
                print("Unknown destination.")
                continue
            if destination == current_location:
                print("You are already there.")
                continue
            current_location = destination
            if not trigger_location_events(current_location, locations, state, stats, inventory):
                return
        elif command == "fight":
            location = locations[current_location]
            combat_id = str(location.get("combat_id", ""))
            if not combat_id:
                print("There is nothing to fight here.")
            elif combat_id in state["combats"]:
                print("This area is already clear.")
            else:
                if not run_combat(dict(location["enemy"]), stats, inventory):
                    return
                state["combats"].add(combat_id)
        elif command == "quit":
            print("You return home for now.")
            return
        else:
            print("Unknown command. Type 'help' for options.")


def run_menu() -> None:
    while True:
        print_menu()
        choice = input("Choose an option (1-3): ").strip()
        if choice == "1":
            play_game()
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
