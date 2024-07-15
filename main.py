import streamlit as st
import pandas as pd
from alpha_scout import apirequest as rq
from alpha_scout import timeconvert as tc
from alpha_scout import arbitrage as arb
from alpha_scout import userinterface as ui


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
    events = []
    for row in df.iterrows():
        events.append(arb.Event(row[1]))
    for event in events:
            event_container = ui.EventContainer()
            event_container.writeCol(1, f"{event.sport_title}")
            event_container.writeCol(2, f"{time_zone.toLocalTime(event.commence_time)}")
            event_container.writeCol(3, f"{event.home_team}")
            event_container.writeCol(3, "VS")
            event_container.writeCol(3, f"{event.away_team}")
            event_container.writeCol(5, f"Best odds")