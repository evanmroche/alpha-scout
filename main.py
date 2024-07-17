import streamlit as st
import pandas as pd
from alpha_scout import api
from alpha_scout import timeconvert as tc
from alpha_scout import arbitrage as arb
from alpha_scout import userinterface as ui
from alpha_scout import options

def main():    
    st.set_page_config(layout='wide')
    with st.sidebar:
        st.title("Alpha Scout")

        api_key = st.text_input(label="Key:", label_visibility='collapsed', type='password', placeholder="The Odds API Key")
        
        with st.expander("Formatting", True):
            bet_size = st.number_input("Bet Size", min_value=10, max_value=1000000, step=25, value=100)
            odds_format = st.selectbox("Odds Format", options.odds_formats, index=0)
            time_zone = tc.TimeZone(st.selectbox("Local Timezone", options.all_time_zones))

        with st.expander("Search", True):
            leagues = st.selectbox("Sports Leage:", options.all_leagues)
            regions = st.multiselect("Regions", options.all_regions, default='US')
            markets = st.multiselect("Markets", options.all_markets, default='Moneyline', placeholder="All Bookmakers")
            bookmakers = st.multiselect("Bookmakers", options.all_bookmakers, placeholder="All bookmakers")

    api_rq = api.ApiRequest(time_zone, leagues, regions, markets, api_key)

    if st.button("Search for Odds"):
        df = api_rq.callAPI()
        df_is_valid = api_rq.apiErrorCheck(df)
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
            events.append(api.Event(row[1]))
        for event in events:
                event_container = ui.EventContainer()
                event_container.writeCol(1, f"{event.sport_title}")
                event_container.writeCol(2, f"{time_zone.toLocalTime(event.commence_time)}")
                event_container.writeCol(3, f"{event.home_team}")
                event_container.writeCol(3, "VS")
                event_container.writeCol(3, f"{event.away_team}")

                arbitrage = arb.ArbitrageEvent(event, bookmakers, 'h2h')
                if odds_format == 'American':
                    best_home_odds = arb.decimalToAmerican(arbitrage.home_odds)
                    best_away_odds = arb.decimalToAmerican(arbitrage.away_odds)
                else:
                    best_home_odds = arbitrage.home_odds
                    best_away_odds = arbitrage.away_odds
                event_container.writeCol(5, f"{arbitrage.home_bookmaker.title}: {best_home_odds}")
                event_container.writeCol(5, f"Best odds")
                event_container.writeCol(5, f"{arbitrage.away_bookmaker.title}: {best_away_odds}")
                event_container.writeCol(6, f"Arbitrage Percentage")
                event_container.writeCol(6, f"{arbitrage.arbitrage_percentage}%")

                

if __name__ == '__main__':
    main() 

