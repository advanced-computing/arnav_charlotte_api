import duckdb
import argparse
import utils  # Import the updated utils.py

# Define database path
db_path = "/mnt/data/lab8.duckdb"
table_name = "economic_data_inc"

# Parse arguments
parser = argparse.ArgumentParser(description="Incrementally load data into DuckDB")
parser.add_argument("--pull_date", type=str, required=True, help="The pull date in YYYY-MM-DD format")
args = parser.parse_args()

# Fetch data
df = utils.get_latest_data(args.pull_date)

# Connect to database
con = duckdb.connect(db_path)

# Ensure table exists
con.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        date DATE PRIMARY KEY, 
        cpi FLOAT
    );
""")

# Insert new data or update existing records
for index, row in df.iterrows():
    con.execute(f"""
        INSERT INTO {table_name} (date, cpi)
        VALUES (?, ?) 
        ON CONFLICT(date) DO UPDATE SET cpi = EXCLUDED.cpi;
    """, (row["date"], row["cpi"]))

con.close()

print(f"Incremental data loading completed for {table_name} up to {args.pull_date}")

