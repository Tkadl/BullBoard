import streamlit as st
import pandas as pd

st.title("Stock Analytics Dashboard")

# Optional: Button to trigger ETL pipeline
if st.button("Run ETL Pipeline"):
    import etl
    etl.main()  # assuming your etl.py has a main() function

# Optional: Load precomputed results
# df = pd.read_csv("your_output.csv")
# st.dataframe(df)
