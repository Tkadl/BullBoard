import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

def main():
    # === USER CONFIGURATION ===
    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'JPM', 'V', 'UNH',
        'HD', 'MA', 'LLY', 'ABBV', 'MRK', 'XOM', 'PFE', 'PEP', 'COST', 'WMT',
        'BAC', 'DIS', 'NKE', 'CVX', 'CSCO', 'KO', 'TMO', 'QCOM', 'ORCL', 'ABT'
    ]
    start_date = "2024-01-01"
    end_date = datetime.today().strftime("%Y-%m-%d")
    min_days_needed = 65
    yield_thresh = 0.01          # 1% daily yield
    risk_thresh = 0.06           # Custom risk score
    rolling_vol_days = 21
    rolling_drawdown_days = 63
    batch_size = 40

    good_dfs = []
    bad_tickers = []

    # Download data in batches
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i+batch_size]
        try:
            raw = yf.download(
                tickers=" ".join(batch),
                start=start_date,
                end=end_date,
                group_by='ticker',
                auto_adjust=True,
                progress=False,
                threads=True
            )
            if len(batch) == 1:
                ticker = batch[0]
                temp = raw.copy()
                if temp.empty:
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
                            bad_tickers.append(ticker)
                            continue
                        temp['symbol'] = ticker
                        temp['Date'] = temp.index
                        good_dfs.append(temp.reset_index(drop=True))
                    except Exception:
                        bad_tickers.append(ticker)
        except Exception:
            bad_tickers.extend(batch)

    if good_dfs:
        df = pd.concat(good_dfs, ignore_index=True)
        df = df[['symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    else:
        print("No data fetched — check your internet connection and ticker list.")
        return

    # TIMESTAMP DATA DOWNLOAD
    download_time = datetime.now()
    df['download_time'] = download_time.strftime('%Y-%m-%d %H:%M')

    # DATA VALIDATION BEFORE CALC
    bad_symbols = []
    for sym, group in df.groupby('symbol'):
        if group.shape[0] < min_days_needed:
            bad_symbols.append(sym)
    df = df[~df['symbol'].isin(bad_symbols)]

    # ROLLING ANALYTICS
    df = df.sort_values(['symbol', 'Date']).reset_index(drop=True)
    df['daily_return'] = df.groupby('symbol')['Close'].pct_change()
    df['volatility_21'] = df.groupby('symbol')['daily_return'].rolling(rolling_vol_days).std().reset_index(0, drop=True)
    df['rolling_yield_21'] = df.groupby('symbol')['daily_return'].rolling(rolling_vol_days).mean().reset_index(0, drop=True)
    df['sharpe_21'] = (df['rolling_yield_21'] / df['volatility_21']) * np.sqrt(252)
    df['max_drawdown_63'] = df.groupby('symbol')['Close'].rolling(rolling_drawdown_days)\
        .apply(lambda x: (np.max(x) - np.min(x)) / np.max(x) if len(x) > 0 and np.max(x) != 0 else 0, raw=False)\
        .reset_index(0, drop=True)
    df['custom_risk_score'] = df['volatility_21'] * 0.7 + df['max_drawdown_63'] * 0.3

    # Get each stock's latest analytics
    latest = df.sort_values('Date').groupby('symbol').tail(1)
    latest = latest[['symbol', 'Date', 'custom_risk_score', 'rolling_yield_21', 'sharpe_21', 'volatility_21', 'max_drawdown_63']].copy()
    latest = latest.sort_values('custom_risk_score', ascending=False)
    latest.reset_index(drop=True, inplace=True)

    # Save summary table for Streamlit app
    df.to_csv("latest_results.csv", index=False)

if __name__ == "__main__":
    main()
