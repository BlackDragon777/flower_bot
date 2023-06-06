import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    def add_userid(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id) VALUES(?)", (user_id,))

    def get_userid(self):
        with self.connection:
            users_id = self.cursor.execute("SELECT user_id FROM users").fetchall()
            return users_id

    def exicts_userid(self, user_id):
        with self.connection:
            users_id = self.cursor.execute("SELECT * FROM users WHERE user_id == ?", (user_id,)).fetchall()
            return bool(len(users_id))