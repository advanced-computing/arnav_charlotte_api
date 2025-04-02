import duckdb
import pandas as pd
from utils import get_latest_data

def run(pull_date: str):
    # Step 1: Get latest CPI data up to the pull_date
    data = get_latest_data(pull_date)

    # Step 2: Connect to the DuckDB database for append
    conn = duckdb.connect("economic_data_append.duckdb")

    # Step 3: Create table if it doesn't exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS economic_data_append (
            date DATE,
            cpi DOUBLE
        );
    """)

    # Step 4: Get existing dates in the table
    existing_dates = conn.execute("SELECT date FROM economic_data_append").fetchdf()
    existing_dates_set = set(existing_dates['date']) if not existing_dates.empty else set()

    # Step 5: Filter data to only new dates
    data_filtered = data[~data['date'].isin(existing_dates_set)]

    # Step 6: Append only new dates
    if not data_filtered.empty:
        conn.register("temp_df", data_filtered)
        conn.execute("""
            INSERT INTO economic_data_append
            SELECT * FROM temp_df;
        """)
        print(f"[append] Pull date {pull_date}: Inserted {len(data_filtered)} new rows.")
    else:
        print(f"[append] Pull date {pull_date}: No new data to insert (all dates already exist).")

    conn.close()
