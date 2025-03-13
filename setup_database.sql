-- Create a table to store the university data
CREATE TABLE universities (
    Rank INTEGER,
    Name VARCHAR,
    Country VARCHAR,
    Established INTEGER,
    Academic_Staff INTEGER,
    Number_of_Students INTEGER,
    Minimum_Tuition_cost FLOAT,
    Volumes_in_the_library INTEGER,
    Endowment FLOAT
);

-- Import data from the CSV file into the universities table
COPY universities FROM '/Users/arnavsahai/Desktop/Arnav_Charlotte_API/arnav_charlotte_api/top-200-universities-in-north-america-cleaned.csv' (FORMAT CSV, HEADER TRUE);

SELECT * FROM universities LIMIT 10;

-- Create a table to store user data
CREATE TABLE users (
    username VARCHAR PRIMARY KEY,
    age INTEGER,
    country VARCHAR
);