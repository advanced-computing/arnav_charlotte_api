import pandas as pd

# Define dataset path
file_path = "/mnt/data/dataset_lab8.xlsx"

def get_latest_data(pull_date: str) -> pd.DataFrame:
    """
    Fetches CPI data up to the given pull_date.

    Returns only two columns: 'date' and 'cpi'.
    """
    df = pd.read_excel(file_path, usecols=["date", "cpi"])  # Keep only required columns
    df["date"] = pd.to_datetime(df["date"])  # Ensure date format
    df = df[df["date"] <= pd.to_datetime(pull_date)]  # Filter by pull_date
    return df

