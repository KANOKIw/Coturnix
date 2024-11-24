import sqlite3
import csv


csv_file_path = "./SHISHIJI/unko.csv"

conn = sqlite3.connect("./SHISHIJI/db/Latest_nametable.db")
cursor = conn.cursor()

create_table_query = """
    CREATE TABLE IF NOT EXISTS NAME_TABLE (
    previous_grade TEXT,
    previous_class TEXT,
    previous_number INTEGER,
    name TEXT,
    misc_1 TEXT,
    organization TEXT,
    misc_2 TEXT,
    previous_dat TEXT,
    latest_dat TEXT,
    latest_grade TEXT,
    latest_class TEXT,
    latest_number INTEGER
)
"""
cursor.execute(create_table_query)


with open(csv_file_path, "r", newline="", encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)
    for row in csv_reader:
        row[3] = row[3].replace(" ", "").replace("　", "")
        cursor.execute(f"INSERT INTO NAME_TABLE VALUES ({','.join(['?' for i in range(12)])})", row)


conn.commit()
conn.close()

print("SAVED as DB")
