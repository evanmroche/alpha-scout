import requests
import streamlit as st
import pandas as pd

class ApiRequest:
    odds_formats = {'Decimal':'decimal', 'American':'american'}
    all_leagues = {'Upcoming':'upcoming','NFL':'americanfootball_nfl','NBA':'basketball_nba','MLB':'baseball_mlb'}
    all_regions = {'US':'us', 'US2':'us2', 'UK':'uk', 'EU':'eu'}
    all_markets = {'Moneyline':'h2h', 'Spreads':'spreads', 'Totals':'totals'}
    all_bookmakers = {'FanDuel':'fanduel', 'DraftKings':'draftkings', 'BetMGM':'betmgm', 'Caesars':'williamhill_us'}

    # List is an array of titles, list_dict is a dictionary mapping titles to strings
    def listToStr(self, list, list_dict):
        temp_str = ''
        for title in list_dict:
            if title in list:
                if temp_str != '':
                    temp_str += ','
                temp_str += list_dict[title]
        return temp_str

    def callAPI(self):
        odds_response = requests.get(
            f'https://api.the-odds-api.com//v4/sports/{self.sport_key}/odds/?apiKey={self.api_key}&regions={self.regions}&markets={self.markets}',
            ).json()
        return pd.json_normalize(odds_response)
        
    def apiErrorCheck(self, df : pd.DataFrame):
        if 'error_code' in df.columns:
            match df['error_code'].to_string(index=False):
                case 'INVALID_KEY':
                    st.error("Invalid API key!")
                case 'MISSING_KEY':
                    st.error("Missing API key!")
                case 'INVALID_REGION':
                    st.error("Select one or more regions!")
            return False
        return True

    @classmethod
    def init(cls):
        return cls

    def __init__(self, time_zone, league, regions, markets, bookmakers, api_key):
        self.time_zone = time_zone
        self.sport_key = self.listToStr(league, self.all_leagues)
        self.regions = self.listToStr(regions, self.all_regions)
        self.markets = self.listToStr(markets, self.all_markets)
        self.bookmakers = bookmakers
        self.api_key = api_key

class Outcome:
    def __init__(self, outcomeDict):
        self.name = outcomeDict['name']
        self.price = outcomeDict['price']
        if 'point' in outcomeDict:
            self.point = outcomeDict['point']
        if 'description' in outcomeDict:
            self.description = outcomeDict['description']

class Market:
    def __init__(self, marketDict):
        self.key = marketDict['key']
        self.last_update = marketDict['last_update']
        self.outcomes = []
        for outcome in marketDict['outcomes']:
            self.outcomes.append(Outcome(outcome))

class Bookmaker:
    def __init__(self, bookmakerDict):
        self.key = bookmakerDict['key']
        self.title = bookmakerDict['title']
        self.last_update = bookmakerDict['last_update']
        self.markets = []
        for market in bookmakerDict['markets']:
            self.markets.append(Market(market))

class Event:
    def __init__(self, df):
        self.df = df
        self.sport_key = df['sport_key']
        self.id = df['id']
        self.commence_time = df['commence_time']
        self.sport_title = df['sport_title']
        self.home_team = df['home_team']
        self.away_team = df['away_team']
        self.bookmakers = []
        for bookmaker in df['bookmakers']:
            self.bookmakers.append(Bookmaker(bookmaker))