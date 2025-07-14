import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime

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
    
    /* Action Button */
    .action-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
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
    
    /* Portfolio Summary */
    .portfolio-summary {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    /* Risk Level Indicators */
    .risk-low { border-left-color: #2ecc71 !important; }
    .risk-medium { border-left-color: #f39c12 !important; }
    .risk-high { border-left-color: #e74c3c !important; }
    
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
        <p>Advanced Stock Risk & Yield Analytics Platform</p>
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

def create_status_card(message, status_type="info"):
    """Create a status card"""
    return f'<div class="status-card status-{status_type}">{message}</div>'

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

# Main App
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
            help
