import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time  # Add this import

def get_sp500_symbols():
    """Get S&P 500 symbols dynamically"""
    # Core S&P 500 symbols (representative list - you can expand this)
    sp500_symbols = [
        # Technology
        'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'NVDA', 'TSLA', 'META', 'NFLX', 'ADBE',
        'CRM', 'ORCL', 'CSCO', 'INTC', 'AMD', 'QCOM', 'TXN', 'AVGO', 'PYPL', 'UBER',
        'SNOW', 'TWLO', 'ZM', 'DOCU', 'OKTA', 'CRWD', 'DDOG', 'NET', 'TEAM', 'WDAY',
        
        # Financial Services
        'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'TFC', 'PNC', 'COF',
        'AXP', 'BLK', 'SCHW', 'CB', 'ICE', 'CME', 'SPGI', 'MCO', 'AON', 'MMC',
        
        # Healthcare
        'UNH', 'JNJ', 'PFE', 'ABBV', 'TMO', 'ABT', 'LLY', 'MRK', 'BMY', 'AMGN',
        'GILD', 'CVS', 'CI', 'ANTM', 'HUM', 'CNC', 'BIIB', 'REGN', 'VRTX', 'ISRG',
        
        # Consumer Discretionary
        'AMZN', 'TSLA', 'HD', 'NKE', 'MCD', 'LOW', 'SBUX', 'TJX', 'BKNG', 'MAR',
        'GM', 'F', 'CCL', 'RCL', 'NCLH', 'MGM', 'WYNN', 'LVS', 'DIS', 'CMCSA',
        
        # Consumer Staples
        'WMT', 'PG', 'KO', 'PEP', 'COST', 'WBA', 'CVS', 'EL', 'CL', 'KMB',
        'GIS', 'K', 'HSY', 'SJM', 'CPB', 'CAG', 'KHC', 'MDLZ', 'MNST', 'KDP',
        
        # Communication Services
        'GOOGL', 'META', 'NFLX', 'DIS', 'CMCSA', 'VZ', 'T', 'TMUS', 'CHTR', 'ATVI',
        
        # Industrials
        'BA', 'CAT', 'HON', 'UPS', 'RTX', 'LMT', 'GE', 'MMM', 'FDX', 'NOC',
        'UNP', 'CSX', 'NSC', 'DAL', 'UAL', 'AAL', 'LUV', 'JBLU', 'ALK', 'SAVE',
        
        # Materials
        'LIN', 'APD', 'ECL', 'FCX', 'NEM', 'DOW', 'DD', 'PPG', 'SHW', 'NUE',
        
        # Energy
        'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'PSX', 'VLO', 'MPC', 'OXY', 'BKR',
        
        # Utilities
        'NEE', 'DUK', 'SO', 'D', 'EXC', 'XEL', 'SRE', 'AEP', 'ES', 'AWK',
        
        # Real Estate
        'AMT', 'CCI', 'PLD', 'EQIX', 'PSA', 'EXR', 'AVB', 'EQR', 'WELL', 'SPG',
        
        # Add your original 30 symbols to ensure continuity
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'JPM', 'V', 'UNH',
        'HD', 'MA', 'LLY', 'ABBV', 'MRK', 'XOM', 'PFE', 'PEP', 'COST', 'WMT',
        'BAC', 'DIS', 'NKE', 'CVX', 'CSCO', 'KO', 'TMO', 'QCOM', 'ORCL', 'ABT'
    ]
    
    # Remove duplicates and return
    return list(set(sp500_symbols))

def main():
    # === USER CONFIGURATION ===
    tickers = get_sp500_symbols()  # Use dynamic S&P 500 list
    start_date = "2024-01-01"
    end_date = datetime.today().strftime("%Y-%m-%d")
    min_days_needed = 65
    yield_thresh = 0.01          # 1% daily yield
    risk_thresh = 0.06           # Custom risk score
    rolling_vol_days = 21
    rolling_drawdown_days = 63
    batch_size = 30  # Reduced batch size for better reliability with more symbols
    delay_between_batches = 2  # Add delay between batches

    print(f"Fetching data for {len(tickers)} symbols...")
    
    good_dfs = []
    bad_tickers = []

    # Download data in batches with progress tracking
    total_batches = (len(tickers) + batch_size - 1) // batch_size
    
    for batch_num, i in enumerate(range(0, len(tickers), batch_size), 1):
        batch = tickers[i:i+batch_size]
        print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} symbols)...")
        
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
                if temp.empty or len(temp) < min_days_needed:
                    bad_tickers.append(ticker)
                    continue
                temp['symbol'] = ticker
                temp['Date'] = temp.index
                good_dfs.append(temp.reset_index(drop=True))
            else:
                for ticker in batch:
                    try:
                        temp = raw[ticker].copy()
                        if temp.empty or len(temp) < min_days_needed:
                            bad_tickers.append(ticker)
                            continue
                        temp['symbol'] = ticker
                        temp['Date'] = temp.index
                        good_dfs.append(temp.reset_index(drop=True))
                    except Exception as e:
                        print(f"Error processing {ticker}: {str(e)}")
                        bad_tickers.append(ticker)
                        
        except Exception as e:
            print(f"Error with batch {batch_num}: {str(e)}")
            bad_tickers.extend(batch)
        
        # Add delay between batches to be respectful to the API
        if batch_num < total_batches:
            time.sleep(delay_between_batches)

    print(f"Successfully fetched: {len(good_dfs)} symbols")
    print(f"Failed to fetch: {len(bad_tickers)} symbols")
    if bad_tickers:
        print(f"Failed symbols: {bad_tickers[:10]}{'...' if len(bad_tickers) > 10 else ''}")

    # Rest of your existing code remains the same...
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
    print(f"Data saved to latest_results.csv with {len(df)} total records for {df['symbol'].nunique()} unique symbols")

if __name__ == "__main__":
    main()
