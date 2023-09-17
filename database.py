import datetime
import sqlite3

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("lattrank.db")
        self.cur = self.conn.cursor()

    def initialize(self):
        existing_table = self.cur.execute("SELECT name FROM sqlite_master WHERE name='src_users'")
        if existing_table.fetchone() is None:
            print("Initializing user database...")
            self.cur.execute("CREATE TABLE src_users(src_id, name, score)")
        else:
            print("Using existing user database...")

        existing_table = self.cur.execute("SELECT name FROM sqlite_master WHERE name='last_ranked'")
        if existing_table.fetchone() is None:
            print("Initializing last ranking database...")
            self.cur.execute("CREATE TABLE last_ranked(timestamp)")
        else:
            print("Using existing last ranking database...")

    def get_all_user_data(self):
        result = self.cur.execute(f"SELECT name, score FROM src_users").fetchall()
        return result

    def get_user_name_by_id(self, src_id):
        result = self.cur.execute(f"SELECT name FROM src_users WHERE src_id='{src_id}'").fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_user_score_by_id(self, src_id):
        result = self.cur.execute(f"SELECT score FROM src_users WHERE src_id='{src_id}'").fetchone()
        if result:
            return result[0]
        else:
            return None

    def add_user(self, src_id, user_name, score):
        self.cur.execute(f"INSERT INTO src_users VALUES('{src_id}', '{user_name}', '{score}')")
        self.conn.commit()

    def update_score(self, src_id, new_score):
        self.cur.execute(f"UPDATE src_users SET score = '{new_score}' WHERE src_id='{src_id}'")
        self.conn.commit()

    def get_last_ranked(self):
        result = self.cur.execute(f"SELECT timestamp FROM last_ranked").fetchone()
        if result:
            return result[0]
        else:
            return None

    def mark_last_ranked(self, latest_timestamp):
        self.cur.execute(f"INSERT INTO last_ranked VALUES('{latest_timestamp}')")
        self.conn.commit()

db = Database()