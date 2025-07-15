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
    
    /* Enhanced Header Styling */
   .main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    padding: 2.5rem 2rem;
    border-radius: 20px;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="20" cy="80" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    pointer-events: none;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    position: relative;
    z-index: 1;
}

.logo-section {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.logo-icon {
    font-size: 3.5rem;
    filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
}

.logo-text h1 {
    margin: 0;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(45deg, #ffffff, #f8f9ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.tagline {
    font-size: 1.2rem;
    font-weight: 500;
    opacity: 0.95;
    margin-top: 0.25rem;
}

.value-props {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
}

.prop-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: transform 0.3s ease;
}

.prop-item:hover {
    transform: translateY(-3px);
    background: rgba(255, 255, 255, 0.2);
}

.prop-icon {
    font-size: 1.8rem;
}

.prop-text {
    font-size: 0.9rem;
    font-weight: 600;
    text-align: center;
    white-space: nowrap;
}

.header-subtitle {
    text-align: center;
    margin-top: 1.5rem;
    font-size: 1rem;
    opacity: 0.9;
    font-weight: 400;
    position: relative;
    z-index: 1;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
        gap: 1.5rem;
        text-align: center;
    }
    
    .value-props {
        justify-content: center;
        gap: 1rem;
    }
    
    .logo-text h1 {
        font-size: 2.5rem;
    }
    
    .tagline {
        font-size: 1rem;
    }
}
    
/* Metric Cards - Fixed height and text positioning */
.metric-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 50%, #ffffff 100%);
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 
        0 4px 6px -1px rgba(0, 0, 0, 0.1),
        0 2px 4px -1px rgba(0, 0, 0, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.6);
    height: 160px; /* Increased from 140px */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin: 8px 0;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 
        0 12px 25px rgba(102, 126, 234, 0.15),
        0 8px 10px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.6);
    border-color: rgba(102, 126, 234, 0.3);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 5px;
    height: 100%;
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    border-radius: 0 2px 2px 0;
}

.metric-card::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100px;
    height: 100px;
    background: radial-gradient(circle, rgba(102, 126, 234, 0.05) 0%, transparent 70%);
    border-radius: 50%;
}

.metric-header {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    position: relative;
    z-index: 1;
}

.metric-icon {
    font-size: 18px;
    margin-right: 10px;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.metric-title {
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #64748b !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    line-height: 1.2 !important;
}

.metric-value {
    font-size: 28px !important; /* Slightly smaller to make room */
    font-weight: 800 !important;
    color: #1e293b !important;
    margin: 8px 0 12px 0 !important; /* Added bottom margin */
    line-height: 1.1 !important;
    position: relative;
    z-index: 1;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.metric-subtitle {
    font-size: 13px !important; /* Slightly smaller but still readable */
    color: #667eea !important;
    font-weight: 600 !important;
    position: relative;
    z-index: 1;
    text-transform: capitalize;
    line-height: 1.2 !important;
    margin-bottom: 4px !important; /* Add bottom margin */
    display: block !important; /* Ensure it displays properly */
}

/* Section Headers - Keep existing styles */
.section-header {
    display: flex;
    align-items: center;
    margin: 2rem 0 1.5rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid #e2e8f0;
}

.section-icon {
    font-size: 1.5rem;
    margin-right: 0.75rem;
}

.section-header h2 {
    margin: 0 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1.5rem !important;
}

/* Fix for dark theme text visibility */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

.main .block-container {
    color: #ffffff;
}

/* Additional refinements */
.element-container {
    margin-bottom: 0 !important;
}

/* Responsive adjustments for cards */
@media (max-width: 768px) {
    .metric-card {
        height: 120px;
        padding: 16px;
    }
    
    .metric-value {
        font-size: 24px !important;
    }
    
    .metric-title {
        font-size: 10px !important;
    }
}

/* Section Headers - Fixed colors */
.section-header {
    display: flex;
    align-items: center;
    margin: 2rem 0 1.5rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid #e2e8f0;
}

.section-icon {
    font-size: 1.5rem;
    margin-right: 0.75rem;
}

.section-header h2 {
    margin: 0 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1.5rem !important;
}

/* Fix for dark theme text visibility */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

.main .block-container {
    color: #ffffff;
}
    
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
    """Create an enhanced, more appealing header section"""
    st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo-section">
                <span class="logo-icon">🐂</span>
                <div class="logo-text">
                    <h1>BullBoard</h1>
                    <div class="tagline">Professional Stock Analysis Made Simple</div>
                </div>
            </div>
            <div class="value-props">
                <div class="prop-item">
                    <span class="prop-icon">📊</span>
                    <span class="prop-text">Objective Data</span>
                </div>
                <div class="prop-item">
                    <span class="prop-icon">🎯</span>
                    <span class="prop-text">Clear Insights</span>
                </div>
                <div class="prop-item">
                    <span class="prop-icon">⚡</span>
                    <span class="prop-text">Real-time Analysis</span>
                </div>
            </div>
        </div>
        <div class="header-subtitle">
            Objective insights for informed decision-making • No advice, just facts
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, subtitle="", icon="📊"):
    """Create a metric card using Streamlit components with custom styling"""
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-icon">{icon}</span>
            <span class="metric-title">{title}</span>
        </div>
        <div class="metric-value">{value}</div>
        <div class="metric-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Return empty string to prevent "None" from appearing
    return ""
        
def calculate_comprehensive_risk_profile(symbol, data):
    """Calculate a comprehensive risk assessment"""
    risk_factors = {}
    
    # 1. Volatility Risk
    volatility = data.get('volatility_21', 0)
    if volatility > 0.08:
        risk_factors['volatility'] = {'level': 'High', 'score': 3, 'description': f'Significant price swings ({volatility:.1%} volatility)'}
    elif volatility > 0.05:
        risk_factors['volatility'] = {'level': 'Moderate', 'score': 2, 'description': f'Moderate price fluctuations ({volatility:.1%} volatility)'}
    else:
        risk_factors['volatility'] = {'level': 'Low', 'score': 1, 'description': f'Relatively stable price movements ({volatility:.1%} volatility)'}
    
    # 2. Drawdown Risk
    max_drawdown = data.get('avg_max_drawdown_63', 0)
    if max_drawdown > 0.20:
        risk_factors['drawdown'] = {'level': 'High', 'score': 3, 'description': f'Large peak-to-trough declines ({max_drawdown:.1%})'}
    elif max_drawdown > 0.10:
        risk_factors['drawdown'] = {'level': 'Moderate', 'score': 2, 'description': f'Moderate downside exposure ({max_drawdown:.1%})'}
    else:
        risk_factors['drawdown'] = {'level': 'Low', 'score': 1, 'description': f'Limited downside risk ({max_drawdown:.1%})'}
    
    # 3. Consistency Risk
    sharpe = data.get('avg_sharpe_21', 0)
    if sharpe < 0.5:
        risk_factors['consistency'] = {'level': 'High', 'score': 3, 'description': f'Inconsistent return patterns (Sharpe: {sharpe:.2f})'}
    elif sharpe < 1.0:
        risk_factors['consistency'] = {'level': 'Moderate', 'score': 2, 'description': f'Moderately consistent returns (Sharpe: {sharpe:.2f})'}
    else:
        risk_factors['consistency'] = {'level': 'Low', 'score': 1, 'description': f'Consistent return generation (Sharpe: {sharpe:.2f})'}
    
    return risk_factors

def analyze_performance_context(symbol, data, portfolio_context):
    """Analyze performance in context of market and peers"""
    insights = []
    
    total_return = data.get('total_return', 0)
    symbol_volatility = data.get('volatility_21', 0)
    
    # Market context
    market_avg = portfolio_context.get('avg_return', 0)
    market_volatility = portfolio_context.get('avg_volatility', 0.05)
    
    # Relative performance analysis
    relative_performance = total_return - market_avg
    if abs(relative_performance) > 0.05:  # 5% difference is significant
        direction = "outperformed" if relative_performance > 0 else "underperformed"
        insights.append(
            f"📊 **Relative Performance**: {symbol} {direction} your selection average by {abs(relative_performance):.1%}"
        )
    
    # Risk-adjusted comparison
    if symbol_volatility < market_volatility * 0.8 and total_return > market_avg:
        insights.append(
            f"🎯 **Risk Efficiency**: {symbol} achieved above-average returns ({total_return:.1%}) with below-average risk ({symbol_volatility:.1%})"
        )
    elif symbol_volatility > market_volatility * 1.2 and total_return < market_avg:
        insights.append(
            f"⚠️ **Risk-Return Mismatch**: {symbol} shows higher risk ({symbol_volatility:.1%}) than average but lower returns ({total_return:.1%})"
        )
    
    return insights

def detect_market_regime(portfolio_data):
    """Detect current market regime with confidence levels"""
    positive_stocks = (portfolio_data['total_return'] > 0).sum()
    total_stocks = len(portfolio_data)
    avg_volatility = portfolio_data['volatility_21'].mean()
    avg_return = portfolio_data['total_return'].mean()
    
    positive_ratio = positive_stocks / total_stocks
    
    if positive_ratio > 0.7 and avg_return > 0.1:
        return {
            'regime': 'Bull Market', 
            'confidence': 'High', 
            'description': f'{positive_ratio:.0%} of stocks positive with {avg_return:.1%} average return',
            'characteristics': 'Broad-based gains with strong momentum'
        }
    elif positive_ratio < 0.4 and avg_return < 0:
        return {
            'regime': 'Bear Market', 
            'confidence': 'High', 
            'description': f'{positive_ratio:.0%} of stocks positive with {avg_return:.1%} average return',
            'characteristics': 'Widespread declines across holdings'
        }
    elif avg_volatility > 0.08:
        return {
            'regime': 'High Volatility', 
            'confidence': 'Medium', 
            'description': f'Average volatility at {avg_volatility:.1%}',
            'characteristics': 'Elevated uncertainty and price swings'
        }
    else:
        return {
            'regime': 'Neutral Market', 
            'confidence': 'Medium', 
            'description': f'{positive_ratio:.0%} positive stocks, {avg_volatility:.1%} average volatility',
            'characteristics': 'Mixed signals with no clear directional bias'
        }

def calculate_quality_metrics(symbol, data):
    """Calculate objective quality metrics (0-100 scale)"""
    metrics = {}
    
    # Consistency Score (based on Sharpe ratio)
    sharpe = data.get('avg_sharpe_21', 0)
    consistency_score = min(100, max(0, (sharpe + 1) * 40))  # Normalize to 0-100
    
    # Efficiency Score (return per unit of risk)
    risk_score = data.get('avg_custom_risk_score', 0.01)
    total_return = data.get('total_return', 0)
    if risk_score > 0:
        efficiency_score = min(100, max(0, (total_return / risk_score) * 5))
    else:
        efficiency_score = 0
    
    # Growth Score (annualized return potential)
    avg_return = data.get('avg_rolling_yield_21', 0)
    annualized_return = avg_return * 252
    growth_score = min(100, max(0, (annualized_return + 0.1) * 200))  # Normalize
    
    # Overall score (weighted average)
    overall_score = (consistency_score * 0.4 + efficiency_score * 0.4 + growth_score * 0.2)
    
    return {
        'consistency': round(consistency_score, 1),
        'efficiency': round(efficiency_score, 1),
        'growth': round(growth_score, 1),
        'overall': round(overall_score, 1)
    }

def generate_comprehensive_analysis(symbol, data, portfolio_context):
    """Generate comprehensive, objective stock analysis - guaranteed insights"""
    insights = []
    
    # Get all analysis components
    risk_profile = calculate_comprehensive_risk_profile(symbol, data)
    performance_context = analyze_performance_context(symbol, data, portfolio_context)
    quality_metrics = calculate_quality_metrics(symbol, data)
    
    # Extract key metrics
    total_return = data.get('total_return', 0)
    volatility = data.get('volatility_21', 0)
    sharpe_ratio = data.get('avg_sharpe_21', 0)
    avg_return = data.get('avg_rolling_yield_21', 0)
    
    # 1. PERFORMANCE SUMMARY (Always included)
    if total_return > 0.20:
        insights.append(f"🚀 **Performance**: {symbol} generated strong {total_return:.1%} returns during the selected period")
    elif total_return > 0.05:
        insights.append(f"📈 **Performance**: {symbol} gained {total_return:.1%} over the analysis period")
    elif total_return > 0:
        insights.append(f"📊 **Performance**: {symbol} posted modest {total_return:.1%} returns")
    elif total_return > -0.10:
        insights.append(f"📉 **Performance**: {symbol} declined {abs(total_return):.1%} during the period")
    else:
        insights.append(f"📉 **Performance**: {symbol} experienced significant decline of {abs(total_return):.1%}")
    
    # 2. RISK ASSESSMENT (Always included)
    volatility_info = risk_profile['volatility']
    insights.append(f"📊 **Risk Profile**: {volatility_info['description']}")
    
    # 3. EFFICIENCY ANALYSIS (Always included)
    if sharpe_ratio > 1.2:
        insights.append(f"⭐ **Efficiency**: Excellent risk-adjusted performance with Sharpe ratio of {sharpe_ratio:.2f}")
    elif sharpe_ratio > 0.8:
        insights.append(f"✅ **Efficiency**: Good risk-adjusted performance with Sharpe ratio of {sharpe_ratio:.2f}")
    elif sharpe_ratio > 0.3:
        insights.append(f"📊 **Efficiency**: Moderate risk-adjusted performance with Sharpe ratio of {sharpe_ratio:.2f}")
    else:
        insights.append(f"⚠️ **Efficiency**: Below-average risk-adjusted performance with Sharpe ratio of {sharpe_ratio:.2f}")
    
    # 4. TREND ANALYSIS (Always included)
    if avg_return > 0.001:
        annualized_trend = avg_return * 252
        insights.append(f"📈 **Trend**: Daily average return of {avg_return:.3%} projects to {annualized_trend:.1%} annualized")
    elif avg_return < -0.001:
        annualized_trend = avg_return * 252
        insights.append(f"📉 **Trend**: Daily average decline of {abs(avg_return):.3%} projects to {abs(annualized_trend):.1%} annualized")
    else:
        insights.append(f"📊 **Trend**: Flat trend with minimal daily movement averaging {avg_return:.3%}")
    
    # 5. QUALITY METRICS (Always included)  
    if quality_metrics['overall'] > 70:
        insights.append(f"🏆 **Quality Score**: High rating of {quality_metrics['overall']}/100 across key metrics")
    elif quality_metrics['overall'] > 50:
        insights.append(f"📊 **Quality Score**: Moderate rating of {quality_metrics['overall']}/100 across key metrics")
    else:
        insights.append(f"📊 **Quality Score**: Below-average rating of {quality_metrics['overall']}/100 across key metrics")
    
    # 6. CONTEXT INSIGHTS (if available)
    insights.extend(performance_context)
    
    # 7. DRAWDOWN ANALYSIS (Always included)
    drawdown_info = risk_profile['drawdown']
    insights.append(f"📊 **Downside Risk**: {drawdown_info['description']}")
    
    # 8. FINAL FACTUAL SUMMARY (Always included)
    risk_category = "high-risk" if volatility > 0.08 else "moderate-risk" if volatility > 0.05 else "low-risk"
    return_category = "strong gains" if total_return > 0.15 else "moderate gains" if total_return > 0.05 else "modest gains" if total_return > 0 else "negative returns"
    
    insights.append(f"📋 **Profile**: {symbol} is a {risk_category} stock showing {return_category} over your selected timeframe")
    
    return insights

def generate_market_regime_insights(summary_data):
    """Generate market regime analysis"""
    regime = detect_market_regime(summary_data)
    insights = []
    
    insights.append(f"🌐 **Market Regime**: {regime['regime']} detected with {regime['confidence'].lower()} confidence")
    insights.append(f"📊 **Regime Details**: {regime['description']} - {regime['characteristics']}")
    
    # Regime-specific insights
    if regime['regime'] == 'Bull Market':
        insights.append("💡 **Market Context**: Favorable conditions for growth-oriented strategies")
    elif regime['regime'] == 'Bear Market':
        insights.append("💡 **Market Context**: Defensive positioning and risk management priority")
    elif regime['regime'] == 'High Volatility':
        insights.append("💡 **Market Context**: Consider reduced position sizes and increased monitoring")
    else:
        insights.append("💡 **Market Context**: Mixed environment suggests selective, balanced approach")
    
    return insights

def generate_portfolio_optimization_insights(summary_data):
    """Generate objective portfolio construction insights - educational only"""
    insights = []
    
    # Top performers by different metrics (FACTUAL REPORTING)
    top_sharpe = summary_data.nlargest(3, 'avg_sharpe_21')['symbol'].tolist()
    top_return = summary_data.nlargest(3, 'total_return')['symbol'].tolist()
    low_risk = summary_data.nsmallest(3, 'avg_custom_risk_score')['symbol'].tolist()
    
    # CHANGED: More objective language
    insights.append(f"📊 **Highest Risk-Adjusted Returns**: {', '.join(top_sharpe)} show the best Sharpe ratios in your selection")
    insights.append(f"📈 **Top Absolute Returns**: {', '.join(top_return)} delivered the highest total returns")
    insights.append(f"📉 **Most Stable**: {', '.join(low_risk)} exhibit the lowest volatility patterns")
    
    # Risk distribution analysis (FACTUAL)
    high_risk_count = (summary_data['avg_custom_risk_score'] > 0.08).sum()
    total_count = len(summary_data)
    risk_percentage = (high_risk_count / total_count) * 100
    
    if high_risk_count / total_count > 0.5:
        insights.append(f"⚠️ **Risk Concentration**: {risk_percentage:.0f}% of your selection ({high_risk_count}/{total_count} stocks) shows elevated risk")
    elif high_risk_count > 0:
        insights.append(f"📊 **Risk Distribution**: {risk_percentage:.0f}% of your selection ({high_risk_count}/{total_count} stocks) shows elevated risk")
    else:
        insights.append(f"🛡️ **Risk Distribution**: All selected stocks show moderate to low risk characteristics")
    
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

def get_sector_mapping():
    """Map stocks to sectors for better organization"""
    return {
        'Technology': ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'NVDA', 'META', 'NFLX', 'ADBE', 'CRM', 'ORCL', 'CSCO', 'INTC', 'AMD', 'QCOM', 'TXN', 'AVGO', 'PYPL', 'UBER', 'SNOW'],
        'Financial Services': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'TFC', 'PNC', 'COF', 'AXP', 'BLK', 'SCHW', 'CB', 'ICE', 'CME', 'SPGI', 'MCO', 'V', 'MA'],
        'Healthcare': ['UNH', 'JNJ', 'PFE', 'ABBV', 'TMO', 'ABT', 'LLY', 'MRK', 'BMY', 'AMGN', 'GILD', 'CVS', 'CI', 'ANTM', 'HUM', 'CNC', 'BIIB', 'REGN', 'VRTX', 'ISRG'],
        'Consumer Discretionary': ['HD', 'NKE', 'MCD', 'LOW', 'SBUX', 'TJX', 'BKNG', 'MAR', 'GM', 'F', 'CCL', 'RCL', 'MGM', 'DIS', 'CMCSA'],
        'Consumer Staples': ['WMT', 'PG', 'KO', 'PEP', 'COST', 'WBA', 'EL', 'CL', 'KMB', 'GIS', 'K', 'HSY', 'MDLZ'],
        'Energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'PSX', 'VLO', 'MPC', 'OXY', 'BKR'],
        'Industrials': ['BA', 'CAT', 'HON', 'UPS', 'RTX', 'LMT', 'GE', 'MMM', 'FDX', 'NOC', 'UNP', 'CSX', 'NSC'],
        'Materials': ['LIN', 'APD', 'ECL', 'FCX', 'NEM', 'DOW', 'DD', 'PPG', 'SHW', 'NUE'],
        'Utilities': ['NEE', 'DUK', 'SO', 'D', 'EXC', 'XEL', 'SRE', 'AEP', 'ES', 'AWK'],
        'Real Estate': ['AMT', 'CCI', 'PLD', 'EQIX', 'PSA', 'EXR', 'AVB', 'EQR', 'WELL', 'SPG']
    }

def create_enhanced_stock_selection(unique_symbols):
    """Create enhanced stock selection with sector filtering"""
    sector_mapping = get_sector_mapping()
    
    # Create reverse mapping for symbols not in defined sectors
    symbol_to_sector = {}
    for sector, symbols in sector_mapping.items():
        for symbol in symbols:
            symbol_to_sector[symbol] = sector
    
    # Add "Other" category for symbols not in predefined sectors
    other_symbols = [sym for sym in unique_symbols if sym not in symbol_to_sector]
    if other_symbols:
        sector_mapping['Other'] = other_symbols
        for sym in other_symbols:
            symbol_to_sector[sym] = 'Other'
    
    # Sector filter UI
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_sectors = st.multiselect(
            "Filter by Sector",
            options=list(sector_mapping.keys()),
            default=['Technology', 'Financial Services', 'Healthcare'],  # Start with popular sectors
            help="Select sectors to filter available stocks"
        )
    
    with col2:
        if st.button("🏢 All Sectors", key="select_all_sectors"):
            selected_sectors = list(sector_mapping.keys())
            st.rerun()
    
    # Get filtered symbols based on selected sectors
    filtered_symbols = []
    for sector in selected_sectors:
        if sector in sector_mapping:
            filtered_symbols.extend(sector_mapping[sector])
    
    # Remove duplicates and filter to only available symbols
    filtered_symbols = list(set(filtered_symbols))
    available_symbols = [sym for sym in filtered_symbols if sym in unique_symbols]
    available_symbols.sort()
    
    # Stock selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_symbols = st.multiselect(
            "Choose stocks to analyze",
            available_symbols,
            default=available_symbols[:8] if len(available_symbols) >= 8 else available_symbols,
            help="Select stocks for detailed analysis and comparison"
        )
    
    with col2:
        if st.button("📈 Select All", key="select_all_stocks"):
            selected_symbols = available_symbols
            st.rerun()
    
    # Show selection summary
    if selected_symbols:
        st.info(f"Selected {len(selected_symbols)} stocks from {len(selected_sectors)} sectors")
    
    return selected_symbols

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
    
   # Data info section with improved metric cards
    st.markdown('<div class="section-header"><span class="section-icon">📊</span><h2>Market Overview</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card("Stocks Analyzed", str(df['symbol'].nunique()), "Active Symbols", "🏢")
    
    with col2:
        create_metric_card("Data Points", f"{len(df):,}", "Total Records", "📊")
    
    with col3:
        if 'download_time' in df.columns and not df['download_time'].isna().all():
            try:
                last_update = pd.to_datetime(df['download_time'].iloc[0])
                formatted_time = last_update.strftime("%H:%M")
                create_metric_card("Last Update", formatted_time, "Today", "🕐")
            except:
                create_metric_card("Last Update", "Recent", "Data Fresh", "🕐")
        else:
            create_metric_card("Last Update", "Recent", "Data Fresh", "🕐")
    
    with col4:
        date_range = df['Date'].max() - df['Date'].min()
        create_metric_card("Date Range", f"{date_range.days}", "Days Coverage", "📅")
    
    # Add some spacing after metrics
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stock Selection
   # Stock Selection section
st.markdown('<div class="section-header"><span class="section-icon">🎯</span><h2>Stock Selection</h2></div>', unsafe_allow_html=True)

unique_symbols = sorted(df['symbol'].unique())
selected_symbols = create_enhanced_stock_selection(unique_symbols)
    
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
        
        # Portfolio metrics with enhanced calculations
        portfolio_return = summary['total_return'].mean()
        portfolio_risk = summary['avg_custom_risk_score'].mean()
        best_performer = summary.loc[summary['total_return'].idxmax(), 'symbol']
        worst_performer = summary.loc[summary['total_return'].idxmin(), 'symbol']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Dynamic return analysis with intelligent indicators
            return_icon = "📈" if portfolio_return > 0 else "📉" if portfolio_return < 0 else "➡️"
            return_magnitude = abs(portfolio_return)
            
            if return_magnitude > 0.2:  # >20% return
                return_descriptor = "Excellent" if portfolio_return > 0 else "Major Loss"
            elif return_magnitude > 0.1:  # >10% return
                return_descriptor = "Strong" if portfolio_return > 0 else "Heavy Loss"
            elif return_magnitude > 0.05:  # >5% return
                return_descriptor = "Good" if portfolio_return > 0 else "Moderate Loss"
            elif return_magnitude > 0:
                return_descriptor = "Modest" if portfolio_return > 0 else "Small Loss"
            else:
                return_descriptor = "Flat"
            
            create_metric_card(
                "Portfolio Return",
                f"{portfolio_return:.2%}",
                return_descriptor,
                return_icon
            )
        
        with col2:
            # Intelligent risk assessment
            if portfolio_risk > 0.15:
                risk_icon = "🔴"
                risk_level = "High Risk"
            elif portfolio_risk > 0.08:
                risk_icon = "🟡"
                risk_level = "Moderate"
            elif portfolio_risk > 0.04:
                risk_icon = "🟢"
                risk_level = "Low Risk"
            else:
                risk_icon = "🟢"
                risk_level = "Very Safe"
                
            create_metric_card(
                "Average Risk Score",
                f"{portfolio_risk:.3f}",
                risk_level,
                risk_icon
            )
        
        with col3:
            # Best performer with shorter context
            best_return = summary.loc[summary['symbol'] == best_performer, 'total_return'].iloc[0]
            
            create_metric_card(
                "Best Performer",
                best_performer,
                f"{best_return:.2%} • Top Pick",
                "🏆"
            )
        
        with col4:
            # Worst performer with shorter context
            worst_return = summary.loc[summary['symbol'] == worst_performer, 'total_return'].iloc[0]
            
            create_metric_card(
                "Worst Performer",
                worst_performer,
                f"{worst_return:.2%} • Review",
                "⚠️"
            )
   # Create portfolio context for individual stock analysis
    portfolio_context = {
        'avg_return': summary['total_return'].mean(),
        'avg_volatility': summary['volatility_21'].mean() if 'volatility_21' in summary.columns else 0,
        'portfolio_size': len(selected_symbols),
        'best_performer': summary.loc[summary['total_return'].idxmax(), 'symbol'] if not summary.empty else None,
        'worst_performer': summary.loc[summary['total_return'].idxmin(), 'symbol'] if not summary.empty else None
    }
            
    # Individual Stock Analysis Section
    st.subheader("🔍 Individual Stock Analysis")
    st.markdown("*Comprehensive analysis for all your selected stocks*")  
    
    # Analyze ALL selected stocks, sorted by return (best first, but show all)
    all_stocks = summary.sort_values('total_return', ascending=False)
    
    for _, row in all_stocks.iterrows():
        # Get comprehensive insights for EVERY stock
        comprehensive_insights = generate_comprehensive_analysis(row['symbol'], row, portfolio_context)
        
        if comprehensive_insights:
            # Add a visual indicator for performance level
            return_pct = row['total_return']
            if return_pct > 0.15:
                performance_indicator = "🚀 Strong Performer"
            elif return_pct > 0.05:
                performance_indicator = "📈 Positive"
            elif return_pct > 0:
                performance_indicator = "📊 Modest Gains"
            elif return_pct > -0.10:
                performance_indicator = "📉 Declining"
            else:
                performance_indicator = "⚠️ Significant Decline"
            
            with st.expander(f"📊 {row['symbol']} - {performance_indicator} ({return_pct:.1%})"):
                for insight in comprehensive_insights:
                    st.markdown(insight)
                    
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
        portfolio_tips = generate_portfolio_optimization_insights(summary)
        if portfolio_tips:
            st.subheader("🎯 Portfolio Composition Analysis")
            for tip in portfolio_tips:
                st.success(tip)
        
        st.markdown("---")
        
    
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

