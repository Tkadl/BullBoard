import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time  # Add this import

def get_sp500_symbols():
    """Get complete S&P 500 symbols list"""
    sp500_symbols = [
        # A
        'A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACN', 'ADBE', 
        'ADI', 'ADM', 'ADP', 'ADSK', 'AEE', 'AEP', 'AES', 'AFL', 'AIG', 'AIZ', 
        'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'AMAT', 'AMCR', 'AMD', 
        'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS', 'AON', 'AOS', 'APA', 
        'APD', 'APH', 'APTV', 'ARE', 'ATO', 'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 
        'AXP', 'AZO',
        
        # B
        'BA', 'BAC', 'BALL', 'BAX', 'BBWI', 'BBY', 'BDX', 'BEN', 'BF-B', 'BIIB', 
        'BIO', 'BK', 'BKNG', 'BKR', 'BLK', 'BMY', 'BR', 'BRK-B', 'BRO', 'BSX', 'BWA',
        
        # C
        'C', 'CAG', 'CAH', 'CARR', 'CAT', 'CB', 'CBOE', 'CBRE', 'CCI', 'CCL', 
        'CDAY', 'CDNS', 'CDW', 'CE', 'CEG', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 
        'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COO', 
        'COP', 'COST', 'CPB', 'CPRT', 'CRM', 'CSCO', 'CSX', 'CTAS', 'CTLT', 'CTRA', 
        'CTSH', 'CTVA', 'CVS', 'CVX', 'CZR',
        
        # D
        'D', 'DAL', 'DD', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISH', 
        'DLR', 'DLTR', 'DOV', 'DOW', 'DPZ', 'DRE', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN',
        
        # E
        'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR', 'ENPH', 'EOG', 
        'EPAM', 'EQIX', 'EQR', 'ES', 'ESS', 'ETN', 'ETR', 'ETSY', 'EVRG', 'EW', 
        'EXC', 'EXPD', 'EXPE', 'EXR',
        
        # F
        'F', 'FANG', 'FAST', 'FB', 'FBHS', 'FCX', 'FDS', 'FDX', 'FE', 'FFIV', 'FIS', 
        'FISV', 'FITB', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRC', 'FRT', 'FTNT', 'FTV',
        
        # G
        'GD', 'GE', 'GILD', 'GIS', 'GL', 'GLW', 'GM', 'GNRC', 'GOOG', 'GOOGL', 
        'GPC', 'GPN', 'GRMN', 'GS', 'GWW',
        
        # H
        'HAL', 'HAS', 'HBAN', 'HBI', 'HCA', 'HD', 'HES', 'HIG', 'HII', 'HLT', 'HOLX', 
        'HON', 'HPE', 'HPQ', 'HRL', 'HSIC', 'HST', 'HSY', 'HUM', 'HWM',
        
        # I
        'IBM', 'ICE', 'IDXX', 'IEX', 'IFF', 'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 
        'IP', 'IPG', 'IPGP', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ',
        
        # J
        'JBHT', 'JCI', 'JKHY', 'JNJ', 'JNPR', 'JPM', 'JWN',
        
        # K
        'K', 'KEY', 'KEYS', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KR', 'KSS',
        
        # L
        'L', 'LDOS', 'LEG', 'LEN', 'LH', 'LHX', 'LIN', 'LKQ', 'LLY', 'LMT', 'LNC', 
        'LNT', 'LOW', 'LRCX', 'LUMN', 'LUV', 'LVS', 'LW', 'LYB', 'LYV',
        
        # M
        'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 
        'META', 'MGM', 'MHK', 'MKC', 'MKTX', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 
        'MOH', 'MOS', 'MPC', 'MPWR', 'MRK', 'MRNA', 'MRO', 'MS', 'MSCI', 'MSFT', 
        'MSI', 'MTB', 'MTCH', 'MTD', 'MU', 'NCLH', 'NDAQ', 'NDSN', 'NEE', 'NEM', 
        'NFLX', 'NI', 'NKE', 'NLOK', 'NLSN', 'NOC', 'NOW', 'NRG', 'NSC', 'NTAP', 
        'NTRS', 'NUE', 'NVDA', 'NVR', 'NWL', 'NWS', 'NWSA',
        
        # O
        'ODFL', 'OGN', 'OKE', 'OMC', 'ORCL', 'ORLY', 'OTIS', 'OXY',
        
        # P
        'PARA', 'PAYC', 'PAYX', 'PCAR', 'PCG', 'PEAK', 'PEG', 'PEP', 'PFE', 'PFG', 
        'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 
        'POOL', 'PPG', 'PPL', 'PRU', 'PSA', 'PSX', 'PTC', 'PVH', 'PWR', 'PXD', 'PYPL',
        
        # Q
        'QCOM', 'QRVO', 'RCL', 'RE', 'REG', 'REGN', 'RF', 'RHI', 'RJF', 'RL', 'RMD', 
        'ROK', 'ROL', 'ROP', 'ROST', 'RSG', 'RTX',
        
        # S
        'SBAC', 'SBNY', 'SBUX', 'SCHW', 'SEDG', 'SEE', 'SHW', 'SIVB', 'SJM', 'SLB', 
        'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRE', 'STE', 'STT', 'STX', 'STZ', 'SWK', 
        'SWKS', 'SYF', 'SYK', 'SYY',
        
        # T
        'T', 'TAP', 'TDG', 'TDY', 'TECH', 'TEL', 'TER', 'TFC', 'TFX', 'TGT', 'TJX', 
        'TMO', 'TMUS', 'TPG', 'TPR', 'TRMB', 'TROW', 'TRV', 'TSCO', 'TSLA', 'TSN', 
        'TT', 'TTWO', 'TWTR', 'TXN', 'TXT', 'TYL',
        
        # U
        'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNP', 'UPS', 'URI', 'USB', 'V', 'VFC', 
        'VLO', 'VMC', 'VNO', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VTRS', 'VZ',
        
        # W
        'WAB', 'WAT', 'WBA', 'WBD', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WM', 'WMB', 
        'WMT', 'WRB', 'WRK', 'WST', 'WTW', 'WY',
        
        # X-Z
        'XRAY', 'XYL', 'YUM', 'ZBH', 'ZBRA', 'ZION', 'ZTS'
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
