from alpha_scout import api
import streamlit as st

class Arbitrage:
    def __init__(self, event : api.Event):
        self.event = event
    
    @staticmethod
    def decimalToAmerican(decimal):
        if decimal >= 2:
            american = (decimal - 1) * 100
        elif decimal < 2:
            american = -100 / (decimal - 1)
        return round(american)
        
    @staticmethod
    def findTeamOdds(team_name, market_key, bookmaker : api.Bookmaker):
        for market in bookmaker.markets:
            if market.key == market_key:
                for outcome in market.outcomes:
                    if outcome.name == team_name:
                        return outcome.price

    def findBestH2hOdds(self, team_name, bookmakers) -> api.Bookmaker:
        best_price_bookmaker = None
        best_price = 0
        for bookmaker in self.event.bookmakers:
            if bookmaker.title in bookmakers:
                for market in bookmaker.markets:
                    if market.key == 'h2h':
                        for outcome in market.outcomes:
                            if outcome.name == team_name and outcome.price > best_price:
                                best_price = outcome.price
                                best_price_bookmaker = bookmaker
        return best_price_bookmaker
