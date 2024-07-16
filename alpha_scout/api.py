import requests
import streamlit as st
import pandas as pd
from alpha_scout import options

class ApiRequest:
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

    def __init__(self, time_zone, league, regions, markets, api_key):
        self.time_zone = time_zone
        self.sport_key = self.listToStr(league, options.all_leagues)
        self.regions = self.listToStr(regions, options.all_regions)
        self.markets = self.listToStr(markets, options.all_markets)
        self.api_key = api_key

class Outcome:
    def __init__(self, outcome_dict):
        self.name = outcome_dict['name']
        self.price = outcome_dict['price']
        if 'point' in outcome_dict:
            self.point = outcome_dict['point']
        if 'description' in outcome_dict:
            self.description = outcome_dict['description']

class Market:
    def __init__(self, market_dict):
        self.key = market_dict['key']
        self.last_update = market_dict['last_update']
        self.outcomes = []
        for outcome in market_dict['outcomes']:
            self.outcomes.append(Outcome(outcome))

class Bookmaker:
    def __init__(self, bookmaker_dict):
        self.key = bookmaker_dict['key']
        self.title = bookmaker_dict['title']
        self.last_update = bookmaker_dict['last_update']
        self.markets = []
        for market in bookmaker_dict['markets']:
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