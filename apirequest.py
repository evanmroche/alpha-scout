import requests
import streamlit as st
import pandas as pd

class ApiRequest:
    oddsFormats = {'Decimal':'decimal', 'American':'american'}
    allLeagues = {'Upcoming':'upcoming','NBA':'basketball_nba','MLB':'baseball_mlb'}
    allRegions = {'US':'us', 'US2':'us2', 'UK':'uk', 'EU':'eu'}
    allMarkets = {'Moneyline':'h2h', 'Spreads':'spreads', 'Totals':'totals'}
    allBookmakers = {'FanDuel':'fanduel', 'DraftKings':'draftkings', 'BetMGM':'betmgm', 'Caesars':'williamhill_us'}

    # List is an array of titles, listStr is the string target, listDict is a dict mapping titles to strings
    def ListToStr(self, list, listDict):
        tempStr = ''
        for title in listDict:
            if title in list:
                if tempStr != '':
                    tempStr += ','
                tempStr += listDict[title]
        return tempStr

    def CallAPI(self):
        oddsResponse = requests.get(
            f'https://api.the-odds-api.com//v4/sports/{self.sportKey}/odds/?apiKey={self.apiKey}&regions={self.regions}&markets={self.markets}',
            ).json()
        return pd.json_normalize(oddsResponse)
        
    def ApiErrorCheck(self, df):
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

    def __init__(self, oddsFormat, betSize, timeZone, league, regions, markets, bookmakers, apiKey):
        self.oddsFormat = oddsFormat
        self.betSize = betSize
        self.timeZone = timeZone
        self.sportKey = self.ListToStr(league, self.allLeagues)
        self.regions = self.ListToStr(regions, self.allRegions)
        self.markets = self.ListToStr(markets, self.allMarkets)
        self.bookmakers = bookmakers
        self.apiKey = apiKey