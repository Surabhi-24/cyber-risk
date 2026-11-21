import sqlite3
from riskengine import calculate_risk_score, classify_risk
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
def add_asset(asset_name, asset_type, owner, description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO assets (asset_name, asset_type, owner, description)
        VALUES (?, ?, ?, ?)
    """, (asset_name, asset_type, owner, description))
    conn.commit()
    conn.close()

def get_assets():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assets")
    assets = cursor.fetchall()
    conn.close()
    return assets

def add_risk(
        asset_id,
        risk_title, 
        description, likelihood, impact):
    inherited_score = calculate_risk_score(likelihood, impact)
    risk_level = classify_risk(inherited_score)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO risks (asset_id, risk_title, description, likelihood, impact, inherited_risk, risk_level)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (asset_id, risk_title, description, likelihood, impact, inherited_score, risk_level))
    conn.commit()
    conn.close()

def get_risks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM risks")
    risks = cursor.fetchall()
    conn.close()
    return risks

if __name__ == "__main__":
    create_tables()
    add_risk(
        1, 
        "Data Breach Risk", 
        "Potential exposure of sensitive customer data", 
        4, 
        5, 
    )

    add_asset(
        "Customer Database", 
        "Data Store", 
        "IT Department",
        "Contains sensitive customer information"
    )
risks = get_risks()
print("Retrieved Risks:")
for risk in risks:
    print(risk)
