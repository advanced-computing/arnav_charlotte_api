# Usage and Manual Testing Instructions

## Overview
This document provides instructions on how to run and manually test the different data loading scripts: `load_append.py`, `load_inc.py`, and `load_trunc.py`. Each script processes data on a daily basis and updates the database according to a specific method using Consumer Price Index (CPI) data from the **Philadelphia Federal Reserve** via their live API.

## Prerequisites

Ensure the following dependencies are installed:
- Python 3.x
- pandas
- duckdb
- openpyxl
- requests

## Data Source

Each script relies on the function `get_latest_data(pull_date)` from `utils.py`, which:
- Downloads the CPI vintages Excel file from the official API
- Selects the correct vintage based on the pull date
- Returns a cleaned DataFrame with only two columns: `date` and `cpi`

## Running the Scripts

Each script can be executed by calling the `run()` function with a `pull_date` string.

### 1. Append Method (`load_append.py`)
**Command:**
```python
import load_append
load_append.run("YYYY-MM-DD")
```

**Expected Outcome:**
- Inserts only new dates (no duplicates)
- Table grows over time
- Existing records remain unchanged

### 2. Incremental Load Method (`load_inc.py`)
**Command:**
```python
import load_inc
load_inc.run("YYYY-MM-DD")
```

**Expected Outcome:**
- Inserts new dates
- Updates existing records if the `cpi` has changed
- Prevents duplicate entries

### 3. Truncate and Load Method (`load_trunc.py`)
**Command:**
```python
import load_trunc
load_trunc.run("YYYY-MM-DD")
```

**Expected Outcome:**
- Deletes all rows from the table
- Replaces the table with the latest snapshot of data up to the `pull_date`

## Manual Testing Instructions

1. **Run Each Script for a Sample Date**:
   - For example: `"2004-01-15"`

2. **Run for Multiple Dates Sequentially**:
   - Simulate daily data loading by running over a date range

3. **Validate Behavior**:
   - `load_append.py`: Data is added, no duplicates by date
   - `load_inc.py`: Data is inserted or updated if already exists
   - `load_trunc.py`: Table has only data available up to the latest `pull_date`

4. **Performance Check**:
   - Measure runtime over long date ranges to evaluate method efficiency

## Expected Table Behavior

| Method           | Table Name              | Data Growth | Duplicates? | Updates Existing Data? | Deletes Old Data? |
|------------------|--------------------------|--------------|-------------|-------------------------|-------------------|
| Append           | economic_data_append     | Grows        | ❌ (deduplicated) | ❌                     | ❌                |
| Incremental      | economic_data_inc        | Grows or updates | ❌       | ✅                     | ❌                |
| Truncate & Load  | economic_data_trunc      | Replaced each run | ❌       | ❌                     | ✅                |

## Example Table Snapshots

### After Running `load_append.py --pull_date 2004-02-15`
| date       | cpi  |
|------------|------|
| 2004-01-01 | 185.8|
| 2004-02-01 | 186.3|

### After Running `load_inc.py --pull_date 2004-02-15`
| date       | cpi  |
|------------|------|
| 2004-01-01 | 185.8|
| 2004-02-01 | 186.3|  (*Updated if previous entry changed*)

### After Running `load_trunc.py --pull_date 2004-02-15`
| date       | cpi  |
|------------|------|
| 2004-01-01 | 185.8|
| 2004-02-01 | 186.3| (*Only current snapshot data remains*)
