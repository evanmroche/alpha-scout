import streamlit as st
import pandas as pd
import apirequest as rq
import timeconvert as tc


st.set_page_config(layout='wide')

with st.sidebar:
    st.title("Alpha Scout")

    apiKey = st.text_input(label="Key:", label_visibility='collapsed', type='password', placeholder="The Odds API Key")

    with st.expander("Formatting", True):
        betSize = st.number_input("Bet Size", min_value=10, max_value=1000000, step=25, value=100)
        oddsFormats = ['Decimal', 'American']
        oddsFormat = st.selectbox("Odds Format", oddsFormats, index=0)
        timeZones = ['Pacific', 'Mountain', 'Central', 'Eastern']
        timeZone = tc.TimeZone(st.selectbox("Local Timezone", timeZones))

    with st.expander("Search", True):
        allLeagues = ['Upcoming','NBA', 'MLB', '...']
        leagues = st.selectbox("Sports Leage:", allLeagues)

        allRegions = ['US', 'US2', 'UK', 'EU']
        regions = st.multiselect("Regions", allRegions, default='US')

        allMarkets = ['Moneyline', 'Spreads', 'Totals']
        markets = st.multiselect("Markets", allMarkets, default='Moneyline')

        allBookmakers = ['DraftKings', 'FanDuel', 'BetMGM', 'Caesars', '...']
        bookmakers = st.multiselect("Bookmakers", allBookmakers, placeholder="All bookmakers")

r = rq.Request(oddsFormat, betSize, timeZone, leagues, regions, markets, bookmakers, apiKey)

df = None
if st.button("Search for Odds"):
    df = r.CallAPI()
    df.to_pickle('df.pkl')
else:
    df = pd.read_pickle('df.pkl')

if not df.empty:
    df.drop('id', axis=1, inplace=True)
    df.drop('sport_key', axis=1, inplace=True)
    st.dataframe(df)

    event0 = df.iloc[0]
    event0time = event0['commence_time']
    st.write(timeZone.ToLocalTime(event0time))
    st.dataframe(event0)