import psycopg2
import csv


conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=superduper")

cur = conn.cursor()
cur.execute("""
    CREATE TABLE organizations(
    id integer PRIMARY KEY,
    name text,
    city text,
    state text,
    postal text,
    category text)
""")

with open('organization_sample_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row.
    for row in reader:
        cur.execute(
            "INSERT INTO organizations VALUES (%s, %s, %s, %s, %s, %s)",
            row
        )
conn.commit()