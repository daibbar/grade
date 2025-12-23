import sqlite3
import os

DB_FILE = 'data/school_management.db'
SCHEMA_FILE = 'data/schema.sql'

def init_db():
    if not os.path.exists(SCHEMA_FILE):
        print(f"ERROR: Schema file not found at {SCHEMA_FILE}")
        return

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    try:
        with open(SCHEMA_FILE, 'r') as f:
            sql_script = f.read()
        cur.executescript(sql_script)
        
        conn.commit()
        print(f"SUCCESS: Database created at '{DB_FILE}'")
        print(" All tables initialized successfully.")

    except sqlite3.Error as e:
        print(f"DATABASE ERROR: {e}")
    
    except Exception as e:
        print(f"SYSTEM ERROR: {e}")
        
    finally:
        conn.close()

if __name__ == '__main__':
    if os.path.exists(DB_FILE):
        response = input(f"WARNING: '{DB_FILE}' already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            exit()
        os.remove(DB_FILE)
    
    init_db()