import sqlite3

class Database:

    def __init__(self):
        self.db = sqlite3.connect("users.db")
        self.cur = self.db.cursor()

    def initialize(self):
        existing_table = self.cur.execute("SELECT name FROM sqlite_master WHERE name='src_users'")
        if existing_table.fetchone() is None:
            print("Initializing user database...")
            self.cur.execute("CREATE TABLE src_users(src_id, name)")
        else:
            print("Using existing user database...")

    def get_user_name_by_id(self, src_id):
        result = self.cur.execute(f"SELECT name FROM src_users WHERE src_id='{src_id}'").fetchone()
        if result:
            return result[0]
        else:
            return None

    def add_user(self, src_id, user_name):
        self.cur.execute(f"INSERT INTO src_users VALUES('{src_id}', '{user_name}')")
        self.db.commit()

db = Database()