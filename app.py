import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="BullBoard - Risk/Yield Dashboard",
    layout="wide"
)

st.title("🐂 BullBoard: Stock Risk & Yield Planner")

st.markdown(
    """
    <div style="background-color: #262730; border-radius: 10px; padding: 18px; margin-bottom:20px;">
    <h3 style="margin-bottom:10px;color:#FAFAFA;">Welcome to BullBoard!</h3>
    <p style="color:#FAFAFA;">Analyze stock risk and yield, get actionable insights, and visualize performance easily.</p>
    </div>
    """, unsafe_allow_html=True
)

# Button to run ETL pipeline
if st.button("Run ETL Pipeline Now"):
    with st.spinner("Running ETL pipeline, please wait..."):
        import etl
        etl.main()
    st.success("ETL Pipeline complete! Reloading data...")
    st.rerun()

# SAFELY load CSV
try:
    df = pd.read_csv("latest_results.csv", parse_dates=["Date"])
except Exception as e:
    st.warning("No results file found or failed to read. Please run the ETL pipeline first.")
    st.exception(e)
    st.stop()

if df.empty or ('symbol' not in df.columns):
    st.warning("ETL produced empty or invalid data! Double check your ETL process and data source.")
    st.stop()

st.write(f"**Last analysis for {df['symbol'].nunique()} stocks.**")

# --- Ticker Dropdown for Filtering ---
unique_syms = sorted(df['symbol'].unique())
selected_syms = st.multiselect(
    "Select stocks for analysis",
    unique_syms,
    default=unique_syms[:5] if len(unique_syms) >= 5 else unique_syms
)
filtered_df = df[df['symbol'].isin(selected_syms)] if selected_syms else df

# --- Date Range Picker ---
if 'Date' in filtered_df.columns and not filtered_df.empty:
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    min_date = filtered_df['Date'].min()
    max_date = filtered_df['Date'].max()
    date_range = st.date_input(
        "Select date window for analysis",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="date_range"
    )
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['Date'] >= pd.to_datetime(start_date)) &
            (filtered_df['Date'] <= pd.to_datetime(end_date))
        ]
else:
    st.warning("No valid 'Date' column or no data after filtering.")
    st.stop()

# -- METRIC EXPLANATIONS TOOLTIP BOX --
with st.expander("💡 Metric Explanations"):
    st.markdown("""
    **period_start/period_end**: Start and end dates for analysis window  
    **period_days**: Number of analyzed dates per ticker  
    **avg_close**: Average close price across window  
    **avg_daily_return**: Average daily % return  
    **total_return**: Overall percent change from first to last day in window  
    **volatility_21**: Average 21-day rolling volatility (windowed std), annualized  
    **avg_rolling_yield_21**: Mean 21-day rolling average daily yield  
    **avg_sharpe_21**: Mean 21-day rolling Sharpe ratio (risk-adjusted yield)  
    **avg_max_drawdown_63**: Mean 63-day max drawdown  
    **avg_custom_risk_score**: Mean weighted risk score (see above)  
    """)

st.caption("📊 All metrics below are aggregated per ticker for your selected period.")

if filtered_df.empty:
    st.warning("No data matches selected stocks/dates. Try selecting more stocks or changing the date range.")
    st.stop()

# ----------- PORTFOLIO-LEVEL AGGREGATED ANALYTICS ----------- #
if filtered_df['symbol'].nunique() > 1:
    close_pivot = (
        filtered_df.pivot(index="Date", columns="symbol", values="Close")
        .sort_index()
        .ffill()
        .dropna(axis=0, how='any')  # Only keep dates where data for all symbols available
    )
    if close_pivot.shape[0] > 1:
        returns = close_pivot.pct_change().dropna(how='any')
        port_daily = returns.mean(axis=1)
        port_total_return = (close_pivot.iloc[-1].mean() / close_pivot.iloc[0].mean()) - 1
        port_annualized_return = port_daily.mean() * 252
        port_annualized_vol = port_daily.std() * np.sqrt(252)
        port_sharpe = port_annualized_return / port_annualized_vol if port_annualized_vol != 0 else np.nan
        port_max_drawdown = ((port_daily.cumsum() + 1).cummax() - (port_daily.cumsum() + 1)).max()
        port_period = f"{close_pivot.index[0].date()} – {close_pivot.index[-1].date()}"

        st.markdown("### Portfolio-level Analytics (Equal-Weighted)")
        st.write({
            "Period": port_period,
            "Total return": f"{port_total_return:.2%}",
            "Annualized return": f"{port_annualized_return:.2%}",
            "Annualized volatility": f"{port_annualized_vol:.2%}",
            "Sharpe ratio": f"{port_sharpe:.2f}",
            "Max drawdown": f"{port_max_drawdown:.2%}"
        })

        st.line_chart((port_daily.cumsum() + 1), use_container_width=True)
    else:
        st.info("Not enough overlapping data to compute portfolio analytics.")
else:
    st.info("Select at least two stocks to see portfolio-level analytics.")

# ----------- SUMMARY: AGGREGATED BY TICKER ----------- #
summary = (
    filtered_df
    .groupby("symbol")
    .agg(
        period_start = ("Date", "min"),
        period_end = ("Date", "max"),
        period_days = ("Date", "count"),
        avg_close = ("Close", "mean"),
        avg_daily_return = ("daily_return", "mean"),
        total_return = ("Close", lambda x: (x.iloc[-1] / x.iloc[0]) - 1 if len(x) > 1 and x.iloc[0] != 0 else np.nan),
        volatility_21 = ("volatility_21", "mean"),
        avg_rolling_yield_21 = ("rolling_yield_21", "mean"),
        avg
