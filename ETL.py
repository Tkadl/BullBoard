# 1: INSTALL DEPENDENCIES
!pip install yfinance pandas numpy > /dev/null 2>&1
print("✔️ All dependencies installed")


# 2: USER CONFIGURATION
tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'JPM', 'V', 'UNH',
    'HD', 'MA', 'LLY', 'ABBV', 'MRK', 'XOM', 'PFE', 'PEP', 'COST', 'WMT',
    'BAC', 'DIS', 'NKE', 'CVX', 'CSCO', 'KO', 'TMO', 'QCOM', 'ORCL', 'ABT']
# Data window to download
start_date = "2024-01-01"
end_date = None   # Set to None for "today", or "YYYY-MM-DD"

# Minimum days of data required (for rolling windows, see later steps)
min_days_needed = 65         # 63 for safe drawdown lookback

# Alert thresholds
yield_thresh = 0.01          # 1% daily yield
risk_thresh = 0.06           # Custom risk score

# Analytics rolling window parameters
rolling_vol_days = 21        # Window for volatility/yield
rolling_drawdown_days = 63   # Window for max drawdown

# yfinance download batching (for > 40 tickers go in batches)
batch_size = 40


# 3: BATCH STOCK DATA DOWNLOAD
import yfinance as yf
import pandas as pd
from datetime import datetime

start_date = "2024-01-01"
end_date = datetime.today().strftime("%Y-%m-%d")
batch_size = 40   # stay well below yfinance/Pandas plot limits

good_dfs = []
bad_tickers = []

# In case I wanna work in batches for > 50 tickers
for i in range(0, len(tickers), batch_size):
    batch = tickers[i:i+batch_size]
    print(f"\nFetching batch: {batch}")
    try:
        raw = yf.download(
            tickers = " ".join(batch),
            start=start_date,
            end=end_date,
            group_by='ticker',
            auto_adjust=True,
            progress=False,
            threads=True
        )
        # For a single ticker, yfinance does NOT create a column for the ticker symbol and returns a plain DataFrame
        if len(batch) == 1:
            ticker = batch[0]
            temp = raw.copy()
            if temp.empty:
                print(f"⚠️ No data for {ticker} — Skipped.")
                bad_tickers.append(ticker)
                continue
            temp['symbol'] = ticker
            temp['Date'] = temp.index
            good_dfs.append(temp.reset_index(drop=True))
        else:
            for ticker in batch:
                try:
                    temp = raw[ticker].copy()
                    if temp.empty:
                        print(f"⚠️ No data for {ticker} — Skipped.")
                        bad_tickers.append(ticker)
                        continue
                    temp['symbol'] = ticker
                    temp['Date'] = temp.index
                    good_dfs.append(temp.reset_index(drop=True))
                except Exception as e:
                    print(f"Warning: could not fetch or parse {ticker}: {e}")
                    bad_tickers.append(ticker)
    except Exception as e:
        print(f"❌ Error fetching batch {batch}: {e}")
        bad_tickers.extend(batch)

if good_dfs:
    df = pd.concat(good_dfs, ignore_index=True)
    df = df[['symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    print(f"\n✅ Fetched data for {df['symbol'].nunique()} stocks.")
else:
    print("No data fetched — check your internet connection and ticker list.")

if bad_tickers:
    print("\nThe following tickers had issues or are missing data:")
    print(bad_tickers)

df.head()


# 4: TIMESTAMP DATA DOWNLOAD
download_time = datetime.now()
print(f"📁 Data last downloaded: {download_time.strftime('%Y-%m-%d %H:%M')}")

# Optionally, attach to every row for later reference or export:
df['download_time'] = download_time.strftime('%Y-%m-%d %H:%M')


# 5: DATA VALIDATION BEFORE CALCULATION
min_days_needed = 65  # At least 63 for rolling analysis to be meaningful
bad_symbols = []

for sym, group in df.groupby('symbol'):
    if group.shape[0] < min_days_needed:
        bad_symbols.append(sym)
        print(f"⚠️ {sym} has only {group.shape[0]} days of data (need at least {min_days_needed}).")

# Remove sparse tickers
df = df[~df['symbol'].isin(bad_symbols)]

if bad_symbols:
    print(f"Filtered out these tickers for too little data: {bad_symbols}")
else:
    print("All tickers have enough data for reliable analysis!")


# 6: ROLLING RISK/YIELD ANALYSIS
import numpy as np

df = df.sort_values(['symbol', 'Date']).reset_index(drop=True)
df['daily_return'] = df.groupby('symbol')['Close'].pct_change()
df['volatility_21'] = df.groupby('symbol')['daily_return'].rolling(21).std().reset_index(0, drop=True)
df['rolling_yield_21'] = df.groupby('symbol')['daily_return'].rolling(21).mean().reset_index(0, drop=True)
df['sharpe_21'] = (df['rolling_yield_21'] / df['volatility_21']) * np.sqrt(252)
df['max_drawdown_63'] = df.groupby('symbol')['Close'].rolling(63)\
    .apply(lambda x: (np.max(x) - np.min(x)) / np.max(x) if len(x)>0 and np.max(x)!=0 else 0, raw=False)\
    .reset_index(0, drop=True)
df['custom_risk_score'] = df['volatility_21'] * 0.7 + df['max_drawdown_63'] * 0.3

# Get each stock's latest analytics
latest = df.sort_values('Date').groupby('symbol').tail(1)
latest = latest[['symbol', 'Date', 'custom_risk_score', 'rolling_yield_21', 'sharpe_21', 'volatility_21', 'max_drawdown_63']]
latest = latest.sort_values('custom_risk_score', ascending=False)
latest.reset_index(drop=True, inplace=True)
latest.head()


# 7: ALERT GENERATION
# Set threshold values
yield_thresh = 0.01  # 1% daily rolling yield (modify as needed)
risk_thresh = 0.06   # your custom risk score threshold

alerts = []
for _, row in latest.iterrows():
    date_str = row['Date'].strftime('%Y-%m-%d')  # Safely format Timestamp as a string
    if (row['custom_risk_score'] > risk_thresh) or (row['rolling_yield_21'] > yield_thresh):
        alerts.append(f"⚠️ ALERT: {row['symbol']} | Risk: {row['custom_risk_score']:.3f} | Yield: {row['rolling_yield_21']:.2%} | Date: {date_str}")
print("\n".join(alerts) if alerts else "No current alerts.")

# Optionally, show all stocks ranked by risk or yield:
latest[['symbol', 'custom_risk_score', 'rolling_yield_21', 'sharpe_21']].head(10)


# 8: SUMMARY TABLE/TOP N DISPLAY
# Top 10 by risk
print("TOP 10 by risk score:")
top_risk = latest.sort_values('custom_risk_score', ascending=False).head(10)
print(top_risk[['symbol', 'custom_risk_score', 'rolling_yield_21']])

# Top 10 by rolling yield
print("\nTOP 10 by rolling yield:")
top_yield = latest.sort_values('rolling_yield_21', ascending=False).head(10)
print(top_yield[['symbol', 'rolling_yield_21', 'custom_risk_score']])


# 9: VISUALIZATION
import matplotlib.pyplot as plt

# Plot top 3 riskiest stocks
for symbol in top_risk['symbol'].tolist():
    stock = df[df['symbol'] == symbol]
    plt.figure(figsize=(12,4))
    plt.plot(stock['Date'], stock['Close'], label=f'{symbol} Close')
    plt.title(f"{symbol} | Custom Risk: {stock['custom_risk_score'].iloc[-1]:.3f}")
    plt.grid()
    plt.legend()
    plt.show()
