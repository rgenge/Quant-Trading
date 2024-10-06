import pandas as pd
import numpy as np

# Load the data
df = pd.read_excel('allstocks.xlsx')
print("Original Data:")
print(df)
print("\n")

# Ensure the data is sorted by date
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(['Stock Name', 'Date'])

# Calculate quarter-over-quarter growth rates
df['Net_Income_Growth'] = df.groupby('Stock Name')['Net Income'].pct_change()
df['Revenue_Growth'] = df.groupby('Stock Name')['Total Revenue'].pct_change()

# Function to calculate price target
def calculate_price_target(current_price, net_income_growth, revenue_growth):
    # We'll use a simple average of net income and revenue growth
    avg_growth = (net_income_growth + revenue_growth) / 2

    # The price target will be the current price adjusted by the average growth
    price_target = current_price * (1 + avg_growth)

    return price_target

# Analyze the last quarter
last_quarter = df.groupby('Stock Name').last()

results = []
for stock_name, data in last_quarter.iterrows():
    current_price = data['Close']
    net_income_growth = data['Net_Income_Growth']
    revenue_growth = data['Revenue_Growth']

    price_target = calculate_price_target(current_price, net_income_growth, revenue_growth)

    growth_prediction = "Grow" if price_target > current_price else "Not Grow"

    results.append({
        'Stock Name': stock_name,
        'Current Price': current_price,
        'Net Income Growth': net_income_growth,
        'Revenue Growth': revenue_growth,
        'Price Target': price_target,
        'Prediction': growth_prediction
    })

results_df = pd.DataFrame(results)
pd.set_option('display.float_format', '{:.2f}'.format)
print("Analysis Results:")
print(results_df)
print("\n")

# Detailed analysis for JPM
jpm_data = df[df['Stock Name'] == 'META'].iloc[-2:]  # Last two quarters
print("Detailed Analysis for JPM:")
print(jpm_data[['Date', 'Net Income', 'Total Revenue', 'Close']])
print("\n")

jpm_net_income_growth = (jpm_data['Net Income'].iloc[1] - jpm_data['Net Income'].iloc[0]) / jpm_data['Net Income'].iloc[0]
jpm_revenue_growth = (jpm_data['Total Revenue'].iloc[1] - jpm_data['Total Revenue'].iloc[0]) / jpm_data['Total Revenue'].iloc[0]
jpm_current_price = jpm_data['Close'].iloc[1]

jpm_price_target = calculate_price_target(jpm_current_price, jpm_net_income_growth, jpm_revenue_growth)

print(f"JPM Net Income Growth: {jpm_net_income_growth:.2%}")
print(f"JPM Revenue Growth: {jpm_revenue_growth:.2%}")
print(f"JPM Current Price: ${jpm_current_price:.2f}")
print(f"JPM Price Target: ${jpm_price_target:.2f}")
print(f"Prediction: {'Grow' if jpm_price_target > jpm_current_price else 'Not Grow'}")
