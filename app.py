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

# ----------- HEALTH REPORT PANEL ----------- #
def health_report_panel(filtered_df, summary, selected_syms, min_date, max_date):
    st.markdown("## 🩺 Data Health & Analytics Validity")
    problems = []
    with st.container():
        # 1. ETL Download Time(s)
        if "download_time" in filtered_df.columns:
            last_dl = filtered_df["download_time"].max()
            st.write(f"**ETL Last Run:** {last_dl}")
        else:
            st.write("**ETL last run time not available.**")

        # 2. Ticker coverage check
        missing_syms = [s for s in selected_syms if s not in filtered_df['symbol'].unique()]
        if missing_syms:
            st.warning(f"⚠️ No data for: {', '.join(missing_syms)}")
            problems.append("Missing tickers")
        else:
            st.success("✅ All selected tickers present in data.")

        # 3. Date coverage check
        health_msgs = []
        for sx in selected_syms:
            symbol_dates = filtered_df[filtered_df['symbol'] == sx]['Date']
            if not symbol_dates.empty:
                start, end = symbol_dates.min(), symbol_dates.max()
                cov_warn = ""
                # Allow 1 day slippage (e.g. market holidays)
                if (min_date is not None and (start > min_date + pd.Timedelta(days=1))) or \
                   (max_date is not None and (end < max_date - pd.Timedelta(days=1))):
                    cov_warn = "Incomplete"
                if cov_warn:
                    health_msgs.append(f"⚠️ {sx} data from {start.date()} to {end.date()}")
            else:
                health_msgs.append(f"⚠️ {sx} has no data in this window.")
        if not health_msgs:
            st.success("✅ All symbols have full date coverage.")
        else:
            for msg in health_msgs:
                st.info(msg)
            problems.append("Incomplete date coverage")

        # 4. NaN/empty columns
        if summary is not None and not summary.empty:
            missing_cols = summary.isnull().any()
            nan_cols = missing_cols[missing_cols].index.tolist()
            if nan_cols:
                st.warning(f"⚠️ Columns with missing values: {', '.join(nan_cols)}")
                problems.append("NaNs in summary stats")
            else:
                st.success("✅ No missing values in summary table.")

        # 5. No filtered data at all
        if filtered_df.empty:
            st.error("❌ No data after filtering. Check your selection or ETL.")

        # Extra tip for hygiene!
        if not problems:
            st.info("✔️ No issues detected. Your analytics passed all health checks!")

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
        avg_sharpe_21 = ("sharpe_21", "mean"),
        avg_max_drawdown_63 = ("max_drawdown_63", "mean"),
        avg_custom_risk_score = ("custom_risk_score", "mean"),
    )
    .reset_index()
)

# ----------- HEALTH PANEL ----------- #
health_report_panel(
    filtered_df, summary, selected_syms,
    min_date=min_date if 'min_date' in locals() else None,
    max_date=max_date if 'max_date' in locals() else None
)

# ----------- PORTFOLIO-LEVEL AGGREGATED ANALYTICS ----------- #
portfolio_returns = None
if filtered_df['symbol'].nunique() > 1:
    close_pivot = (
        filtered_df.pivot(index="Date", columns="symbol", values="Close")
        .sort_index()
        .ffill()
        .dropna(axis=0, how='any')
    )
    if close_pivot.shape[0] > 1:
        returns = close_pivot.pct_change().dropna(how='any')
        port_daily = returns.mean(axis=1)
        portfolio_returns = port_daily  # For potential future use
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
st.subheader("Summary Table (Aggregated per Ticker for Selected Period)")
st.dataframe(summary)

# Show Top N
if not summary.empty:
    N = st.number_input("Show top N stocks by risk/yield:",
                        min_value=1,
                        max_value=len(summary),
                        value=min(10, len(summary)))
    st.write("**Top by average risk score:**")
    st.dataframe(summary.sort_values("avg_custom_risk_score", ascending=False).head(N)
                 [["symbol", "avg_custom_risk_score", "avg_rolling_yield_21"]])

    st.write("**Top by average rolling yield:**")
    st.dataframe(summary.sort_values("avg_rolling_yield_21", ascending=False).head(N)
                 [["symbol", "avg_rolling_yield_21", "avg_custom_risk_score"]])

# Visualizations
st.subheader("Visualize Aggregate Metrics Timeline or Compare Across Tickers")
symbols = summary['symbol'].tolist()
selected = st.multiselect("Select stocks to plot", symbols, default=symbols[:min(3, len(symbols))])
if selected:
    st.write("**Side-by-side bar plot of risk/yield metrics (Averages over period):**")
    filtered = summary[summary['symbol'].isin(selected)]
    for metric, label in [
        ("avg_custom_risk_score", "Avg Risk"),
        ("avg_rolling_yield_21", "Avg Yield"),
        ("avg_sharpe_21", "Avg Sharpe"),
    ]:
        st.bar_chart(filtered.set_index("symbol")[[metric]].rename(columns={metric: label}))
