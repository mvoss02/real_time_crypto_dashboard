from utils.feature_reader import FeatureReader
from config.config import hopsworksSettingsConfig, hopsworksCredentialsConfig

import streamlit as st


# Set page config
st.set_page_config(
    page_title="Real-Time Crypto Dashboard",
    page_icon="📈",
    layout="wide"
)

# Initialize FeatureReader with caching
@st.cache_resource
def init_feature_reader():
    return FeatureReader(
        hopsworks_project_name=hopsworksCredentialsConfig.project_name,
        hopsworks_api_key=hopsworksCredentialsConfig.api_key,
        feature_group_name=hopsworksSettingsConfig.feature_group_name, 
        feature_group_version=hopsworksSettingsConfig.feature_group_version,
        feature_view_name=hopsworksSettingsConfig.feature_view_name,
        feature_view_version=hopsworksSettingsConfig.feature_view_version,
    )

# Get data with caching
@st.cache_data(ttl=60)  # Cache for 60 seconds
def get_crypto_data(_reader: FeatureReader, days: int):
    return _reader.gets_data(n_days=days)

# Initialize connection
try:
    reader = init_feature_reader()
    
    # Main content
    st.title("Real-Time Crypto Dashboard")
    
    # Load data
    with st.spinner("Loading data..."):
        df = get_crypto_data(reader, days=10)
        
        st.dataframe(data=df)

except Exception as e:
    st.error(f"Error connecting to feature store: {str(e)}")



