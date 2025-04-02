import pandas as pd
import requests
from io import BytesIO
from datetime import datetime

# Download and cache the Excel file from the API
def download_cpi_data():
    url = (
        "https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/"
        "real-time-data/data-files/xlsx/pcpiMvMd.xlsx?sc_lang=en&hash=E41A743DC6423F950B10C3DE7A4F674D"
    )
    response = requests.get(url)
    response.raise_for_status()  # Ensure we fail clearly if download breaks
    df = pd.read_excel(BytesIO(response.content))
    return df

# Get the correct vintage column name from pull_date
def get_vintage_column(pull_date: str) -> str:
    date_obj = pd.to_datetime(pull_date)
    year_suffix = str(date_obj.year)[-2:]  # e.g., "04" for 2004
    month = date_obj.month
    return f"PCPI{year_suffix}M{month}"

# Main function to return only two columns: date and cpi
def get_latest_data(pull_date: str) -> pd.DataFrame:
    df = download_cpi_data()
    
    # Normalize the DATE column
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')

    # Get the vintage column to use
    vintage_col = get_vintage_column(pull_date)
    
    if vintage_col not in df.columns:
        raise ValueError(f"Vintage column {vintage_col} not found for pull_date {pull_date}")
    
    # Build the final DataFrame
    result = df[['DATE', vintage_col]].copy()
    result.columns = ['date', 'cpi']

    # Remove rows with missing CPI values
    result.dropna(subset=['cpi'], inplace=True)

    # Filter to include only data up to pull_date (inclusive)
    pull_date_obj = pd.to_datetime(pull_date)
    result = result[result['date'] <= pull_date_obj]

    # Sort by date just in case
    result.sort_values('date', inplace=True)

    return result
