import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("StoxPlanner: Stock Risk/Yield Dashboard")

# Button to run ETL pipeline
if st.button("Run ETL Pipeline Now"):
    with st.spinner("Running ETL pipeline, please wait..."):
        import etl
        etl.main()
    st.success("ETL Pipeline complete! Reloading data...")

# Try to load resulting CSV
try:
    df = pd.read_csv("latest_results.csv", parse_dates=["Date"])
    st.write(f"**Last analysis for {df['symbol'].nunique()} stocks.**")

    # Display score table
    st.subheader("Summary Table")
    st.dataframe(df)

    # Show Top N
    N = st.number_input("Show top N stocks by risk/yield:", 1, 30, 10)
    st.write("**Top by risk score:**")
    st.dataframe(df.sort_values("custom_risk_score", ascending=False).head(N)[["symbol", "custom_risk_score", "rolling_yield_21"]])

    st.write("**Top by rolling yield:**")
    st.dataframe(df.sort_values("rolling_yield_21", ascending=False).head(N)[["symbol", "rolling_yield_21", "custom_risk_score"]])

    # Select stocks for visualization
    st.subheader("Visualize Price Timeline")
    symbols = df['symbol'].tolist()
    selected = st.multiselect("Select stocks to plot", symbols, default=symbols[:min(3, len(symbols))])
    if selected:
        data_full = pd.read_csv("latest_results.csv")
        for symbol in selected:
            # You will likely want to load price history from a separate CSV (not just the summary)
            # Here we only plot points from the summary table.
            # For a true line plot with time, you can save the entire time series to a CSV during ETL.
            st.write(f"**{symbol} Analytic Snapshot**")
            filtered = df[df['symbol'] == symbol]
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

st.info("Tip: You can update the code in GitHub and Streamlit Cloud will auto-refresh this app.")
