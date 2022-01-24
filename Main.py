databases = []


def create_database(name: str, password: str):
    database = [f'[{password.__hash__()}]']
    with open(f'./{name}.pdb', 'wb+') as file:
        for entry in database:
            file.write(entry.encode('UTF-8'))
    file.close()
    databases.append(database)
