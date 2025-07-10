# BullBoard

Phase 0: Project Foundations (Now)
 Create GitHub repository and README
 Set up a clear folder structure (etl.py, app.py, requirements.txt, data/)
 Create ROADMAP.md and basic “Contributing” docs
 Create public “Ideas/Features/Requests” discussion thread or GitHub Project board
 
Phase 1: MVP – Alpha Release
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

 PORTFOLIO-LEVEL AGGREGATED ANALYTICS
Most tools show scores/stats for individual tickers, but the majority of serious investors want to know:
- “How would a basket (my watchlist or portfolio) have performed—risk, yield, drawdown—if I’d held it over that timeframe?”
- Even the free version of Yahoo/TradingView etc. doesn’t make this easy.
- It creates a “wow!” moment for your users—and lays groundwork for backtesting, comparison, and eventual pro features.

Add a Multi-Level Data Validation Panel + Analytics Health Report
- Most apps don’t clearly tell users if their latest analytics are “stale,” have gaps, or have anomalies.
- By including a compact “Health & Validity” panel, you instantly boost user trust (“No missing data, all tickers up-to-date!”) and make troubleshooting easier for yourself.
- Data freshness: When was the ETL last run? Any tickers/rows missing recent data?
- Ticker completeness: Are all selected tickers covered for the whole period?
- Missing/NaN values: Any metrics/columns have missing values after the ETL or user’s filtering?
- Warnings: e.g., “Warning: GOOGL missing data for last 5 days”, “No rows for META in this date range”, etc.
- Visually, includes green ticks ✅ and yellow/orange exclamation signs ⚠️ for user clarity.

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

RANDOM THOUGHTS FOR FUTURE:
Možnost konfigurace custom investiční strategie a její následná implementace do aplikace, user definuje pouze časové rozmezí a vybere akcie, plugin mu vypočítá parametry investiční strategie aplikované na dané stocks v definovaném timeframu.
