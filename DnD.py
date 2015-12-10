"""
    D&D Text-based game
"""

__author__ = "tektx"

import pymysql
import math
from collections import OrderedDict

db_conn = pymysql.connect(user='root', password='password', database='dnd')
cursor = db_conn.cursor()


def new_game_ability_scores(name, mode, points, abilities):
    max_score = 18
    min_score = 3
    count = 0
    ability_dict = {}
    modifier_dict = {}
    print("\nAbility scores")
    for ability in abilities:
        # Calculate the modifier
        modifier = math.floor((abilities[ability] - 10) / 2)
        print(str(count) + ") " + str(ability) + ": " + str(abilities[ability]) + " (" + str(modifier) + ")")

        # Calculate the cost of raising/lowering ability score
        if mode == "add":
            modifier_dict[count] = 1 if abilities[ability] < 13 else math.floor((abilities[ability] - 11) / 2) + 1
        else:
            modifier_dict[count] = 1 if abilities[ability] < 13 else math.floor((abilities[ability] - 12) / 2) + 1

        ability_dict[count] = str(ability)
        count += 1

    print("Points remaining: " + str(points))
    print("Type + or - to switch to 'Add' or 'Subtract' mode respectively")
    print("Type a number to modify that ability score")
    print("Type 'done' to exit screen")
    print("Current mode is '" + mode + "'")
    choice = input("? ")

    if choice == "-":
        new_game_ability_scores(name, "subtract", points, abilities)
    elif choice == "+":
        new_game_ability_scores(name, "add", points, abilities)

    # Insert the ability scores
    elif choice == "done":
        inserts = "INSERT INTO player (name, ability_str, ability_dex, ability_con, ability_wis, ability_int," \
                  "ability_cha)"
        values = "('" + name + "', " + str(abilities['STR']) + ", " + str(abilities['DEX']) + ", " +\
                 str(abilities['CON']) + ", " + str(abilities['WIS']) + ", " + str(abilities['INT']) + ", " +\
                 str(abilities['CHA']) + ");"
        cursor.execute(inserts + " VALUES " + values)

    # Test that provided value is an integer
    try:
        if int(choice) < len(abilities):
            # Add points
            if mode == "add":
                if points >= modifier_dict[int(choice)]:
                    if abilities[str(ability_dict[int(choice)])] < max_score:
                        abilities[str(ability_dict[int(choice)])] += 1
                        points -= modifier_dict[int(choice)]
                        new_game_ability_scores(name, mode, points, abilities)
                    else:
                        print("\n! - Ability score can't exceed " + str(max_score))
                        new_game_ability_scores(name, mode, points, abilities)
                else:
                    print("\n! - Not enough points remaining to be allocated")
                    new_game_ability_scores(name, mode, points, abilities)
            # Remove points
            elif mode == "subtract":
                if abilities[str(ability_dict[int(choice)])] > min_score:
                    abilities[str(ability_dict[int(choice)])] -= 1
                    points += modifier_dict[int(choice)]
                    new_game_ability_scores(name, mode, points, abilities)
                else:
                    print("\n! - Ability score can't be lower than " + str(min_score))
                    new_game_ability_scores(name, mode, points, abilities)
            else:
                new_game_ability_scores(name, "add", points, abilities)

        # A value outside of the ability score range was provided
        else:
            print("\n! - Invalid choice")
            new_game_ability_scores(name, mode, points, abilities)
    except ValueError:
        print("\n! - Invalid choice")
        new_game_ability_scores(name, mode, points, abilities)


def new_game_race():
    count = 0
    list_races = ['Human', 'Halfling', 'Dwarf', 'High Elf', 'Half-orc', 'Half-elf', 'Gnome']

    print("\nChoose your race")
    for choice in list_races:
        print(str(count) + ": " + choice)
        count += 1

    choice = int(input("Race: "))
    if choice < len(list_races):
        return list_races[choice]
    else:
        print("\n! - Invalid choice")
        new_game_race()


def new_game_class():
    count = 0
    list_classes = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue',
                    'Sorcerer', 'Wizard']

    print("\nChoose your class")
    for choice in list_classes:
        print(str(count) + ": " + choice)
        count += 1

    choice = int(input("Class: "))
    if choice < len(list_classes):
        return list_classes[choice]
    else:
        print("\n! - Invalid choice")
        new_game_class()


def new_game_alignment():
    count = 0
    list_alignments = ['Lawful Good', 'Neutral Good', 'Chaotic Good',
                       'Lawful Neutral', 'True Neutral', 'Chaotic Neutral',
                       'Lawful Evil', 'Neutral Evil', 'Chaotic Evil']

    print("\nChoose your alignment")
    for choice in list_alignments:
        print(str(count) + ": " + choice)
        count += 1

    choice = int(input("Alignment: "))
    if choice < len(list_alignments):
        return list_alignments[choice]
    else:
        print("\n! - Invalid choice")
        new_game_alignment()


def new_game_info():
    ability_points = 22
    ability_scores = OrderedDict()
    ability_scores['STR'] = 10
    ability_scores['DEX'] = 10
    ability_scores['CON'] = 10
    ability_scores['WIS'] = 10
    ability_scores['INT'] = 10
    ability_scores['CHA'] = 10

    # Create the character
    player_name = input("Choose your name: ")
    player_race = new_game_race()
    player_class = new_game_class()
    player_alignment = new_game_alignment()
    new_game_ability_scores(player_name, "add", ability_points, ability_scores)

    # TODO: Move confirmation to a separate function
    # Confirm entries
    print("\nName: " + player_name)
    print("Race: " + player_race)
    print("Class: " + player_class)
    print("Alignment: " + player_alignment)
    confirm = input("Is this correct? y/n\n? ")

    # End new game creation
    if confirm == "n" or confirm == "no":
        new_game_info()
    else:
        # Build the inserts
        inserts = "INSERT INTO player (name, race, class, alignment, level)"

        # Build the values
        values = "('" + player_name + "', '" + player_race + "', '" + player_class + "', '" + player_alignment +\
                 "', 1);"

        cursor.execute(inserts + " VALUES " + values)
        cursor.execute("COMMIT;")


def new_game():
    print("\nStarting new game...")
    cursor.execute("SHOW TABLES LIKE 'player';")
    if cursor.fetchone():
        cursor.execute("DROP TABLE player;")
        cursor.execute("COMMIT;")

    cursor.execute("CREATE TABLE IF NOT EXISTS player "
                   "(name VARCHAR(30) NOT NULL PRIMARY KEY,"
                   "race VARCHAR(30) NOT NULL,"
                   "class VARCHAR(30) NOT NULL,"
                   "alignment VARCHAR(30) NOT NULL,"
                   "level INT(2) UNSIGNED NOT NULL,"
                   "ability_str INT(2) UNSIGNED,"
                   "ability_dex INT(2) UNSIGNED,"
                   "ability_con INT(2) UNSIGNED,"
                   "ability_wis INT(2) UNSIGNED,"
                   "ability_int INT(2) UNSIGNED,"
                   "ability_cha INT(2) UNSIGNED,"
                   "gold INT(2));")
    new_game_info()


def show_menu():
    print("Choose an option")
    choice = input("1) Continue\n2) Start new game\n3) Options\n? ")
    if choice == "2":
        confirm = input("A save already exists. Are you sure? Type 'yes' to confirm\n? ")
        if confirm == "yes":
            new_game()
        else:
            show_menu()
    else:
        print("\n! - Invalid choice")
        show_menu()


def main():
    show_menu()

if __name__ == "__main__":
    main()
