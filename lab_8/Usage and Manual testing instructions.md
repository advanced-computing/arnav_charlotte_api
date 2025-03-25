# Usage and Manual Testing Instructions

## Overview
This document provides instructions on how to run and manually test the different data loading scripts: `load_append.py`, `load_inc.py`, and `load_trunc.py`. Each script processes data on a daily basis and updates the database according to a specific method.

## Prerequisites
Ensure the following dependencies are installed before running the scripts:

- Python 3.x
- Pandas
- Any additional dependencies specified in `utils.py`

## Running the Scripts
Each script can be executed by calling the `run` function with a date parameter. This simulates daily data processing.

### 1. Append Method (`load_append.py`)
**Command:**
```python
import load_append
load_append.run("YYYY-MM-DD")
```
**Expected Outcome:**
- New data for the specified date is appended to the table.
- The table grows continuously as new data is added daily.
- No old data is modified or removed.

### 2. Incremental Load Method (`load_inc.py`)
**Command:**
```python
import load_inc
load_inc.run("YYYY-MM-DD")
```
**Expected Outcome:**
- New data for the specified date is inserted.
- If data for the same date already exists, it is updated instead of being duplicated.
- The table size increases only when new data is available.

### 3. Truncate and Load Method (`load_trunc.py`)
**Command:**
```python
import load_trunc
load_trunc.run("YYYY-MM-DD")
```
**Expected Outcome:**
- The existing table is completely deleted (truncated) before loading new data.
- Only the most recent day's data remains in the table after execution.

## Manual Testing Instructions
To verify correctness, follow these steps:

1. **Start with an Empty Table**:
   - Ensure the database is cleared before running any script.

2. **Run Each Script for a Sample Date**:
   - Execute each script with a specific date, e.g., `"2023-01-01"`.
   - Check the table contents after execution.

3. **Run for Multiple Dates Sequentially**:
   - Execute the script for several consecutive days and observe the changes in the table.
   
4. **Validate Data Consistency**:
   - For `load_append.py`, ensure all past data remains.
   - For `load_inc.py`, confirm updates instead of duplicates.
   - For `load_trunc.py`, ensure only the last executed date’s data is retained.

5. **Performance Evaluation**:
   - Measure execution time for each method over a longer date range.
   - Compare the speed and efficiency of the different methods.


## Expected Table Changes Summary
| Method        | Table Name              | Data Growth | Duplicates? | Updates Existing Data? | Deletes Old Data? |
|--------------|------------------------|------------|-------------|-------------------------|-------------------|
| Append       | economic_data_append    | Grows continuously | Yes | No | No |
| Incremental  | economic_data_inc       | Grows only when new data exists | No | Yes | No |
| Truncate & Load | economic_data_trunc | Always size of one day's data | No | No | Yes |

## Example Table Outputs
### After Running `load_append.py --pull_date 2025-03-20`
| date       | cpi  |
|------------|------|
| 2025-03-18 | 289  |
| 2025-03-19 | 290  |
| 2025-03-20 | 291  |

### After Running `load_inc.py --pull_date 2025-03-20`
| date       | cpi  |
|------------|------|
| 2025-03-18 | 289  |
| 2025-03-19 | 290  |
| 2025-03-20 | 292  |  (*Updated if previous entry exists*)

### After Running `load_trunc.py --pull_date 2025-03-20`
| date       | cpi  |
|------------|------|
| 2025-03-20 | 291  | (*Only the latest data remains*)


