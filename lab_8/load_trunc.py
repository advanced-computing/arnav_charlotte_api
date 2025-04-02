import duckdb
import argparse
import utils  # Import the updated utils.py

# Define database path
db_path = "/mnt/data/lab8.duckdb"
table_name = "economic_data_trunc"

# Parse arguments
parser = argparse.ArgumentParser(description="Truncate and load new data into DuckDB")
parser.add_argument("--pull_date", type=str, required=True, help="The pull date in YYYY-MM-DD format")
args = parser.parse_args()

# Fetch data
df = utils.get_latest_data(args.pull_date)

# Truncate and reload new data
con = duckdb.connect(db_path)
con.execute(f"DROP TABLE IF EXISTS {table_name};")
df.to_sql(table_name, con, if_exists="replace", index=False)
con.close()

print(f"Truncate and load completed for {table_name} with data up to {args.pull_date}")

