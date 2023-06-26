from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests

url = "http://www.howstat.com/cricket/Statistics/IPL/PlayerList.asp?s=XXXX"

response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")

# Find all tables within the HTML content
tables = soup.find_all("table")

# Check if at least two tables exist
if len(tables) > 1:
    outer_table = tables[0]  # First table (index 0)
    inner_table = tables[3]  # Second table (index 1)

    # Extract the table data from the second table into a list of dictionaries
    data = []
    rows = inner_table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        row_data = [cell.text.strip() for cell in cells]
        data.append(row_data)

    # Convert the list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(data)

else:
    print("Not enough tables found.")

df.columns = df.iloc[0]
df = df[1:].reset_index(drop=True)

df["Matches"] = pd.to_numeric(df["Matches"])
df["Runs"] = pd.to_numeric(df["Runs"])
df["Bat Avg"] = pd.to_numeric(df["Bat Avg"])
df["Runs"] = pd.to_numeric(df["Runs"])
df["Bat Avg"] = pd.to_numeric(df["Bat Avg"])
df["Wickets"] = pd.to_numeric(df["Wickets"])
df["Bowl Avg"] = pd.to_numeric(df["Bowl Avg"])

conditions = [
    (df["Wickets"] >= 10) & (df["Bat Avg"] < 25),  # Condition 1
    (df["Wickets"] >= 10) & (df["Bat Avg"] >= 25),  # Condition 2
    (df["Bat Avg"] < 15)
]
values = ["Bowler", "All Rounder", "Bowler"]

# Add a new column based on conditions
df["Role"] = np.select(conditions, values, default="Batsman")

df.to_csv('ipl_1.csv', index=False)