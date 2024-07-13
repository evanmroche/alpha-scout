import requests
import pandas as pd

class ApiRequest:
    regionsDict = {'US':'us', 'US2':'us2', 'UK':'uk', 'EU':'eu'}
    bookmakersDict = {'FanDuel':'fanduel', 'DraftKings':'draftkings', 'BetMGM':'betmgm', 'Caesars':'williamhill_us'}
    marketsDict = {'Moneyline':'h2h', 'Spreads':'spreads', 'Totals':'totals'}
    leaguesDict = {'Upcoming':'upcoming','NBA':'basketball_nba','MLB':'baseball_mlb'}

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

    def __init__(self, oddsFormat, betSize, timeZone, league, regions, markets, bookmakers, apiKey):
        self.oddsFormat = oddsFormat
        self.betSize = betSize
        self.timeZone = timeZone
        self.sportKey = self.ListToStr(league, self.leaguesDict)
        self.regions = self.ListToStr(regions, self.regionsDict)
        self.markets = self.ListToStr(markets, self.marketsDict)
        self.bookmakers = bookmakers
        self.apiKey = apiKey
