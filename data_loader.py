import pandas as pd
from sqlalchemy import create_engine

# Load Excel files
file_5308 = pd.read_excel('5308.xlsx', sheet_name=None)
file_5329 = pd.read_excel('5329.xlsx', sheet_name=None)

# Combine datasets
data_5308 = {sheet_name: file_5308[sheet_name] for sheet_name in file_5308.keys()}
data_5329 = {sheet_name: file_5329[sheet_name] for sheet_name in file_5329.keys()}

# Define database connection
engine = create_engine('postgresql://postgres:postgres@localhost:5432/nunamdb')

# Save data to the database
for sheet_name, df in data_5308.items():
    df.to_sql(f'5308_{sheet_name}', con=engine, if_exists='replace', index=False)

for sheet_name, df in data_5329.items():
    df.to_sql(f'5329_{sheet_name}', con=engine, if_exists='replace', index=False)
