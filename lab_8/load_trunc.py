import duckdb
from utils import get_latest_data

def run(pull_date: str):
    # Step 1: Get CPI data up to the given pull_date
    data = get_latest_data(pull_date)

    # Step 2: Connect to the DuckDB database
    conn = duckdb.connect("economic_data_trunc.duckdb")

    # Step 3: Create table if it doesn't exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS economic_data_trunc (
            date DATE,
            cpi DOUBLE
        );
    """)

    # Step 4: Truncate the table (delete all existing rows)
    conn.execute("DELETE FROM economic_data_trunc;")

    # Step 5: Insert fresh data
    conn.register("new_data", data)
    conn.execute("""
        INSERT INTO economic_data_trunc
        SELECT * FROM new_data;
    """)

    print(f"[truncate] Pull date {pull_date}: Replaced with {len(data)} rows.")

    conn.close()
