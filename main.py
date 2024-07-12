import streamlit as st
import pandas as pd
import request as rq
import requests
import json

st.set_page_config(layout='wide')

with st.sidebar:
    st.title("Alpha Scout")

    ApiKey = st.text_input(label="Key:", label_visibility='collapsed', type='password', placeholder="The Odds API Key")

    with st.expander("Formatting", True):
        betSize = st.number_input("Bet Size", min_value=10, max_value=1000000, step=25, value=100)
        oddsFormats = ['Decimal', 'American']
        oddsFormat = st.selectbox("Odds Format", oddsFormats)
        timeZones = ['PST', 'EST', '...']
        timeZone = st.selectbox("Timezone", timeZones)

    with st.expander("Search", True):
        allLeagues = ['NBA', 'MLB', '...']
        leagues = st.selectbox("Sports Leage:", allLeagues)

        allRegions = ['US', 'US2', 'UK', 'EU']
        regions = st.multiselect("Regions", allRegions)

        allMarkets = ['Moneyline', 'Spreads', 'Totals']
        markets = st.multiselect("Markets", allMarkets)

        allBookmakers = ['draftkings', 'fanduel', 'betmgm', 'williamhill_us', '...']
        bookmakers = st.multiselect("Bookmakers", allBookmakers)

r = rq.Request()
r.markets = 'h2h'
r.ApiKey = ApiKey
r.sportKey = 'upcoming'
r.regions = 'us'

oddsResponse = requests.get(
    f'https://api.the-odds-api.com//v4/sports/{r.sportKey}/odds/?apiKey={r.ApiKey}&regions={r.regions}&markets={r.markets}',
    )

data = oddsResponse.json()
df = pd.json_normalize(data)
df.drop(columns='id')

st.dataframe(df)