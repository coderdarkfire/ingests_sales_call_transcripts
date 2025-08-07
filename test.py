import os
import sqlite3

db_path = "calllog.db"
print("🔍 Using DB:", os.path.abspath(db_path))

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print("📋 Tables in DB:", tables)

# Check for 'calllog' table
if "calllog" in tables:
    cursor.execute("SELECT COUNT(*) FROM calllog;")
    print(" Total call logs inserted:", cursor.fetchone()[0])

    cursor.execute("SELECT * FROM calllog LIMIT 5;")
    print(" Sample rows:")
    for row in cursor.fetchall():
        print(row)
else:
    print(" Table 'calllog' does not exist in the database.")

conn.close()
