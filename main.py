from altair import value
import streamlit as st
from streamlit import session_state as ss
from streamlit_modal import Modal
import pandas as pd
from alpha_scout import api
from alpha_scout import timeconvert as tc
from alpha_scout import arbitrage as arb
from alpha_scout import userinterface as ui
from alpha_scout import options

def checkboxFlip(index):
    if ss[f'check{index}']:
        ss.include_bookmakers[index] = True
    else:
        ss.include_bookmakers[index] = False

def main():    
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    ui.formatPage()

    with st.sidebar:
        st.title("Alpha Scout")

        api_key = st.text_input(label="Key:", label_visibility='collapsed', type='password', placeholder="The Odds API Key")
        
        with st.expander("Formatting", True):
            bet_amount = st.number_input("Bet Amount", min_value=10, max_value=1000000, step=25, value=100)
            odds_format = st.selectbox("Odds Format", options.odds_formats, index=0)
            time_zone = tc.TimeZone(st.selectbox("Local Timezone", options.all_time_zones))

        with st.expander("Search", True):
                leagues = st.selectbox("Sports Leage:", options.all_leagues)
                regions = st.multiselect("Regions", options.all_regions, default='US')
                # markets = st.multiselect("Markets", options.all_markets, default='Moneyline', placeholder="All Bookmakers")
                markets = 'Moneyline'
                # bookmakers = st.multiselect("Bookmakers", options.all_bookmakers, placeholder="All bookmakers")
                if 'bookmakers' not in ss:
                    bookmakers = [None] * len(options.all_bookmakers)
                bookmakers_modal = Modal(key='choose_bookmakers', title='Choose Bookmakers')
                choose_bookmakers = st.button(label="Choose Bookmakers")
                if choose_bookmakers:
                    bookmakers_modal.open()

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
    
    if 'include_bookmakers' not in ss:
        ss.include_bookmakers = []
        for i, bookmaker in enumerate(options.all_bookmakers):
            ss.include_bookmakers.append(True)
    
    if bookmakers_modal.is_open():
        with bookmakers_modal.container():
            bookmaker_cols = st.columns(5)
            col_num = 0
            for i, bookmaker in enumerate(options.all_bookmakers):
                with bookmaker_cols[col_num]:
                            if ss.include_bookmakers[i]:
                                 st.checkbox(bookmaker, value=ss.include_bookmakers[i], key=f'check{i}', on_change=checkboxFlip, kwargs={'index':i})
                            else:
                                st.checkbox(bookmaker, value=ss.include_bookmakers[i], key=f'check{i}', on_change=checkboxFlip, kwargs={'index':i})
                col_num += 1
                if col_num >= 5:
                    col_num = 0
    
    for i, bookmaker in enumerate(options.all_bookmakers):
        if f'check{i}' not in ss:
            ss[f'check{i}'] = True
        if ss.include_bookmakers[i]:
            bookmakers[i] = bookmaker
        else:
            bookmakers[i] = None
    
    event_containers_container = st.container(border=True)
    with event_containers_container:
        if df_is_valid:
            events: api.Event = []
            title_container = ui.EventContainer()
            title_container.writeCol(1, "Arb %")
            title_container.writeCol(2, "League")
            title_container.writeCol(3, "Date/Time")
            title_container.writeCol(4, "Teams")
            title_container.writeCol(5, "Best Odds")
            title_container.writeCol(6, "Bet Amounts")
            title_container.writeCol(7, "Profit")
            for row in df.iterrows():
                if api.validateDfRow(row[1]):
                    events.append(api.Event(row[1]))
            for event in events:
                    arbitrage = arb.ArbitrageEvent(event, bookmakers, 'h2h', bet_amount)
                    event_container = ui.EventContainer()
                    if arbitrage.has_arbitrage:
                        event_container.writeCol(1, f":green[{arbitrage.arbitrage_percentage}%]")
                    else:
                        event_container.writeCol(1, f":red[{arbitrage.arbitrage_percentage}%]")
                    event_container.writeCol(2, f"{event.sport_title}")
                    event_container.writeCol(3, f"{time_zone.toLocalTime(event.commence_time)}")
                    event_container.writeCol(4, f"{event.home_team}")
                    if arbitrage.has_draw:
                        event_container.writeCol(4, f"Draw")
                    event_container.writeCol(4, f"{event.away_team}")

                    if odds_format == 'American':
                        best_home_odds = arb.decimalToAmerican(arbitrage.home_odds)
                        best_away_odds = arb.decimalToAmerican(arbitrage.away_odds)
                        if arbitrage.has_draw:
                            best_draw_odds = arb.decimalToAmerican(arbitrage.draw_odds)
                    else:
                        best_home_odds = arbitrage.home_odds
                        best_away_odds = arbitrage.away_odds
                        if arbitrage.has_draw:
                            best_draw_odds = arbitrage.draw_odds
                    event_container.writeCol(5, f"{arbitrage.home_bookmaker.title}: {best_home_odds}")
                    if arbitrage.has_draw:
                        event_container.writeCol(5, f"{arbitrage.draw_bookmaker.title}: {best_draw_odds}")
                    event_container.writeCol(5, f"{arbitrage.away_bookmaker.title}: {best_away_odds}")
                    event_container.writeCol(6, f"${arbitrage.home_bet_amount}")
                    if arbitrage.has_draw:
                        event_container.writeCol(6, f"\${arbitrage.draw_bet_amount}")
                    event_container.writeCol(6, f"${arbitrage.away_bet_amount}")
                    if arbitrage.has_arbitrage:
                        event_container.writeCol(7, f":green[\${arbitrage.home_win_profit} - \${arbitrage.away_win_profit}]")
                    else:
                        event_container.writeCol(7, f":red[\${arbitrage.home_win_profit} - \${arbitrage.away_win_profit}]")

if __name__ == '__main__':
    main() 