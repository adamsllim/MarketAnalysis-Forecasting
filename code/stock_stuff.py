# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------
import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Setup: Create data folder
# ------------------------------------------------------------
os.makedirs("data", exist_ok=True)


# ------------------------------------------------------------
# Step 1: Define tickers
# ------------------------------------------------------------
tickers = {
    "WTI": "CL=F",      # West Texas Intermediate (US benchmark)
    "Brent": "BZ=F",    # Brent Crude (Global benchmark)
    "NatGas": "NG=F"    # Natural Gas Futures
}


# ------------------------------------------------------------
# Step 2: Download historical price data
# ------------------------------------------------------------
print("Downloading price data...")
data = yf.download(
    list(tickers.values()),
    start="2015-01-01",
    end=None
)

# Keep only closing prices and rename columns
prices = data["Close"].copy()
prices.columns = tickers.keys()

print("Sample of downloaded data:")
print(prices.head())


# ------------------------------------------------------------
# Step 3: Save the data
# ------------------------------------------------------------
prices.to_csv("data/raw_prices.csv")


# ------------------------------------------------------------
# Step 4: Load and clean the data
# ------------------------------------------------------------
df = pd.read_csv("data/raw_prices.csv", parse_dates=["Date"], index_col="Date")

# Forward-fill missing values
df = df.ffill()

# Drop any remaining missing rows
df = df.dropna(subset=["WTI", "Brent"])

# Add simple features
df["WTI_Returns"] = df["WTI"].pct_change()
df["Brent_Returns"] = df["Brent"].pct_change()

df["WTI_MA30"] = df["WTI"].rolling(30).mean()
df["Brent_MA30"] = df["Brent"].rolling(30).mean()

# Save cleaned dataset
df.to_csv("data/clean_prices.csv")

print("\nCleaned data preview:")
print(df.head())


# ------------------------------------------------------------
# Step 5: Plot WTI vs Brent
# ------------------------------------------------------------
plt.style.use("seaborn-v0_8")  # cleaner visual style

plt.figure(figsize=(12, 6))
plt.plot(prices["WTI"], label="WTI")
plt.plot(prices["Brent"], label="Brent")


plt.title("WTI vs Brent Prices (2015–Present)", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# check...
print("Script started")
print(df.index.min(), df.index.max())
print(df.shape)


# ------------------------------------------------------------
# Not finished...
# ------------------------------------------------------------

