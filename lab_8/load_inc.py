import duckdb
import pandas as pd
from utils import get_latest_data

def run(pull_date: str):
    # Step 1: Get CPI data up to the given pull_date
    new_data = get_latest_data(pull_date)

    # Step 2: Connect to the DuckDB database for incremental loading
    conn = duckdb.connect("economic_data_inc.duckdb")

    # Step 3: Create table if it doesn't exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS economic_data_inc (
            date DATE PRIMARY KEY,
            cpi DOUBLE
        );
    """)

    # Step 4: Load existing dates
    existing_dates_df = conn.execute("SELECT date FROM economic_data_inc").fetchdf()
    existing_dates_set = set(existing_dates_df['date']) if not existing_dates_df.empty else set()

    # Step 5: Split into new and existing rows
    to_insert = new_data[~new_data['date'].isin(existing_dates_set)]
    to_update = new_data[new_data['date'].isin(existing_dates_set)]

    # Step 6: Insert new rows
    if not to_insert.empty:
        conn.register("to_insert", to_insert)
        conn.execute("""
            INSERT INTO economic_data_inc
            SELECT * FROM to_insert;
        """)
        print(f"[incremental] Pull date {pull_date}: Inserted {len(to_insert)} new rows.")

    # Step 7: Update existing rows (if CPI values changed)
    if not to_update.empty:
        for _, row in to_update.iterrows():
            conn.execute("""
                UPDATE economic_data_inc
                SET cpi = ?
                WHERE date = ?;
            """, (row['cpi'], row['date']))
        print(f"[incremental] Pull date {pull_date}: Updated {len(to_update)} existing rows.")

    if to_insert.empty and to_update.empty:
        print(f"[incremental] Pull date {pull_date}: No changes needed (data already up-to-date).")

    conn.close()
