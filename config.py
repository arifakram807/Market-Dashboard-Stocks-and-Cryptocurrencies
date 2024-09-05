import pandas as pd
import time
from datetime import datetime

# Convert 'YYYY-MM-DD' to UNIX timestamp
def date_to_unix(date_str):
    return int(time.mktime(time.strptime(date_str, "%Y-%m-%d")))

# Get the current date in 'YYYY-MM-DD' format
current_date = datetime.now().strftime('%Y-%m-%d')

# Define the start date for the data
start_date = '2023-07-01'  # Adjust this as needed
period1 = date_to_unix(start_date)
period2 = date_to_unix(current_date)

# Read the CSV file to get the list of stock symbols and their types
file_path = 'C:/Users/arifa/OneDrive/Desktop/course/Stock Market Dashboard/trackers.csv'  # Replace with the path to your CSV file
symbols_df = pd.read_csv(file_path)
trackers = symbols_df[['Symbol', 'Type']].to_dict(orient='records')

# Initialize a list to hold all data
data_frames = []

for tracker in trackers:
    symbol = tracker['Symbol']
    type_of_asset = tracker['Type']
    
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval=1d&events=history&includeAdjustedClose=true'
    
    try:
        # Fetch data from Yahoo Finance
        df = pd.read_csv(url)
        df['Symbol'] = symbol  # Add a column for the stock symbol
        df['Type'] = type_of_asset  # Add a column for the type (Stock or Crypto)
        data_frames.append(df)  # Append the dataframe to the list
        print(f"Data for {symbol} downloaded successfully.")
    except Exception as e:
        print(f"Failed to download data for {symbol}: {e}")

# Concatenate all dataframes into a single dataframe
combined_data = pd.concat(data_frames, ignore_index=True)

# Reorder columns for better readability
combined_data = combined_data[['Symbol', 'Type', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

# Display the combined dataframe
print(combined_data.head())