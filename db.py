import csv
import sqlite3


def create_table(cursor):
    try:
        cursor.execute("""
            CREATE TABLE colors(
                id INTEGER PRIMARY KEY,
                name TEXT,
                hex_code TEXT,
                active BOOLEAN,
                UNIQUE(active) ON CONFLICT FAIL
            )
        """)
    except sqlite3.OperationalError as error:
        print(error)

def set_table_trigger(cursor):
    try:
        cursor.execute("""
            CREATE TRIGGER enforce_one_active_row
            AFTER INSERT ON colors
            WHEN NEW.active = TRUE
            BEGIN
                UPDATE colors SET active = FALSE WHERE id != NEW.id;
            END;
        """)
    except sqlite3.OperationalError as error:
        print(error)

def populate_table(cursor):
    with open('colors.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            try:
                cursor.execute('INSERT INTO colors (id, name, hex_code) VALUES (?, ?, ?)', row)
            except sqlite3.IntegrityError:
                print(f"Unique constraint. Skipping row {row}")

def set_crimson_active(cursor):
    """ Sets as initial state the crismon color as active. """
    try:
        cursor.execute('UPDATE colors SET active = NULL')
        cursor.execute('UPDATE colors SET active = TRUE WHERE id = 6')
    except sqlite3.OperationalError as error:
        print(error)


if __name__ == '__main__':
    connection = sqlite3.connect("aura.sqlite")
    cursor = connection.cursor()

    create_table(cursor)
    set_table_trigger(cursor)
    populate_table(cursor)
    set_crimson_active(cursor)

    connection.commit()
    connection.close()