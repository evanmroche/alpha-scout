from alpha_scout import api
import streamlit as st

def decimalToAmerican(decimal):
    if decimal >= 2:
        american = (decimal - 1) * 100
    elif decimal < 2:
        american = -100 / (decimal - 1)
    return round(american)

class ArbitrageEvent:
    def __init__(self, event : api.Event, chosen_bookmakers, market, bet_amount):
        self.event = event
        self.chosen_bookmakers = chosen_bookmakers
        self.home_bookmaker = self.findBestH2hBookmaker(event.home_team)
        self.away_bookmaker = self.findBestH2hBookmaker(event.away_team)
        self.market = market
        self.bet_amount = bet_amount
        if (self.home_bookmaker) == None:
            self.home_odds = None
        else:
            self.home_odds = self.findTeamOdds(event.home_team, self.home_bookmaker)
        if self.away_bookmaker == None:
            self.away_odds = None
        else:
            self.away_odds = self.findTeamOdds(event.away_team, self.away_bookmaker)
        if self.away_odds == None or self.home_odds == None:
            self.arbitrage_percentage = None
            self.has_arbitrage = False
            st.error("No arbitrage found!")
        else:
            self.inverse_price = self.calculateInversePrice()
            self.arbitrage_percentage = self.calculateArbitragePercentage()
            self.home_bet_amount = self.calculateBetAmounts()['home_bet_amount']
            self.away_bet_amount = self.calculateBetAmounts()['away_bet_amount']
            self.has_arbitrage = True if self.inverse_price < 1 else False
            self.calculateArbitrageProfit()

    def calculateArbitrageProfit(self):
        self.home_win_profit = round((self.home_bet_amount * self.home_odds) - self.bet_amount, 2)
        self.away_win_profit = round((self.away_bet_amount * self.away_odds) - self.bet_amount, 2)

    def findBestH2hBookmaker(self, team_name) -> api.Bookmaker:
        best_price_bookmaker = None
        best_price = 0
        for bookmaker in self.event.bookmakers:
            if bookmaker.title in self.chosen_bookmakers:
                for market in bookmaker.markets:
                    if market.key == 'h2h':
                        for outcome in market.outcomes:
                            if outcome.name == team_name and outcome.price > best_price:
                                best_price = outcome.price
                                best_price_bookmaker = bookmaker
        return best_price_bookmaker

    def findTeamOdds(self, team_name, bookmaker: api.Bookmaker):
        for market in bookmaker.markets:
            if market.key == self.market:
                for outcome in market.outcomes:
                    if outcome.name == team_name:
                        return outcome.price
    
    def calculateInversePrice(self):
        return (1 / self.home_odds) + (1 / self.away_odds)

    def calculateArbitragePercentage(self):
        return round((100 / self.inverse_price - 100), 2)

    def calculateBetAmounts(self):
        home_arb_percentage = 1 / self.home_odds * 100
        away_arb_percentage = 1 / self.away_odds * 100
        total_arb_percentage = home_arb_percentage + away_arb_percentage
        home_bet_amount = round(self.bet_amount * home_arb_percentage / (total_arb_percentage), 2)
        away_bet_amount = round(self.bet_amount * away_arb_percentage / (total_arb_percentage), 2)
        return {'home_bet_amount':home_bet_amount, 'away_bet_amount':away_bet_amount}