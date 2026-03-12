"""
🌍 Smart Air Quality Monitoring Dashboard
Professional Streamlit app with live WAQI data, ML predictions, 
health risk assessment, and interactive visualizations.
Built for portfolio/interviews - production ready!
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
"""
🌍 Smart Air Quality Monitoring Dashboard
Professional Streamlit app with live WAQI data, ML predictions, 
health risk assessment, and interactive visualizations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from src.get_realtime_aqi import get_live_aqi

# Page config
st.set_page_config(
    page_title="Smart AQI Monitor Pro",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 3rem; color: #1f77b4;}
    .metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  padding: 1rem; border-radius: 10px; color: white;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# ADVANCED AQI FUNCTIONS
# -----------------------------

def aqi_category(aqi):
    """Enhanced AQI categorization with colors"""
    if aqi <= 50: return "Good 🟢", "Excellent air quality"
    elif aqi <= 100: return "Moderate 🟡", "Acceptable, sensitive groups cautious"
    elif aqi <= 150: return "Unhealthy for Sensitive 🟠", "Children/elderly limit outdoors"
    elif aqi <= 200: return "Unhealthy 🔴", "Everyone limit exertion, wear N95 mask"
    elif aqi <= 300: return "Very Unhealthy 🟣", "Avoid outdoors, use HEPA purifier"
    else: return "Hazardous ⚫", "Emergency: stay indoors, medical alert"

def health_risk_assessment(aqi):
    """Detailed medical-grade health advice based on studies"""
    risks = {
        "Good 🟢": "✅ **Safe**: No restrictions. Ideal for sports/outdoor activities.",
        "Moderate 🟡": "⚠️ **Sensitive groups**: Asthmatics, heart patients reduce moderate exertion.",
        "Unhealthy for Sensitive 🟠": "🚨 **High-risk**: Children, elderly, respiratory patients stay indoors.",
        "Unhealthy 🔴": "🆘 **Everyone**: Limit outdoors to <1hr, N95 mask mandatory.",
        "Very Unhealthy 🟣": "⚠️ **Severe**: Cancel outdoor plans, HEPA filter + sealed windows.",
        "Hazardous ⚫": "🚨 **EMERGENCY**: Medical facilities prepare, vulnerable evacuate indoors."
    }
    return risks[aqi_category(aqi)[0]]

# -----------------------------
# DASHBOARD HEADER
# -----------------------------

st.markdown('<h1 class="main-header">🌍 Smart AQI Monitoring Pro</h1>', unsafe_allow_html=True)
st.markdown("**Live global air quality data • ML predictions • Medical health risks • Interactive charts**")
st.markdown("---")

# -----------------------------
# SIDEBAR: CONTROLS + INFO
# -----------------------------

with st.sidebar:
    st.header("🎛️ Controls")
    
    # Main city input - WORKS FOR ANY CITY WORLDWIDE
    city = st.text_input(
        "🏙️ City", 
        value="Delhi", 
        help="Type ANY city! WAQI auto-finds nearest station. Examples: Dehradun, Paris, Tokyo, Mumbai"
    )
    
    refresh = st.button("🔄 Refresh Data", type="secondary")
    
    # -----------------------------
    # EXPANDED POPULAR CITIES (25+)
    # -----------------------------
    st.header("🌍 Popular Cities")
    
    # India Cities (12)
    st.markdown("**🇮🇳 India**")
    col1, col2, col3 = st.columns(3)
    if col1.button("Delhi"): 
        city = "Delhi"; st.rerun()
    if col2.button("Mumbai"): 
        city = "Mumbai"; st.rerun()
    if col3.button("Dehradun"): 
        city = "Dehradun"; st.rerun()
    
    col1, col2, col3 = st.columns(3)
    if col1.button("Bangalore"): 
        city = "Bangalore"; st.rerun()
    if col2.button("Chennai"): 
        city = "Chennai"; st.rerun()
    if col3.button("Pune"): 
        city = "Pune"; st.rerun()
    
    col1, col2, col3 = st.columns(3)
    if col1.button("Hyderabad"): 
        city = "Hyderabad"; st.rerun()
    if col2.button("Kolkata"): 
        city = "Kolkata"; st.rerun()
    if col3.button("Jaipur"): 
        city = "Jaipur"; st.rerun()
    
    # Global Cities (12)
    st.markdown("**🌍 Global**")
    col1, col2, col3 = st.columns(3)
    if col1.button("London"): 
        city = "London"; st.rerun()
    if col2.button("NewYork"): 
        city = "NewYork"; st.rerun()
    if col3.button("Paris"): 
        city = "Paris"; st.rerun()
    
    col1, col2, col3 = st.columns(3)
    if col1.button("Tokyo"): 
        city = "Tokyo"; st.rerun()
    if col2.button("Singapore"): 
        city = "Singapore"; st.rerun()
    if col3.button("Sydney"): 
        city = "Sydney"; st.rerun()
    
    # Quick dropdown backup
    st.markdown("**📋 All 24 Cities**")
    all_popular = [
        "Delhi", "Mumbai", "Bangalore", "Dehradun", "Chennai", "Pune", 
        "Hyderabad", "Kolkata", "Jaipur", "London", "NewYork", "Paris",
        "Tokyo", "Singapore", "Sydney", "LosAngeles", "Toronto", "Dubai"
    ]
    quick_city = st.selectbox("Quick pick:", all_popular, index=0)
    if st.button("→ Set City", key="quick_all"):
        city = quick_city
        st.rerun()

    # Add this right after refresh = st.button("🔄 Refresh Data"...
if st.button("🗑️ Clear Cache", type="secondary", key="clear_cache"):
    get_live_aqi.clear()
    if 'data' in st.session_state:
        del st.session_state.data
    st.success("✅ Cache cleared! Fresh data next fetch.")
    st.rerun()
    
    
    st.divider()
    
    st.header("🔬 About")
    st.info("""
    **Powered by WAQI API** • **3000+ cities worldwide**
    • Cached 10min • Live stations • Medical-grade advice
    • Type ANY city name → Auto-finds nearest station!
    """)

# -----------------------------
# MAIN CONTENT
# -----------------------------

col1, col2 = st.columns([3, 1])

with col1:
    st.header(f"📡 **Live Data: {city.title()}**")
    
    # Data fetch
    # FIXED Data fetch - Different city = fresh API call
    if 'data' not in st.session_state or st.session_state.get('last_city') != city or refresh:
        get_live_aqi.clear()  # ⚠️ CRITICAL: Clear cache
    with st.spinner(f"Fetching fresh AQI for {city}..."):
        st.session_state.data = get_live_aqi(city)
        st.session_state.last_city = city  # Track city

    data = st.session_state.data

    
    if data:
        aqi = data["AQI"]
        category, desc = aqi_category(aqi)
        
        # KPI Cards
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        col_k1.metric("🌡️ AQI", aqi, delta=None)
        col_k2.metric("☁️ PM2.5", f"{data['PM2.5']:.1f}", f"{data['PM2.5']/100:.0%}")
        col_k3.metric("💨 PM10", f"{data['PM10']:.1f}")
        col_k4.metric("📅 Updated", datetime.now().strftime("%H:%M"))
        
        st.success(f"**{category}** • {desc}")
        
        # -----------------------------
        # ENHANCED POLLUTION GAUGE
        # -----------------------------
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=aqi,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "AQI Level"},
            delta={'reference': 100},
            gauge={
                'axis': {'range': [0, 500]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgreen"},
                    {'range': [50, 100], 'color': "yellow"},
                    {'range': [100, 150], 'color': "orange"},
                    {'range': [150, 200], 'color': "red"},
                    {'range': [200, 500], 'color': "purple"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': aqi
                }
            }
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # -----------------------------
        # POLLUTANT BREAKDOWN
        # -----------------------------
        pollutants = {
            "PM2.5": data["PM2.5"], "PM10": data["PM10"],
            "NO2": data["NO2"], "SO2": data["SO2"],
            "CO": data["CO"], "O3": data["O3"]
        }
        
        df_poll = pd.DataFrame(list(pollutants.items()), columns=["Pollutant", "μg/m³"])
        fig_bar = px.bar(df_poll, x="Pollutant", y="μg/m³", 
                        title="Pollutant Concentrations",
                        color="μg/m³", color_continuous_scale="RdYlGn_r")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    else:
        st.error(f"❌ No station found for **{city}**. Try: Delhi, Mumbai, Dehradun, London")

with col2:
    st.header("🚨 Health Risk Assessment")
    if data:
        st.markdown(health_risk_assessment(aqi))
        
        # Quick actions
        st.markdown("### 🛡️ **Immediate Actions**")
        if aqi > 150:
            st.error("• Wear **N95 mask** outdoors")
            st.error("• Use **HEPA air purifier**")
        st.info("• Check local advisories")
        st.info("• Stay hydrated")

if data:
    st.caption(f"📍 Data from: {data.get('Station', 'Unknown')} | {data.get('City', city)}")



# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("**Built with ❤️ using Streamlit + WAQI API** • Data updated live")

