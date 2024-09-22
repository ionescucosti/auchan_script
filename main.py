import json
import sqlite3
import requests
import pandas as pd

from endpoint_popular_movies import response as response1
from endpoint_emmy_winners import response as response2
from endpoint_top_10_week import response as response3

# Open and read the JSON mockup files
# with open('data_popular_movies.json', 'r') as file:
#     data1 = json.load(file)
# with open('data_top_10.json', 'r') as file:
#     data2 = json.load(file)
# with open('data_emmy_winners.json', 'r') as file:
#     data3 = json.load(file)
#
# data1 = data1["data"]["list"]
# data2 = data2["data"]
# data3 = data3["data"]["list"]

# Function to fetch data from the API
def fetch_data(response):
    print(response.status)
    if response.status == 200:
        data = json.loads(response.read().decode("utf-8"))
        print(data.keys())
        return data
    else:
        print(f"Error: {response.status}")
        return None

# Fetch data from 3 different endpoints
data1 = fetch_data(response1)
data2 = fetch_data(response2)
data3 = fetch_data(response3)

# Normalize the JSON data
def normalize_data(data):
    # Flatten the JSON structure using pandas (if nested)
    df = pd.json_normalize(data)
    # Convert bool columns to int
    bool_cols = df.select_dtypes(include=['bool']).columns
    df[bool_cols] = df[bool_cols].astype(int)
    # Convert object columns that may contain lists/dictionaries to JSON strings
    object_cols = df.select_dtypes(include=['object']).columns
    for col in object_cols:
        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)

    # Handle potential None/NaN values
    df = df.where(pd.notnull(df), None)

    return df

# Normalize the fetched data
df1 = normalize_data(data1)
df2 = normalize_data(data2)
df3 = normalize_data(data3)


# Create SQLite connection and cursor
conn = sqlite3.connect('imdb_data.db')
cursor = conn.cursor()

# Create 3 different tables and insert the normalized data
def create_table_and_insert_data(df, table_name):
    # Create table based on DataFrame columns
    df.to_sql(table_name, conn, if_exists='replace', index=False)

# Insert data into 3 tables
create_table_and_insert_data(df1, 'table1')
create_table_and_insert_data(df2, 'table2')
create_table_and_insert_data(df3, 'table3')

# Create relationships between tables (if applicable)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS related_table AS
    SELECT * FROM table1 t1
    FULL JOIN table2 t2 
    ON t1."title.id" = t2.id;
''')
conn.commit()

# Run some SQL queries for reporting
def generate_report():
    query = '''
        SELECT t1."title.originalTitleText.text", t2."originalTitleText.text"
        FROM table1 t1
        FULL JOIN table2 t2 ON t1."title.id" = t2.id;
    '''
    result = pd.read_sql_query(query, conn)
    result.to_csv("report.csv", index=False)  # Set index=False to avoid writing row numbers in the CSV file


# Generate and display a report
generate_report()

# Close the SQLite connection
conn.close()
