import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import json
import numpy as np

def fetch_treasury_yield(ticker, date):
    """
    Fetch the Treasury yield for a given ticker and date from Yahoo Finance.
    
    Parameters:
    ticker (str): The ticker symbol for the Treasury yield (e.g., '^IRX' for 1-year, '^FVX' for 5-year, '^TNX' for 10-year).
    date (str): The target date for the yield in 'YYYY-MM-DD' format.
    
    Returns:
    float: The yield for the exact date if available, otherwise the latest available yield within the specified date range.
    """
    target_date = datetime.strptime(date, '%Y-%m-%d')
    start_date = target_date - timedelta(days=7)
    end_date = target_date + timedelta(days=1)  # Fetch one extra day to ensure we include the target date
    data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    
    if data.empty:
        raise ValueError(f"No data found for {ticker} around {date}")
    
    # Check if target date is in the fetched data
    if date in data.index.strftime('%Y-%m-%d'):
        latest_yield = data.loc[date, 'Close']
    else:
        # If the exact date is not available, get the latest available yield within the range
        latest_yield = data['Close'].iloc[-1]
    
    return round(latest_yield, 2)

# Load configuration
with open('config/config.json') as config_file:
    config = json.load(config_file)

tickers = config['tickers']
dates = config['dates']

# Prepare to collect results
results = []

# Fetch yields for each ticker and date
for ticker_name, ticker_symbol in tickers.items():
    row = [ticker_name]
    for date in dates:
        try:
            latest_yield = fetch_treasury_yield(ticker_symbol, datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d'))
            row.append(latest_yield)
        except Exception as e:
            print(f"Error fetching data for {ticker_name} on {date}: {e}")
            row.append(None)
    results.append(row)

# Create DataFrame
columns = ['Yield Type'] + dates
df = pd.DataFrame(results, columns=columns)

# Extract known maturities and years from tickers
known_maturities = {ticker_name: int(ticker_name.split('-')[0]) for ticker_name in tickers}
max_maturity = max(known_maturities.values())
intermediate_maturities = [i for i in range(1, max_maturity + 1) if i not in known_maturities.values()]

all_maturities = sorted(set(list(known_maturities.values()) + intermediate_maturities))

interpolated_results = {maturity: [] for maturity in all_maturities}

for date in dates:
    known_yields = []
    for ticker_name, maturity in known_maturities.items():
        yield_values = df.loc[df['Yield Type'] == ticker_name, date].values
        if len(yield_values) > 0:
            yield_value = float(np.mean(yield_values))  # Use the average if there are multiple values
            known_yields.append((maturity, yield_value))
    
    if known_yields:
        known_yields = sorted(known_yields)  # Sort by maturity
        known_maturity_years, known_yield_values = zip(*known_yields)
    
        # Debug statements
        print(f"Date: {date}")
        print(f"Known maturities: {known_maturity_years}")
        print(f"Known yields: {known_yield_values}")
    
        interpolated_yields = np.interp(intermediate_maturities, known_maturity_years, known_yield_values)
    
        for maturity in all_maturities:
            if maturity in known_maturity_years:
                interpolated_results[maturity].append(known_yield_values[known_maturity_years.index(maturity)])
            else:
                interpolated_results[maturity].append(round(interpolated_yields[intermediate_maturities.index(maturity)], 2))
    else:
        for maturity in all_maturities:
            interpolated_results[maturity].append(None)

# Convert the results to a DataFrame
interpolated_df = pd.DataFrame(interpolated_results, index=dates)

# Transpose the DataFrame so that dates are columns
interpolated_df = interpolated_df.transpose()
interpolated_df.index.name = 'Maturity'
interpolated_df.columns.name = 'Date'

# Rename index to use "Treasury Rate" instead of "Bill Rate"
interpolated_df.index = [f"{maturity}-year" for maturity in interpolated_df.index]

# Save to CSV
output_file = 'output/treasury_yield_results.csv'
interpolated_df.to_csv(output_file)

print(f"Results saved to {output_file}")
