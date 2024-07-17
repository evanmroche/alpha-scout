from alpha_scout import api
import streamlit as st

def decimalToAmerican(decimal):
    if decimal >= 2:
        american = (decimal - 1) * 100
    elif decimal < 2:
        american = -100 / (decimal - 1)
    return round(american)

def findBestH2hOdds(event, team_name, bookmakers) -> api.Bookmaker:
    best_price_bookmaker = None
    best_price = 0
    for bookmaker in event.bookmakers:
        if bookmaker.title in bookmakers:
            for market in bookmaker.markets:
                if market.key == 'h2h':
                    for outcome in market.outcomes:
                        if outcome.name == team_name and outcome.price > best_price:
                            best_price = outcome.price
                            best_price_bookmaker = bookmaker
    return best_price_bookmaker

def findTeamOdds(team_name, market_key, bookmaker: api.Bookmaker):
    for market in bookmaker.markets:
         if market.key == market_key:
             for outcome in market.outcomes:
                 if outcome.name == team_name:
                    return outcome.price

def calculateArbitragePercentage(home_odds, away_odds):
    return round((100 - (((1 / home_odds) * 100) + ((1 / away_odds) * 100))), 2)

class ArbitrageEvent:
    def __init__(self, event : api.Event, bookmakers, market):
        self.event = event
        self.home_bookmaker = findBestH2hOdds(event, event.home_team, bookmakers)
        self.away_bookmaker = findBestH2hOdds(event, event.away_team, bookmakers)
        if (self.home_bookmaker) == None:
            self.home_odds = None
        else:
            self.home_odds = findTeamOdds(event.home_team, market, self.home_bookmaker)
        if self.away_bookmaker == None:
            self.away_odds = None
        else:
            self.away_odds = findTeamOdds(event.away_team, market, self.away_bookmaker)
        if self.away_odds == None or self.home_odds == None:
            self.arbitrage_percentage = None
            self.has_arbitrage = False
            st.error("No arbitrage found!")
        else:
            self.arbitrage_percentage = calculateArbitragePercentage(self.home_odds, self.away_odds)
            self.has_arbitrage = True if self.arbitrage_percentage > 0.25 else False
