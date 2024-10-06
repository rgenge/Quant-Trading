import yfinance as yf
import pandas as pd
import requests
import os

stock_name = input("Enter the stock symbol (e.g., IBM): ").upper()
apikey = "demo"
url = (
    "https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol="
    + stock_name
    + "&apikey="
    + apikey
)
r = requests.get(url)
data = r.json()
# Append data
def append_to_excel(fpath, df):
    if os.path.exists(fpath):
        x = pd.read_excel(fpath)
    else:
        x = pd.DataFrame()

    dfNew = pd.concat([df, x])
    dfNew.to_excel(fpath, index=False)

# Prepare the data
records = []
for report in data["quarterlyReports"]:
    fiscal_date_ending = report["fiscalDateEnding"]
    year = int(fiscal_date_ending.split("-")[0])

    if 2017 <= year <= 2023:
        net_income = report["netIncome"]
        total_revenue = report["totalRevenue"]
        records.append(
            {
                "Stock Name": stock_name,
                "Date": fiscal_date_ending,
                "Net Income": int(net_income),
                "Total Revenue": int(total_revenue),
            }
        )
# Create a DataFrame
df = pd.DataFrame(records)
append_to_excel("temp.xlsx", df)

# Step 1: Load the existing Excel file
file_path = "temp.xlsx"  # Replace with your actual file path

data = pd.read_excel(file_path)

# Step 2: Set up to retrieve stock history
tickers = yf.Ticker(stock_name)

# Initialize a list to store close values
close_values = []

# Step 3: Iterate through the DataFrame rows
for index, row in data.iterrows():
#    stock_name = row["Stock Name"]
    date = pd.to_datetime(row["Date"])  # Ensure date is in datetime format

    # Get the historical data for the specific stock
    history = tickers.history(period="10y")
    history.index =  pd.to_datetime(history.index).tz_localize(None)
    history.to_excel(os.path.join("history",stock_name + "history.xlsx"), index=True)
    # Filter the historical data for the specified date
    if date in history.index:
        close_value = history.loc[date]["Close"]
    else:
        # If the exact date isn't available, check for 26th or 28th of the same month and year
        month_data = history[
            (history.index.month == date.month) & (history.index.year == date.year)
        ]

        if (28 in month_data.index.day.tolist()):
            close_value = month_data.loc[month_data.index.day == 28]["Close"].values[0]
        elif (26 in month_data.index.day.tolist()):
            close_value = month_data.loc[month_data.index.day == 26]["Close"].values[0]
        else:
            close_value = None  # No available close value for this date

    close_values.append(close_value)

# Step 4: Add the close values to the DataFrame
data["Close"] = close_values

# Step 5: Save the updated DataFrame back to Excel
append_to_excel("allstocks.xlsx", data)
data.to_excel(os.path.join("stocks",stock_name + ".xlsx"), index=False)
os.remove('temp.xlsx')
