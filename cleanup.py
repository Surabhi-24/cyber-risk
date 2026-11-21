import sqlite3
conn = sqlite3.connect("risk_data.db")
conn.execute("PRAGMA foreign_keys = 1")

cursor = conn.cursor()
cursor.execute("DELETE FROM controls WHERE risk_id != 1")
cursor.execute("DELETE FROM treatments WHERE risk_id != 1")
cursor.execute("DELETE FROM controls WHERE control_id != 1")
cursor.execute("DELETE FROM treatments WHERE treatment_id != 1")
cursor.execute("DELETE FROM risks WHERE risk_id != 1")
cursor.execute("DELETE FROM assets WHERE asset_id != 1")

conn.commit() 

for table in ["controls", "treatments", "risks", "assets"]:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"{table}: {cursor.fetchone()[0]} record(s)")

conn.close()