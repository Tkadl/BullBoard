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
    st.experimental_rerun()

# Try to load resulting CSV
try:
    df = pd.read_csv("latest_results.csv", parse_dates=["Date"])
    st.write(f"**Last analysis for {df['symbol'].nunique()} stocks.**")

    # --- Ticker Dropdown for Filtering ---
    if 'symbol' in df.columns:
        unique_syms = sorted(df['symbol'].unique())
        selected_syms = st.multiselect(
            "Select stocks for analysis",
            unique_syms,
            default=unique_syms[:5]
        )
        filtered_df = df[df['symbol'].isin(selected_syms)]
    else:
        filtered_df = df  # fallback

    # --- Date Range Picker ---
    if 'Date' in filtered_df.columns:
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

    # -- METRIC EXPLANATIONS TOOLTIP BOX --
    with st.expander("💡 Metric Explanations"):
        st.markdown("""
        **custom_risk_score**: Composite risk (0.7×21d volatility + 0.3×63d drawdown), higher is riskier  
        **rolling_yield_21**: 21-day rolling mean of daily returns — recent 'drift' (positive, negative, or flat)  
        **sharpe_21**: Risk-adjusted annualized return over 21 days (higher = better)  
        **volatility_21**: "Wiggliness" — std deviation of daily return, 21-day window  
        **max_drawdown_63**: Largest price drop from peak over the last 63 days  
        """)

    st.caption("📊 Click column headers to sort, or use the search box (upper right of table) to filter.")

    # Display score table (sorting/filtering work out-of-the-box in st.dataframe!)
    st.subheader("Summary Table")
    st.dataframe(
        filtered_df,
        help="Table is interactive! Click headers to sort. Use search to find stocks."
    )

    # Show Top N - (this is still sorted result slices, not interactive filter, but it's useful)
    N = st.number_input("Show top N stocks by risk/yield:", 1, min(30, len(filtered_df)), min(10, len(filtered_df)))
    st.write("**Top by risk score:**")
    st.dataframe(filtered_df.sort_values("custom_risk_score", ascending=False).head(N)
                 [["symbol", "custom_risk_score", "rolling_yield_21"]])

    st.write("**Top by rolling yield:**")
    st.dataframe(filtered_df.sort_values("rolling_yield_21", ascending=False).head(N)
                 [["symbol", "rolling_yield_21", "custom_risk_score"]])

    # Select stocks for visualization
    st.subheader("Visualize Price Timeline")
    symbols = filtered_df['symbol'].tolist()
    selected = st.multiselect("Select stocks to plot", symbols, default=symbols[:min(3, len(symbols))])
    if selected:
        for symbol in selected:
            st.write(f"**{symbol} Analytic Snapshot**")
            filtered = filtered_df[filtered_df['symbol'] == symbol]
            if not filtered.empty:
                fig, ax = plt.subplots(figsize=(8, 3))
                ax.bar(["Risk", "Yield", "Sharpe"], [
                    filtered["custom_risk_score"].values[0],
                    filtered["rolling_yield_21"].values[0],
                    filtered["sharpe_21"].values[0]
                ])
                ax.set_title(f"{symbol} (Risk/Yield/Sharpe)")
                st.pyplot(fig)

except Exception as e:
    st.warning("No results file found. Please run the ETL pipeline first.")
