import pandas as pd
import re

# Load the CSV file
file_path = '/Users/arnavsahai/Desktop/Arnav_Charlotte_API/arnav_charlotte_api/top-200-universities-in-north-america.csv'
df = pd.read_csv(file_path, encoding='ISO-8859-1')
# Remove special characters
df['Name'] = df['Name'].apply(lambda x: re.sub(r'[^\x00-\x7F]+', '', x))

# Handle missing values (example: fill with 0)
df.fillna(0, inplace=True)

# Standardize currency formatting
def clean_currency(value):
    if isinstance(value, str):
        value = value.replace('$', '').replace(',', '')
        if 'B' in value:
            return float(value.replace('B', '')) * 1e9
        elif 'M' in value:
            return float(value.replace('M', '')) * 1e6
        elif 'K' in value:
            return float(value.replace('K', '')) * 1e3
        return float(value)
    return value

df['Minimum Tuition cost'] = df['Minimum Tuition cost'].apply(clean_currency)
df['Endowment'] = df['Endowment'].apply(clean_currency)

# Trim whitespace
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Ensure consistent quoting (if needed)
# This step might not be necessary if the CSV is read correctly

# Fix inconsistent capitalization
df['Name'] = df['Name'].str.title()

# Save the cleaned CSV file
cleaned_file_path = '/Users/arnavsahai/Desktop/Arnav_Charlotte_API/arnav_charlotte_api/top-200-universities-in-north-america-cleaned.csv'
df.to_csv(cleaned_file_path, index=False)