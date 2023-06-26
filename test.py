from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests

def extract_personal_data(sublink):
    response = requests.get(sublink)
    soup = BeautifulSoup(response.content, "lxml")
    tables = soup.find_all("table")

    table_1 = tables[3]

    data = []
    rows = table_1.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        row_data = [cell.text.strip() for cell in cells]
        data.append(row_data)

    df = pd.DataFrame(data)
    df = df.drop(df.columns[2], axis=1)
    df = df.drop(df.index[:2])
    df = df.reset_index(drop=True)
    return df

def extract_stats(sublink):
    response = requests.get(sublink)
    soup = BeautifulSoup(response.content, "lxml")
    tables = soup.find_all("table")

    table_1 = tables[5]

    data = []
    rows = table_1.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        row_data = [cell.text.strip() for cell in cells]
        data.append(row_data)

    df = pd.DataFrame(data)

    split_indices = [16, 30]

    df_bat = df.iloc[:split_indices[0]].drop(df.index[:1])
    df_bowl = df.iloc[split_indices[0] + 1:split_indices[1]].reset_index(drop=True).drop(df.index[:1])
    df_field = df.iloc[split_indices[1] + 1:].reset_index(drop=True).drop(df.index[:1])

    return df_bat, df_bowl, df_field

url = "http://www.howstat.com/cricket/Statistics/IPL/PlayerOverview.asp?PlayerID=3916"

bat, bowl, field = extract_stats(url)
personal_data = extract_personal_data(url)

new_column_names = ['Attribute', 'Value']

# Change column names in each DataFrame
dataframes = [bat, bowl, field, personal_data]
for df in dataframes:
    df.rename(columns=dict(zip(df.columns, new_column_names)), inplace=True)
    df['Attribute'] = df['Attribute'].str.replace(':', '')

names = ['Batting stats', 'Bowling stats', 'Fielding stats', 'Personal Info']

for i, df in enumerate(dataframes):
    transposed_df = df.transpose()
    transposed_df.columns = transposed_df.iloc[0]
    transposed_df = transposed_df[1:]
    file_name = f'{names[i]}.csv'
    transposed_df.to_csv(file_name, index=False)

