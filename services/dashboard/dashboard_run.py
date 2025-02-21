import time

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from config.config import hopsworksCredentialsConfig, hopsworksSettingsConfig
from loguru import logger
from utils.date_converter import convert_timestamp_ms_todatetime
from utils.feature_reader import FeatureReader

# Set page config
st.set_page_config(
    page_title='Real-Time Crypto Dashboard', page_icon='📈', layout='wide'
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


# Get initial historical data with caching
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_initial_data(_reader: FeatureReader, days: int) -> pd.DataFrame:
    return _reader.get_data(n_days=days)


#############
## Sidebar ##
#############
refresh_interval = st.sidebar.selectbox(
    'Select Refresh Interval',
    options=[15, 30, 60],
    format_func=lambda x: f'{x} seconds',
)

real_time_toggle = st.sidebar.toggle('Enable Real-time Updates', False)

pair_to_be_displayed = st.sidebar.selectbox(
    'Select Pair', options=['BTC/USD', 'BTC/EUR', 'ETH/EUR', 'ETH/USD'], index=1
)

candle_seconds_to_be_displayed = st.sidebar.selectbox(
    'Select Candle Window Length (in sec)', options=[5, 10, 30, 60, 180], index=3
)

##################
## Main content ##
##################
st.title('Real-Time Crypto Dashboard')

# Initialize session state
if 'crypto_data' not in st.session_state:
    st.session_state.crypto_data = pd.DataFrame()

# Main logic
try:
    # Set ms columns
    ms_columns = ['timestamp_ms', 'window_start_ms', 'window_end_ms']

    # Initialize reader
    reader = init_feature_reader()

    # Initial data load (only if not already loaded)
    if st.session_state.crypto_data.empty:
        with st.spinner('Loading initial data...'):
            df = get_initial_data(reader, days=10)
            df = convert_timestamp_ms_todatetime(df=df, columns_to_convert=ms_columns)
            st.session_state.crypto_data = df

    # Filter data for display
    crypto_df = (
        st.session_state.crypto_data.drop(columns=ms_columns)
        .sort_values(by=['pair', 'timestamp_ms_date', 'candle_seconds'])
        .reset_index(drop=True)
    )
    crypto_df = crypto_df[crypto_df['pair'] == pair_to_be_displayed]
    crypto_df = crypto_df[crypto_df['candle_seconds'] == candle_seconds_to_be_displayed]

    # Display the filtered dataframe
    st.dataframe(data=crypto_df)

    # Create and display candlestick chart
    if not crypto_df.empty:
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=crypto_df['window_start_ms_date'],
                    open=crypto_df['open'],
                    high=crypto_df['high'],
                    low=crypto_df['low'],
                    close=crypto_df['close'],
                    increasing_line_color='green',
                    decreasing_line_color='red',
                )
            ]
        )

        # Update layout
        fig.update_layout(
            title=f'Real-Time Crypto Candlestick Chart (Pair: {pair_to_be_displayed}, {candle_seconds_to_be_displayed}s Candles)',
            yaxis_title='Price',
            xaxis_title='Time',
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            xaxis={
                'tickformat': '%H:%M:%S',
                'autorange': True,
            },
            yaxis={
                'autorange': True,
                'gridcolor': 'gray',
            },
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning('No data available for the selected pair and candle window length.')

    # Real-time updates
    if real_time_toggle:
        logger.info('Real-Time Updates have been triggered')
        with st.spinner('Fetching latest data...'):
            new_data = reader.get_data(n_days=1)
            if not new_data.empty:
                # Add human readable timestamps to the new data
                new_data = convert_timestamp_ms_todatetime(
                    df=new_data, columns_to_convert=ms_columns
                )

                # Update data
                st.session_state.crypto_data = pd.concat(
                    [st.session_state.crypto_data, new_data]
                ).drop_duplicates(subset=['pair', 'timestamp_ms', 'candle_seconds'])
            else:
                logger.warning('Newest data fetch has been empty!')

        time.sleep(refresh_interval)
        st.rerun()

except Exception as e:
    st.error(f'Error connecting to feature store or processing data: {str(e)}')
