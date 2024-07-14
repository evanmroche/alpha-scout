import streamlit as st
import pandas as pd
import apirequest as rq
import timeconvert as tc


st.set_page_config(layout='wide')

with st.sidebar:
    st.title("Alpha Scout")

    apiKey = st.text_input(label="Key:", label_visibility='collapsed', type='password', placeholder="The Odds API Key")
    
    api = rq.ApiRequest.init()

    with st.expander("Formatting", True):
        betSize = st.number_input("Bet Size", min_value=10, max_value=1000000, step=25, value=100)
        oddsFormat = st.selectbox("Odds Format", api.oddsFormats, index=0)
        timeZone = tc.TimeZone(st.selectbox("Local Timezone", tc.TimeZone.allTimeZones))

    with st.expander("Search", True):
        leagues = st.selectbox("Sports Leage:", api.allLeagues)
        regions = st.multiselect("Regions", api.allRegions, default='US')
        markets = st.multiselect("Markets", api.allMarkets, default='Moneyline')
        bookmakers = st.multiselect("Bookmakers", api.allBookmakers, placeholder="All bookmakers")

api = rq.ApiRequest(oddsFormat, betSize, timeZone, leagues, regions, markets, bookmakers, apiKey)

if st.button("Search for Odds"):
    df = api.CallAPI()
    dfIsValid = api.ApiErrorCheck(df)
    if dfIsValid:
        df.to_pickle('df.pkl')
else:
    try:
        df = pd.read_pickle('df.pkl')
        dfIsValid = True
    except FileNotFoundError:
        dfIsValid = False

if dfIsValid:
    df.drop('id', axis=1, inplace=True)
    df.drop('sport_key', axis=1, inplace=True)
    st.dataframe(df)

    event0 = df.iloc[0]
    event0time = event0['commence_time']
    st.dataframe(event0)