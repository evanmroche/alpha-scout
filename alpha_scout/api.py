import requests
import streamlit as st
import pandas as pd
from alpha_scout import options

class ApiRequest:
    # List is an array of titles, list_dict is a dictionary mapping titles to strings
    def listToStr(self, list, list_dict):
        temp_str: str = ''
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

    def __init__(self, time_zone, league, regions, markets, api_key):
        self.time_zone = time_zone
        self.sport_key: str = self.listToStr(league, options.all_leagues)
        self.regions: str = self.listToStr(regions, options.all_regions)
        self.markets: str = self.listToStr(markets, options.all_markets)
        self.api_key: str = api_key

class Outcome:
    def __init__(self, outcome_dict):
        self.name: str = outcome_dict['name']
        self.price: float = outcome_dict['price']
        if 'point' in outcome_dict:
            self.point: float = outcome_dict['point']
        if 'description' in outcome_dict:
            self.description: str = outcome_dict['description']

class Market:
    def __init__(self, market_dict):
        self.key: str = market_dict['key']
        self.last_update = market_dict['last_update']
        self.outcomes: Outcome = []
        for outcome in market_dict['outcomes']:
            self.outcomes.append(Outcome(outcome))

class Bookmaker:
    def __init__(self, bookmaker_dict):
        self.key: str = bookmaker_dict['key']
        self.title: str = bookmaker_dict['title']
        self.last_update = bookmaker_dict['last_update']
        self.markets: Market = []
        for market in bookmaker_dict['markets']:
            self.markets.append(Market(market))

class Event:
    def __init__(self, df):
        self.df: pd.DataFrame = df
        self.sport_key: str = df['sport_key']
        self.id = df['id']
        self.commence_time = df['commence_time']
        self.sport_title: str = df['sport_title']
        self.home_team: str = df['home_team']
        self.away_team: str = df['away_team']
        self.bookmakers: Bookmaker = []
        for bookmaker in df['bookmakers']:
            self.bookmakers.append(Bookmaker(bookmaker))

def validateDfRow(df_row: pd.DataFrame) -> bool:
    if df_row['id'] == None:
        return False
    if df_row['sport_key'] == None:
        return False
    if df_row['sport_title'] == None:
        return False
    if df_row['home_team'] == None:
        return False
    if df_row['away_team'] == None:
        return False
    if len(df_row['bookmakers']) == 0:
        return False
    return True