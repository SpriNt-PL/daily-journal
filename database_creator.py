import sqlite3
from configparser import ConfigParser

class DatabaseCreator:
    def __init__(self):   
        self.cp = ConfigParser()
        self.cp.read('config.ini')
        self.db_path = self.cp.get('database', 'path')

    def create_database(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                print(f"Opened SQLite database successfully.")

                cursor = conn.cursor()

                query = """--sql
                CREATE TABLE IF NOT EXISTS journal_entry (
                    entry_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    entry_date DATETIME NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT (datetime('now')),
                    updated_at DATETIME DEFAULT (datetime('now'))
                )
                """
                cursor.execute(query)

        except sqlite3.OperationalError as e:
            print("Failed to open database:", e)

if __name__ == '__main__':
    db_creator = DatabaseCreator()
    db_creator.create_database()