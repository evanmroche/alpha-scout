import streamlit as st
import pandas as pd
from alpha_scout import apirequest as rq
from alpha_scout import timeconvert as tc
from alpha_scout import arbitrage as arb


st.set_page_config(layout='wide')

with st.sidebar:
    st.title("Alpha Scout")

    api_key = st.text_input(label="Key:", label_visibility='collapsed', type='password', placeholder="The Odds API Key")
    
    with st.expander("Formatting", True):
        bet_size = st.number_input("Bet Size", min_value=10, max_value=1000000, step=25, value=100)
        odds_format = st.selectbox("Odds Format", rq.ApiRequest.odds_formats, index=0)
        time_zone = tc.TimeZone(st.selectbox("Local Timezone", tc.TimeZone.all_time_zones))

    with st.expander("Search", True):
        leagues = st.selectbox("Sports Leage:", rq.ApiRequest.all_leagues)
        regions = st.multiselect("Regions", rq.ApiRequest.all_regions, default='US')
        markets = st.multiselect("Markets", rq.ApiRequest.all_markets, default='Moneyline', placeholder="All Bookmakers")
        bookmakers = st.multiselect("Bookmakers", rq.ApiRequest.all_bookmakers, placeholder="All bookmakers")

api = rq.ApiRequest(odds_format, bet_size, time_zone, leagues, regions, markets, bookmakers, api_key)

if st.button("Search for Odds"):
    df = api.callAPI()
    df_is_valid = api.apiErrorCheck(df)
    if df_is_valid:
        df.to_pickle('df.pkl')
else:
    try:
        df = pd.read_pickle('df.pkl')
        df_is_valid = True
    except FileNotFoundError:
        df_is_valid = False

if df_is_valid:
    df.drop('id', axis=1, inplace=True)
    df.drop('sport_key', axis=1, inplace=True)
    st.dataframe(df)

    event_0 = df.iloc[0]
    event_0_time = event_0['commence_time']
    st.dataframe(event_0)