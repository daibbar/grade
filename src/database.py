import sqlite3
import pandas as pd
import os

# Ensure we point to the correct file paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '../data/parascolaire.db')
SCHEMA_PATH = os.path.join(BASE_DIR, '../data/schema.sql')

def get_connection():
    """Establishes a connection to the SQLite database with Foreign Keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    # ⚠️ CRITICAL: SQLite disables Foreign Keys by default. We must enable them.
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Reads the schema.sql file and initializes the database tables."""
    if not os.path.exists(SCHEMA_PATH):
        print(f"Error: Schema file not found at {SCHEMA_PATH}")
        return
    
    conn = get_connection()
    with open(SCHEMA_PATH, 'r') as f:
        sql_script = f.read()
    
    try:
        conn.executescript(sql_script)
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")
    finally:
        conn.close()

def run_query(query, params=()):
    """
    Executes INSERT, UPDATE, DELETE queries.
    Returns: None
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback() # Undo changes if error occurs
        raise e # Re-raise error to show it in Streamlit later
    finally:
        conn.close()

def get_data(query, params=()):
    """
    Executes SELECT queries.
    Returns: A Pandas DataFrame (perfect for Streamlit display).
    """
    conn = get_connection()
    try:
        # pd.read_sql executes raw SQL and returns a formatted table
        df = pd.read_sql(query, conn, params=params)
        return df
    finally:
        conn.close()