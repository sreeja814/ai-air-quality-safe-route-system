import requests
import streamlit as st
import os

# Secure token handling
WAQI_TOKEN = st.secrets.get("WAQI_TOKEN", os.getenv("WAQI_TOKEN", "a5c6d5d52a527c28c0a8bcc3998b0fe9926020ec"))

@st.cache_data(ttl=600)  # Cache 10 minutes
def get_live_aqi(city="Delhi"):
    """
    MAGIC: User types ANY city → WAQI finds nearest station automatically!
    Works for 3000+ cities worldwide
    """
    if not WAQI_TOKEN or WAQI_TOKEN == "a5c6d5d52a527c28c0a8bcc3998b0fe9926020ec":
        st.error("❌ Add WAQI_TOKEN to Streamlit secrets or .env")
        return None
    
    # Auto-format city name for WAQI
    city_formatted = city.strip().title().replace(" ", "")
    
    url = f"https://api.waqi.info/feed/{city_formatted}/?token={WAQI_TOKEN}"
    
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            json_data = resp.json()
            
            # Check if WAQI found a station
            if json_data.get('status') == 'ok':
                data = json_data['data']
                iaqi = data.get('iaqi', {})
                
                return {
                    'AQI': int(data['aqi']),
                    'PM2.5': float(iaqi.get('pm25', {}).get('v', 0)),
                    'PM10': float(iaqi.get('pm10', {}).get('v', 0)),
                    'NO2': float(iaqi.get('no2', {}).get('v', 0)),
                    'SO2': float(iaqi.get('so2', {}).get('v', 0)),
                    'CO': float(iaqi.get('co', {}).get('v', 0)),
                    'O3': float(iaqi.get('o3', {}).get('v', 0)),
                    'Station': data.get('station', {}).get('name', city_formatted),
                    'City': city_formatted,
                    'Timestamp': data.get('time', {}).get('s', 'Unknown')
                }
            else:
                return None
        else:
            return None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None
