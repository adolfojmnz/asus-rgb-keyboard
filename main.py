import os
import sqlite3

DB_PATH = os.environ.get('HOME', '') + '/workspace/linux/aura/aura.sqlite'


class DB:

    def __init__(self):
        self._connect()

    def _connect(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()


class Color():

    def __init__(self, db=None):
        self.db = db or DB()

    def get_highest_color_index(self):
        self.db.cursor.execute('SELECT MAX(id) FROM colors')
        row = self.db.cursor.fetchone()
        return row[0] if row else 0

    def _update_active_color(self, color):
        self.db.cursor.execute('UPDATE colors SET active = NULL')
        self.db.cursor.execute(
            f'UPDATE colors SET active = TRUE WHERE id = {color[0]}'
        )
        self.db.connection.commit()

    def get_active_color(self):
        self.db.cursor.execute('SELECT * FROM colors WHERE active = TRUE')
        row = self.db.cursor.fetchone()
        return row if row else None

    def get_color_by_id(self, id) -> tuple:
        self.db.cursor.execute(f'SELECT * FROM colors WHERE id = {id}')
        row = self.db.cursor.fetchone()
        return row if row else None

    def set_color_by_id(self, color_id):
        new_color = self.get_color_by_id(color_id)
        if not new_color:
            return {'message': 'Color not found.', 'status': 404}
        os.system(f"asusctl led-mode static -c {new_color[2]}")
        self._update_active_color(new_color)
        return {'message': 'the color has been set.', 'status': 200}

    def set_next_color(self):
        next_color_id = self.get_active_color()[0] + 1
        if next_color_id > self.get_highest_color_index():
            next_color_id = 1
        print(next_color_id)
        return self.set_color_by_id(next_color_id)

    def set_prev_color(self):
        prev_color_id = self.get_active_color()[0] - 1
        if prev_color_id < 1:
            prev_color_id = self.get_highest_color_index()
        print(prev_color_id)
        return self.set_color_by_id(prev_color_id)


if __name__ == "__main__":
    import sys

    color_class = Color()

    if not len(sys.argv) > 1:
        color_class.set_next_color()
    elif '--prev' in sys.argv:
        color_class.set_prev_color()
    elif '--next' in sys.argv:
        color_class.set_next_color()
    elif '--color' in sys.argv:
        for idx,arg in enumerate(sys.argv):
            if not arg == '--color':
                continue
            color_class.set_color_by_id(int(sys.argv[idx+1]))

