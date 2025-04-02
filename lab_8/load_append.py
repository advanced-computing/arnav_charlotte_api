import duckdb
import argparse
import utils  # Import the updated utils.py

# Define database path
db_path = "/mnt/data/lab8.duckdb"
table_name = "economic_data_append"

# Parse arguments
parser = argparse.ArgumentParser(description="Append new data into DuckDB")
parser.add_argument("--pull_date", type=str, required=True, help="The pull date in YYYY-MM-DD format")
args = parser.parse_args()

# Fetch data
df = utils.get_latest_data(args.pull_date)

# Insert into database (append mode)
con = duckdb.connect(db_path)
df.to_sql(table_name, con, if_exists="append", index=False)
con.close()

print(f"Data appended successfully to {table_name} for date {args.pull_date}")
