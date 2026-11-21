import sqlite3
def connect_db():
    conn = sqlite3.connect('risk_data.db')
    return conn 

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_name TEXT NOT NULL,
            asset_type TEXT NOT NULL,
            owner TEXT NOT NULL,
            description TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risks (
            risk_id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER NOT NULL,
            risk_title TEXT NOT NULL,
            description TEXT NOT NULL,
            likelihood INTEGER NOT NULL,
            impact INTEGER NOT NULL,
            inherited_risk INTEGER NOT NULL,
            risk_level TEXT NOT NULL,
            residual_likelihood INTEGER,
            residual_impact INTEGER,
            residual_level TEXT,
            status TEXT DEFAULT 'Open',
            FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS controls (
            control_id INTEGER PRIMARY KEY AUTOINCREMENT,
            risk_id INTEGER NOT NULL,
            control_name TEXT NOT NULL,
            control_type TEXT NOT NULL,
            description TEXT NOT NULL,
            implementation_status TEXT DEFAULT 'Planned',
            FOREIGN KEY (risk_id) REFERENCES risks (risk_id)
        )
   """) 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS  treatments (
            treatment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            risk_id INTEGER NOT NULL,
            treatment_strategy TEXT NOT NULL,
            action_description TEXT NOT NULL,
            assigned_to TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (risk_id) REFERENCES risks (risk_id)
        )
    """)
    conn.commit()
    conn.close()
if __name__ == "__main__":
    create_tables()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table'
    """)
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])
    conn.close()
