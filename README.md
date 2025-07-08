# BullBoard

► Phase 0: Project Foundations (Now)
 Create GitHub repository and README
 Set up a clear folder structure (etl.py, app.py, requirements.txt, data/)
 Create ROADMAP.md and basic “Contributing” docs
 Create public “Ideas/Features/Requests” discussion thread or GitHub Project board
 
► Phase 1: MVP – Alpha Release
(Aim: End-to-end data flow, analysis, and dashboard for core user needs)

Data and ETL:
 Download daily stock price/volume for user-defined tickers, covering any time window
 Batch/bulk downloading for large ticker sets
 Handle missing days, delisted/missing tickers gracefully
Analytics:
 Calculate daily returns per stock
 Compute rolling window stats (by default, 21/63 days):
Volatility
Max drawdown
Sharpe ratio
Rolling mean return
Custom risk score
 Generate per-ticker summary (latest stats, daily updated)
Alerting and Ranking:
 Thresholding for custom alerts (yield, risk)
 Sort and rank stocks by yield, risk, or other analytics
Dashboard/UI:
 Interactive web interface (Streamlit) – basic table + rank view
 Filters by ticker, risk, yield
 Visualizations: line plots for prices, bar/rank plots for risk/yield
Project Hygiene:
 List all dependencies (requirements.txt)
 Clear README with “How to use/apply” and contribution guide
Deployment:
 Deploy on Streamlit Community Cloud
 Instructions for deploying/replicating
