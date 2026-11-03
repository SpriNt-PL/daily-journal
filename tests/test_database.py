import sqlite3

import pytest

from database_creator import DatabaseCreator


@pytest.fixture
def temp_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test_journal.db"
    config_file = tmp_path / "config.ini"
    
    config_file.write_text(f"[database]\npath = {db_file}\n")
    
    monkeypatch.chdir(tmp_path)
    
    return db_file

def test_create_database_creates_table(temp_db):
    creator = DatabaseCreator()

    creator.create_database()

    assert temp_db.exists()
    
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='journal_entry';")
        table = cursor.fetchone()
        
        assert table is not None
        assert table[0] == "journal_entry"

def test_unique_entry_date_constraint(temp_db):
    creator = DatabaseCreator()
    creator.create_database()

    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO journal_entry (entry_date, content) VALUES (?, ?)", 
            ("2026-11-03", "First entry")
        )
        
        # Drugi wpis z tą samą datą – powinien rzucić wyjątek przez UNIQUE
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute(
                "INSERT INTO journal_entry (entry_date, content) VALUES (?, ?)", 
                ("2026-11-03", "Second entry with the same date")
            )