import os
import sys
import random
import string
from hashlib import blake2s

databases = []
menu_options = []
dnames = []


def create_database(name: str, password: str):
    hash = blake2s(password.encode('UTF-8')).hexdigest()
    database = [name, hash]
    save_database(database)


def load_databases():
    try:
        paths = os.listdir('./nothing_secret_here/')
        for path in paths:
            if ".pdb" in path:
                dnames.append(path)
    except FileNotFoundError:
        os.mkdir('./nothing_secret_here/')
        load_databases()


def save_database(database: list[str]):
    name = database[0]
    output = '\n'.join(database)
    with open(f'./nothing_secret_here/{name}.pdb', 'w+') as file:
        file.write(output)
    print(f'Saved Database: {name}')


def open_database(name: str, password: str) -> list[str]:
    if '.pdb' not in name:
        name = name + '.pdb'
    hash = blake2s(password.encode('UTF-8')).hexdigest()
    if name in os.listdir('./nothing_secret_here/'):
        with open(f'./nothing_secret_here/{name}', 'r+') as file:
            entries = file.read().split("\n")
            if hash == entries[1]:
                return entries
            else:
                print("ERROR -> Invalid master password used")
                input('')
    else:
        print("ERROR -> That database was not found.")
        input('')


def generate_password() -> str:
    letters = string.ascii_letters
    digits = string.digits
    password = []
    for index in range(0, 9):
        if random.choice([True, False]):
            password.append(random.choice(letters))
        else:
            password.append(random.choice(digits))
    return ''.join(password)


def create_entry(descriptor: str, username: str):
    password = generate_password()
    entry = f'{descriptor}:{username}:{password}'
    return entry


def main_menu():
    print("[1] Create Database")
    print("[2] Open Database")
    print("[3] Remove Database")
    print("[0] Exit")


def db_menu():
    print("[1] Add Entry")
    print("[2] Edit Entry")
    print("[3] Remove Entry")
    print("[4] Close Database")


def clear_screen():
    os.system("cls")


load_databases()
while True:
    clear_screen()
    main_menu()
    menu_select = int(input("Please select an option: "))
    if menu_select == 1:  # create db
        clear_screen()
        name = input("Name: ")
        passw = input("Password: ")
        create_database(name, passw)
    elif menu_select == 2:  # open db
        clear_screen()
        print('-----------------DATABASES-----------------')
        for dname in dnames:
            print(dname)
        print('-------------------------------------------')
        name = input("Name: ")
        passw = input("Password: ")
        database = open_database(name, passw)

        while True:
            entries = database[2: len(database)]
            clear_screen()
            print('-------------------------------------------')
            for entry in entries:
                print(entry)
            print('-------------------------------------------')
            db_menu()
            menu_select = int(input("Please select and option: "))
            if menu_select == 1:  # create entry
                clear_screen()
                descriptor = input("Descriptor: ")
                username = input("Username: ")
                entry = create_entry(descriptor, username)
                database.append(entry)
                save_database(database)
            elif menu_select == 2: # edit entry2
                pass
            elif menu_select == 3: # remove entry
                descORuser = input("Descriptor OR Username: ")
                for entry in entries:
                    entrySplit = entry.split(":")
                    if descORuser in entrySplit:
                        database.remove(entry)
                        continue
                print('ERROR -> Entry not found, remember they are cAsE-sEnSiTivE.')
                input('')
            elif menu_select == 4:
                save_database(database)
                print('Exiting Database...')
                input("")
                break
    elif menu_select == 3: # remove db
        pass
    elif menu_select == 0:
        pass
    else:
        print('Invalid option -> Please try again')
        input("")
