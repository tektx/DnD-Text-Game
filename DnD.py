"""
    D&D Text-based game
"""

__author__ = "tektx"

import pymysql
import random

db_conn = pymysql.connect(user='root', password='password', database='dnd')
cursor = db_conn.cursor()


def new_game_ability_scores(mode, points, ability_str, ability_dex, ability_con, ability_wis, ability_int, ability_cha):
    print("Ability scores")
    print("STR: " + ability_str)
    print("DEX: " + ability_dex)
    print("CON: " + ability_con)
    print("WIS: " + ability_wis)
    print("INT: " + ability_int)
    print("CHA: " + ability_cha)
    print("---------")
    print("Points remaining: " + points)


def new_game_info():
    ability_points = 20
    ability_scores = {'Strength': 10, 'Dexterity': 10, 'Constitution': 10,
                      'Wisdom': 10, 'Intelligence': 10, 'Charisma': 10}
    list_races = ['Human', 'Halfling', 'Dwarf', 'High Elf', 'Half-orc', 'Half-elf', 'Gnome']
    list_classes = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue',
                    'Sorcerer', 'Wizard']
    list_alignments = ['Lawful Good', 'Neutral Good', 'Chaotic Good',
                       'Lawful Neutral', 'True Neutral', 'Chaotic Neutral',
                       'Lawful Evil', 'Neutral Evil', 'Chaotic Evil']
    player_name = input("Name: ")

    # Loop through the available races
    count = 0
    for choice in list_races:
        print(str(count) + ": " + choice)
        count += 1
    player_race = list_races[int(input("Race: "))]

    # Loop through the available classes
    count = 0
    for choice in list_classes:
        print(str(count) + ": " + choice)
        count += 1
    player_class = list_classes[int(input("Class: "))]

    # Loop through the available alignments
    count = 0
    for choice in list_alignments:
        print(str(count) + ": " + choice)
        count += 1
    player_alignment = list_alignments[int(input("Alignment: "))]
    print("Name: " + player_name)
    print("Race: " + player_race)
    print("Class: " + player_class)
    print("Alignment: " + player_alignment)
    confirm = input("Is this correct? y/n\n? ")

    # Allocate ability points
    new_game_ability_scores("add", ability_points, **ability_scores)

    # End new game creation
    if confirm == "n":
        new_game_info()
    else:
        cursor.execute("INSERT INTO player (name, race, class, alignment, level) VALUES ('" + player_name + "', '" +
                       player_race + "', '" + player_class + "', '" + player_alignment + "', 1);")
        cursor.execute("COMMIT;")


def new_game():
    print("Starting new game...")
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
                   "strength INT(2) UNSIGNED,"
                   "dexterity INT(2) UNSIGNED,"
                   "constitution INT(2) UNSIGNED,"
                   "wisdom INT(2) UNSIGNED,"
                   "intelligence INT(2) UNSIGNED,"
                   "charisma INT(2) UNSIGNED,"
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
        show_menu()


def main():
    show_menu()

if __name__ == "__main__":
    main()
