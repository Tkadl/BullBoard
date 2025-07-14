import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime
TRANSFORMERS_AVAILABLE = False
pipeline = None

# Page configuration
st.set_page_config(
    page_title="BullBoard - Advanced Stock Analytics",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Custom CSS for modern styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main > div {
        padding-top: 2rem;
    }
    
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-change {
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }
    
    .positive { color: #2ecc71; }
    .negative { color: #e74c3c; }
    
    /* Status Cards */
    .status-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    
    .status-success {
        background: #d5f4e6;
        border-color: #2ecc71;
        color: #27ae60;
    }
    
    .status-warning {
        background: #fef9e7;
        border-color: #f39c12;
        color: #e67e22;
    }
    
    .status-info {
        background: #ebf3fd;
        border-color: #3498db;
        color: #2980b9;
    }
    
    /* AI Insight Cards */
    .ai-insight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #ffd700;
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ecf0f1;
    }
    
    .section-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def create_header():
    """Create the main header section"""
    st.markdown("""
    <div class="main-header">
        <h1>🐂 BullBoard</h1>
        <p>Advanced Stock Risk & Yield Analytics Platform with AI Insights</p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(label, value, change=None, change_type="neutral"):
    """Create a styled metric card"""
    change_class = "positive" if change_type == "positive" else "negative" if change_type == "negative" else ""
    change_symbol = "↗" if change_type == "positive" else "↘" if change_type == "negative" else ""
    
    change_html = f'<p class="metric-change {change_class}">{change_symbol} {change}</p>' if change else ""
    
    return f"""
    <div class="metric-card">
        <p class="metric-label">{label}</p>
        <p class="metric-value">{value}</p>
        {change_html}
    </div>
    """

def generate_advanced_insights(symbol, data, market_context=None):
    """Generate sophisticated rule-based insights that rival AI analysis"""
    insights = []
    
    # Extract key metrics
    risk_score = data.get('avg_custom_risk_score', 0)
    total_return = data.get('total_return', 0)
    sharpe_ratio = data.get('avg_sharpe_21', 0)
    volatility = data.get('volatility_21', 0)
    avg_return = data.get('avg_rolling_yield_21', 0)
    
    # 1. MOMENTUM ANALYSIS
    if total_return > 0.20:
        momentum_strength = "Strong" if total_return > 0.30 else "Moderate"
        insights.append(f"🚀 **Momentum Alert**: {symbol} shows {momentum_strength.lower()} bullish momentum with {total_return:.1%} returns")
    elif total_return < -0.15:
        insights.append(f"📉 **Risk Warning**: {symbol} showing bearish trend with {total_return:.1%} decline - monitor closely")
    
    # 2. RISK-ADJUSTED PERFORMANCE ANALYSIS
    if sharpe_ratio > 1.5 and total_return > 0.10:
        insights.append(f"💎 **Alpha Generator**: {symbol} delivers exceptional risk-adjusted returns (Sharpe: {sharpe_ratio:.2f}) - potential portfolio cornerstone")
    elif sharpe_ratio > 1.0:
        insights.append(f"⭐ **Quality Pick**: {symbol} shows solid risk-adjusted performance - good addition to diversified portfolio")
    elif sharpe_ratio < 0.3:
        insights.append(f"⚠️ **Efficiency Warning**: {symbol} poor risk-adjusted returns - consider alternatives or position sizing")
    
    # 3. VOLATILITY REGIME ANALYSIS
    if volatility < 0.02 and total_return > 0.05:
        insights.append(f"🛡️ **Low-Vol Winner**: {symbol} rare combination of low volatility ({volatility:.1%}) with positive returns - ideal for conservative portfolios")
    elif volatility > 0.08:
        vol_category = "Extremely High" if volatility > 0.12 else "High"
        if total_return > volatility * 2:  # Return compensates for risk
            insights.append(f"⚡ **High-Risk Reward**: {symbol} {vol_category.lower()} volatility but returns justify the risk")
        else:
            insights.append(f"🔥 **Volatility Alert**: {symbol} {vol_category.lower()} volatility ({volatility:.1%}) - suitable only for risk-tolerant investors")
    
    # 4. MARKET POSITIONING ANALYSIS
    risk_percentile = get_risk_percentile(risk_score)
    return_percentile = get_return_percentile(total_return)
    
    if risk_percentile < 25 and return_percentile > 75:
        insights.append(f"🏆 **Market Outperformer**: {symbol} in top quartile for returns while maintaining low risk profile")
    elif risk_percentile > 75 and return_percentile < 25:
        insights.append(f"💔 **Underperformer**: {symbol} high risk with poor returns - consider exit strategy")
    
    # 5. TREND STRENGTH ANALYSIS
    if avg_return > 0.001:  # Positive daily average
        annualized_projection = avg_return * 252
        if annualized_projection > 0.15:
            insights.append(f"📈 **Trend Strength**: {symbol} consistent daily gains averaging {avg_return:.3%} - projects to {annualized_projection:.1%} annually")
    
    # 6. PORTFOLIO ROLE RECOMMENDATION
    if risk_score < 0.04 and total_return > 0.08:
        insights.append(f"🎯 **Portfolio Core**: {symbol} ideal for portfolio foundation - low risk with steady returns")
    elif risk_score > 0.10 and sharpe_ratio > 1.2:
        insights.append(f"🎲 **Satellite Position**: {symbol} suitable for 5-10% portfolio allocation - high risk but compensated returns")
    elif volatility < 0.03:
        insights.append(f"⚖️ **Stability Anchor**: {symbol} can provide portfolio stability during market turbulence")
    
    return insights

def get_risk_percentile(risk_score):
    """Calculate risk percentile (mock function - you can enhance this)"""
    # Simple percentile calculation - you can make this more sophisticated
    if risk_score < 0.04:
        return 25
    elif risk_score < 0.07:
        return 50
    elif risk_score < 0.10:
        return 75
    else:
        return 90

def get_return_percentile(total_return):
    """Calculate return percentile (mock function - you can enhance this)"""
    if total_return > 0.20:
        return 90
    elif total_return > 0.10:
        return 75
    elif total_return > 0.05:
        return 50
    elif total_return > 0:
        return 25
    else:
        return 10

def generate_market_regime_insights(summary_data):
    """Detect market regime based on portfolio data"""
    insights = []
    
    avg_returns = summary_data['total_return'].mean()
    avg_volatility = summary_data['volatility_21'].mean()
    positive_stocks = (summary_data['total_return'] > 0).sum()
    total_stocks = len(summary_data)
    
    # Market regime detection
    if positive_stocks / total_stocks > 0.7 and avg_returns > 0.10:
        insights.append("🔥 **Bull Market Detected**: 70%+ of stocks showing positive returns - favorable environment for growth strategies")
    elif positive_stocks / total_stocks < 0.4:
        insights.append("🐻 **Bear Market Conditions**: Majority of stocks declining - focus on defensive positions and risk management")
    elif avg_volatility > 0.08:
        insights.append("🌪️ **High Volatility Regime**: Elevated market uncertainty - consider reducing position sizes")
    else:
        insights.append("⚖️ **Balanced Market**: Mixed signals suggest neutral stance with selective opportunities")
    
    return insights

def generate_portfolio_optimization_tips(summary_data):
    """Generate portfolio construction insights"""
    insights = []
    
    # Find best Sharpe ratios
    top_sharpe = summary_data.nlargest(3, 'avg_sharpe_21')
    low_correlation_candidates = summary_data[summary_data['volatility_21'] < summary_data['volatility_21'].median()]
    
    insights.append(f"🎯 **Optimization Tip**: Consider overweighting {', '.join(top_sharpe['symbol'].tolist())} for risk-adjusted returns")
    
    if len(low_correlation_candidates) > 0:
        insights.append(f"🔄 **Diversification Opportunity**: {', '.join(low_correlation_candidates['symbol'].head(3).tolist())} offer portfolio stabilization")
    
    # Risk parity suggestion
    high_risk_stocks = summary_data[summary_data['avg_custom_risk_score'] > summary_data['avg_custom_risk_score'].quantile(0.75)]
    if len(high_risk_stocks) > 0:
        insights.append(f"⚖️ **Risk Management**: Limit exposure to {', '.join(high_risk_stocks['symbol'].tolist())} or reduce position sizes")
    
    return insights

def create_risk_return_scatter(summary):
    """Create interactive risk vs return scatter plot"""
    fig = px.scatter(
        summary, 
        x='avg_custom_risk_score', 
        y='avg_rolling_yield_21',
        size='avg_close',
        color='avg_sharpe_21',
        hover_name='symbol',
        color_continuous_scale='RdYlGn',
        title="Risk vs Return Analysis",
        size_max=20
    )
    
    fig.update_layout(
        title={
            'text': "Risk vs Return Analysis",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Inter'}
        },
        xaxis_title="Risk Score",
        yaxis_title="Expected Return",
        font=dict(family="Inter", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    fig.update_xaxes(gridcolor='lightgray', gridwidth=0.5)
    fig.update_yaxes(gridcolor='lightgray', gridwidth=0.5)
    
    return fig

def create_performance_chart(filtered_df, selected_symbols):
    """Create normalized performance comparison chart"""
    if len(selected_symbols) == 0:
        return None
    
    # Calculate normalized performance
    perf_data = []
    for symbol in selected_symbols:
        symbol_data = filtered_df[filtered_df['symbol'] == symbol].sort_values('Date')
        if not symbol_data.empty:
            symbol_data = symbol_data.copy()
            symbol_data['normalized'] = symbol_data['Close'] / symbol_data['Close'].iloc[0] * 100
            perf_data.append(symbol_data[['Date', 'normalized', 'symbol']])
    
    if not perf_data:
        return None
    
    combined_data = pd.concat(perf_data)
    
    fig = px.line(
        combined_data,
        x='Date',
        y='normalized',
        color='symbol',
        title="Normalized Performance Comparison (Base 100)",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    
    fig.update_layout(
        title={
            'text': "Normalized Performance Comparison (Base 100)",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Inter'}
        },
        xaxis_title="Date",
        yaxis_title="Normalized Price",
        font=dict(family="Inter", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        hovermode='x unified'
    )
    
    fig.update_xaxes(gridcolor='lightgray', gridwidth=0.5)
    fig.update_yaxes(gridcolor='lightgray', gridwidth=0.5)
    
    return fig

def create_portfolio_metrics_chart(summary):
    """Create portfolio metrics comparison chart"""
    metrics = ['volatility_21', 'avg_rolling_yield_21', 'avg_sharpe_21']
    metric_names = ['Volatility', 'Expected Return', 'Sharpe Ratio']
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=metric_names,
        specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
    )
    
    colors = ['#e74c3c', '#2ecc71', '#3498db']
    
    for i, (metric, name, color) in enumerate(zip(metrics, metric_names, colors)):
        top_5 = summary.nlargest(5, metric)
        
        fig.add_trace(
            go.Bar(
                x=top_5['symbol'],
                y=top_5[metric],
                name=name,
                marker_color=color,
                showlegend=False
            ),
            row=1, col=i+1
        )
    
    fig.update_layout(
        title={
            'text': "Top 5 Stocks by Key Metrics",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Inter'}
        },
        font=dict(family="Inter", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig

def create_correlation_heatmap(filtered_df, selected_symbols):
    """Create correlation heatmap for selected stocks"""
    if len(selected_symbols) < 2:
        return None
    
    # Pivot data to get returns for each stock
    pivot_data = filtered_df.pivot(index='Date', columns='symbol', values='daily_return')
    pivot_data = pivot_data[selected_symbols].dropna()
    
    if pivot_data.empty:
        return None
    
    correlation_matrix = pivot_data.corr()
    
    fig = px.imshow(
        correlation_matrix,
        title="Stock Correlation Matrix",
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    
    fig.update_layout(
        title={
            'text': "Stock Correlation Matrix",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Inter'}
        },
        font=dict(family="Inter", size=12),
        height=500
    )
    
    return fig

def main():
    create_header()
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown("### 🎛️ Controls")
        
        # ETL Pipeline Button
        if st.button("🔄 Refresh Data", key="etl_button"):
            with st.spinner("Fetching latest market data..."):
                import etl
                etl.main()
            st.success("Data updated successfully!")
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Analysis Settings")
        
        st.success("🧠 Advanced Rule-Based Analytics Active")
        st.info("💡 Sophisticated insights without AI dependencies")
    
    # Load and validate data
    try:
        df = pd.read_csv("latest_results.csv", parse_dates=["Date"])
    except Exception as e:
        st.error("Failed to load data. Please refresh the data first.")
        st.stop()
    
    if df.empty or 'symbol' not in df.columns:
        st.error("No valid data found. Please refresh the data.")
        st.stop()
    
    # Data info section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card(
            "Stocks Analyzed", 
            str(df['symbol'].nunique()),
            "Active", 
            "positive"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "Data Points", 
            f"{len(df):,}",
            "Records", 
            "neutral"
        ), unsafe_allow_html=True)
    
    with col3:
        if 'download_time' in df.columns:
            last_update = df['download_time'].iloc[0]
            st.markdown(create_metric_card(
                "Last Update", 
                last_update.split()[1] if ' ' in str(last_update) else "Today"
            ), unsafe_allow_html=True)
        else:
            st.markdown(create_metric_card("Last Update", "Unknown"), unsafe_allow_html=True)
    
    with col4:
        date_range = df['Date'].max() - df['Date'].min()
        st.markdown(create_metric_card(
            "Date Range", 
            f"{date_range.days} days"
        ), unsafe_allow_html=True)
    
    # Stock Selection
    st.markdown('<div class="section-header"><span class="section-icon">🎯</span><h2>Stock Selection</h2></div>', unsafe_allow_html=True)
    
    unique_symbols = sorted(df['symbol'].unique())
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_symbols = st.multiselect(
            "Choose stocks to analyze",
            unique_symbols,
            default=unique_symbols[:8] if len(unique_symbols) >= 8 else unique_symbols,
            help="Select stocks for detailed analysis and comparison"
        )
    
    with col2:
        if st.button("📈 Select All", key="select_all"):
            selected_symbols = unique_symbols
            st.rerun()
    
    # Filter data based on selection
    filtered_df = df[df['symbol'].isin(selected_symbols)] if selected_symbols else df
    
    # Date Range Selection
    if not filtered_df.empty:
        min_date = filtered_df['Date'].min().date()
        max_date = filtered_df['Date'].max().date()
        
        date_range = st.date_input(
            "Select analysis period",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df['Date'] >= pd.to_datetime(start_date)) &
                (filtered_df['Date'] <= pd.to_datetime(end_date))
            ]
    
    if filtered_df.empty:
        st.warning("No data available for selected stocks and date range.")
        st.stop()
    
    # Generate summary statistics
    summary = (
        filtered_df
        .groupby("symbol")
        .agg(
            period_start=("Date", "min"),
            period_end=("Date", "max"),
            period_days=("Date", "count"),
            avg_close=("Close", "mean"),
            avg_daily_return=("daily_return", "mean"),
            total_return=("Close", lambda x: (x.iloc[-1] / x.iloc[0]) - 1 if len(x) > 1 and x.iloc[0] != 0 else np.nan),
            volatility_21=("volatility_21", "mean"),
            avg_rolling_yield_21=("rolling_yield_21", "mean"),
            avg_sharpe_21=("sharpe_21", "mean"),
            avg_max_drawdown_63=("max_drawdown_63", "mean"),
            avg_custom_risk_score=("custom_risk_score", "mean"),
        )
        .reset_index()
    )
    
    # Portfolio Overview
    if len(selected_symbols) > 1:
        st.markdown('<div class="section-header"><span class="section-icon">💼</span><h2>Portfolio Overview</h2></div>', unsafe_allow_html=True)
        
        # Portfolio metrics
        portfolio_return = summary['total_return'].mean()
        portfolio_risk = summary['avg_custom_risk_score'].mean()
        best_performer = summary.loc[summary['total_return'].idxmax(), 'symbol']
        worst_performer = summary.loc[summary['total_return'].idxmin(), 'symbol']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card(
                "Portfolio Return",
                f"{portfolio_return:.2%}",
                f"{portfolio_return:.2%}",
                "positive" if portfolio_return > 0 else "negative"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                "Average Risk Score",
                f"{portfolio_risk:.3f}",
                "Risk Level",
                "neutral"
            ), unsafe_allow_html=True)
        
        with col3:
            best_return = summary.loc[summary['symbol'] == best_performer, 'total_return'].iloc[0]
            st.markdown(create_metric_card(
                "Best Performer",
                best_performer,
                f"{best_return:.2%}",
                "positive"
            ), unsafe_allow_html=True)
        
        with col4:
            worst_return = summary.loc[summary['symbol'] == worst_performer, 'total_return'].iloc[0]
            st.markdown(create_metric_card(
                "Worst Performer",
                worst_performer,
                f"{worst_return:.2%}",
                "negative"
            ), unsafe_allow_html=True)
    
# Advanced Analytics Section
    st.markdown('<div class="section-header"><span class="section-icon">🧠</span><h2>Advanced Market Intelligence</h2></div>', unsafe_allow_html=True)
    
    if not summary.empty:
        # Market regime analysis
        market_insights = generate_market_regime_insights(summary)
        if market_insights:
            st.subheader("📊 Market Regime Analysis")
            for insight in market_insights:
                st.info(insight)
        
        # Portfolio optimization tips
        portfolio_tips = generate_portfolio_optimization_tips(summary)
        if portfolio_tips:
            st.subheader("🎯 Portfolio Optimization")
            for tip in portfolio_tips:
                st.success(tip)
        
        st.markdown("---")
        
        # Individual stock analysis for top performers
        st.subheader("🔍 Individual Stock Analysis")
        top_stocks = summary.nlargest(5, 'total_return')
        
        for _, row in top_stocks.iterrows():
            # Get advanced insights
            advanced_insights = generate_advanced_insights(row['symbol'], row)
            
            if advanced_insights:
                with st.expander(f"📊 {row['symbol']} - Advanced Analysis"):
                    for insight in advanced_insights:
                        st.markdown(insight)
    # Interactive Charts Section
    st.markdown('<div class="section-header"><span class="section-icon">📊</span><h2>Interactive Analytics</h2></div>', unsafe_allow_html=True)
    
    # Risk vs Return Scatter Plot
    if not summary.empty:
        fig = create_risk_return_scatter(summary)
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance Comparison Chart
    if selected_symbols:
        perf_fig = create_performance_chart(filtered_df, selected_symbols)
        if perf_fig:
            st.plotly_chart(perf_fig, use_container_width=True)
    
    # Metrics Comparison Chart
    if not summary.empty:
        metrics_fig = create_portfolio_metrics_chart(summary)
        st.plotly_chart(metrics_fig, use_container_width=True)
    
    # Correlation Heatmap
    if len(selected_symbols) > 1:
        corr_fig = create_correlation_heatmap(filtered_df, selected_symbols)
        if corr_fig:
            st.plotly_chart(corr_fig, use_container_width=True)
    
    # Data Table Section
    st.markdown('<div class="section-header"><span class="section-icon">📋</span><h2>Detailed Analysis</h2></div>', unsafe_allow_html=True)
    
    # Summary table with better formatting
    if not summary.empty:
        # Format the summary table for better display
        display_summary = summary.copy()
        display_summary['total_return'] = display_summary['total_return'].apply(lambda x: f"{x:.2%}" if pd.notna(x) else "N/A")
        display_summary['avg_daily_return'] = display_summary['avg_daily_return'].apply(lambda x: f"{x:.4%}" if pd.notna(x) else "N/A")
        display_summary['avg_rolling_yield_21'] = display_summary['avg_rolling_yield_21'].apply(lambda x: f"{x:.4%}" if pd.notna(x) else "N/A")
        display_summary['volatility_21'] = display_summary['volatility_21'].apply(lambda x: f"{x:.4f}" if pd.notna(x) else "N/A")
        display_summary['avg_sharpe_21'] = display_summary['avg_sharpe_21'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")
        display_summary['avg_custom_risk_score'] = display_summary['avg_custom_risk_score'].apply(lambda x: f"{x:.4f}" if pd.notna(x) else "N/A")
        display_summary['avg_close'] = display_summary['avg_close'].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "N/A")
        
        st.dataframe(
            display_summary,
            use_container_width=True,
            column_config={
                "symbol": "Stock",
                "total_return": "Total Return",
                "avg_daily_return": "Avg Daily Return",
                "avg_close": "Avg Price",
                "volatility_21": "Volatility",
                "avg_sharpe_21": "Sharpe Ratio",
                "avg_custom_risk_score": "Risk Score"
            }
        )
    
    # Top performers section
    if not summary.empty and len(summary) > 5:
        st.markdown("### 🏆 Top Performers")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🚀 Highest Returns**")
            top_returns = summary.nlargest(5, 'total_return')[['symbol', 'total_return']]
            for _, row in top_returns.iterrows():
                st.markdown(f"• **{row['symbol']}**: {row['total_return']:.2%}")
        
        with col2:
            st.markdown("**⚡ Best Risk-Adjusted Returns**")
            top_sharpe = summary.nlargest(5, 'avg_sharpe_21')[['symbol', 'avg_sharpe_21']]
            for _, row in top_sharpe.iterrows():
                st.markdown(f"• **{row['symbol']}**: {row['avg_sharpe_21']:.2f}")

if __name__ == "__main__":
    main()
