import pandas as pd
from sqlalchemy import create_engine

# Load your CSV file into a pandas DataFrame
csv_file = r"C:\Users\sspon\Downloads\archive (27)\pib_per_capita_countries_dataset.csv"
df = pd.read_csv(csv_file)

# Create an SQLite database in memory (or you can specify a file-based database)
engine = create_engine('sqlite:///financial_data.db', echo=True)

# Write the DataFrame to SQLite
df.to_sql('financial_data', con=engine, index=False, if_exists='replace')

print("CSV data loaded into SQLite database successfully.")
