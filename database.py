
import sqlite3

from riskengine import calculate_risk_score, classify_risk


def connect_db():
    conn = sqlite3.connect("risk_data.db")
    conn.execute("PRAGMA foreign_keys = ON")
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
            inherent_score INTEGER NOT NULL,
            risk_level TEXT NOT NULL,
            residual_likelihood INTEGER,
            residual_impact INTEGER,
            residual_score INTEGER,
            residual_level TEXT,
            status TEXT DEFAULT 'Open',
            FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
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
            FOREIGN KEY (risk_id) REFERENCES risks(risk_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS treatments (
            treatment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            risk_id INTEGER NOT NULL,
            treatment_strategy TEXT NOT NULL,
            action_description TEXT NOT NULL,
            assigned_to TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (risk_id) REFERENCES risks(risk_id)
        )
    """)

    conn.commit()
    conn.close()


def add_asset(asset_name, asset_type, owner, description):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO assets (
            asset_name,
            asset_type,
            owner,
            description
        )
        VALUES (?, ?, ?, ?)
    """, (asset_name, asset_type, owner, description))

    conn.commit()
    asset_id = cursor.lastrowid
    conn.close()

    return asset_id


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
    description,
    likelihood,
    impact
):

    inherent_score = calculate_risk_score(
        likelihood,
        impact
    )

    risk_level = classify_risk(inherent_score)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO risks (
            asset_id,
            risk_title,
            description,
            likelihood,
            impact,
            inherent_score,
            risk_level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        asset_id,
        risk_title,
        description,
        likelihood,
        impact,
        inherent_score,
        risk_level
    ))

    conn.commit()
    risk_id = cursor.lastrowid
    conn.close()

    return risk_id


def get_risks():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM risks")

    risks = cursor.fetchall()

    conn.close()

    return risks


def add_controls(
    risk_id,
    control_name,
    control_type,
    description,
    implementation_status
):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO controls (
            risk_id,
            control_name,
            control_type,
            description,
            implementation_status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        risk_id,
        control_name,
        control_type,
        description,
        implementation_status
    ))

    conn.commit()
    control_id = cursor.lastrowid
    conn.close()

    return control_id


def get_controls():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM controls")

    controls = cursor.fetchall()

    conn.close()

    return controls


def add_treatment(
    risk_id,
    treatment_strategy,
    action_description,
    assigned_to,
    due_date,
    status
):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO treatments (
            risk_id,
            treatment_strategy,
            action_description,
            assigned_to,
            due_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        risk_id,
        treatment_strategy,
        action_description,
        assigned_to,
        due_date,
        status
    ))

    conn.commit()
    treatment_id = cursor.lastrowid
    conn.close()

    return treatment_id


def get_treatments():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM treatments")

    treatments = cursor.fetchall()

    conn.close()

    return treatments


def update_residual_risk(
    risk_id,
    residual_likelihood,
    residual_impact
):

    residual_score = calculate_risk_score(
        residual_likelihood,
        residual_impact
    )

    residual_level = classify_risk(residual_score)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE risks
        SET residual_likelihood = ?,
            residual_impact = ?,
            residual_score = ?,
            residual_level = ?
        WHERE risk_id = ?
    """, (
        residual_likelihood,
        residual_impact,
        residual_score,
        residual_level,
        risk_id
    ))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated


if __name__ == "__main__":

    create_tables()

    assets = get_assets()

    asset_id = None

    for asset in assets:
        if asset[1] == "Customer Database":
            asset_id = asset[0]
            break

    if asset_id is None:
        asset_id = add_asset(
            "Customer Database",
            "Data Store",
            "IT Department",
            "Contains sensitive customer information"
        )

    risks = get_risks()

    risk_id = None

    for risk in risks:
        if risk[1] == asset_id and risk[2] == "Data Breach Risk":
            risk_id = risk[0]
            break

    if risk_id is None:
        risk_id = add_risk(
            asset_id,
            "Data Breach Risk",
            "Potential exposure of sensitive customer data",
            4,
            5
        )

    controls = get_controls()

    control_exists = any(
        control[1] == risk_id
        and control[2] == "Multi-Factor Authentication"
        for control in controls
    )

    if not control_exists:
        add_controls(
            risk_id,
            "Multi-Factor Authentication",
            "Preventive",
            "Implement MFA for all user accounts to reduce unauthorized access.",
            "Implemented"
        )

    treatments = get_treatments()

    treatment_exists = any(
        treatment[1] == risk_id
        and treatment[2] == "Mitigation"
        for treatment in treatments
    )

    if not treatment_exists:
        add_treatment(
            risk_id,
            "Mitigation",
            "Implement encryption for sensitive data at rest and in transit.",
            "Security Team",
            "2026-12-31",
            "In Progress"
        )

    print("\nREGISTERED ASSETS")
    for asset in get_assets():
        print(asset)

    print("\nREGISTERED RISKS")
    for risk in get_risks():
        print(risk)

    print("\nREGISTERED CONTROLS")
    for control in get_controls():
        print(control)

    print("\nREGISTERED TREATMENTS")
    for treatment in get_treatments():
        print(treatment)

    print("\nDatabase verification completed!")
