from alpha_scout import api
import streamlit as st

def decimalToAmerican(decimal):
    if decimal >= 2:
        american = (decimal - 1) * 100
    elif decimal < 2:
        american = -100 / (decimal - 1)
    return round(american)

class ArbitrageBet:
    def __init__(self, outcome, bookmaker: api.Bookmaker, bet_amount, market_key, price):
        self.outcome = outcome
        self.bookmaker_title = bookmaker.title
        self.market_key = market_key
        self.price = price
        self.bet_amount = bet_amount

class ArbitrageEvent:
    def __init__(self, event : api.Event, chosen_bookmakers, market, bet_amount):
        self.event = event
        self.market = market
        self.chosen_bookmakers = chosen_bookmakers
        self.home_bookmaker = self.findBestBookmaker(event.home_team, market)
        self.away_bookmaker = self.findBestBookmaker(event.away_team, market) 
        self.has_draw = False
        for bookmaker in event.bookmakers:
            # The 0 index used in this line is the index for the h2h market,
            # if using different markets this index must be changed 
            for outcome in bookmaker.markets[0].outcomes:
                if outcome.name == 'Draw':
                    self.has_draw = True
                    self.draw_bookmaker = self.findBestBookmaker('Draw', market)
                    self.draw_odds = self.findTeamOdds('Draw', self.draw_bookmaker)
                        
        self.bet_amount = bet_amount
        self.home_odds = self.findTeamOdds(event.home_team, self.home_bookmaker)
        self.away_odds = self.findTeamOdds(event.away_team, self.away_bookmaker)
        self.inverse_price = self.calculateInversePrice()
        self.arbitrage_percentage = self.calculateArbitragePercentage()
        self.home_bet_amount = self.calculateBetAmounts()['home_bet_amount']
        self.away_bet_amount = self.calculateBetAmounts()['away_bet_amount']
        if self.has_draw:
            self.draw_bet_amount = self.calculateBetAmounts()['draw_bet_amount']
        self.has_arbitrage = True if self.inverse_price < 1 else False
        self.calculateArbitrageProfit()

    def calculateArbitrageProfit(self):
        self.home_win_profit = round((self.home_bet_amount * self.home_odds) - self.bet_amount, 2)
        self.away_win_profit = round((self.away_bet_amount * self.away_odds) - self.bet_amount, 2)
        if self.has_draw:
            self.draw_profit = round((self.draw_bet_amount * self.draw_odds) - self.bet_amount, 2)

    def findBestBookmaker(self, team_name, market_key) -> api.Bookmaker:
        best_price_bookmaker = None
        best_price = 0
        for bookmaker in self.event.bookmakers:
            if bookmaker.title in self.chosen_bookmakers:
                for market in bookmaker.markets:
                    if market.key == market_key: 
                        for outcome in market.outcomes:
                            if outcome.name == team_name and outcome.price > best_price:
                                best_price = outcome.price
                                best_price_bookmaker = bookmaker
        if best_price_bookmaker == None:
            st.error("Failed to find odds from current bookmakers! Please select more bookmakers to see more games!")
            st.stop()
        return best_price_bookmaker

    def findTeamOdds(self, team_name, bookmaker: api.Bookmaker):
        for market in bookmaker.markets:
            if market.key == self.market:
                for outcome in market.outcomes:
                    if outcome.name == team_name:
                        return outcome.price
    
    def calculateInversePrice(self):
        if self.has_draw:
            return (1 / self.home_odds) + (1 / self.away_odds) + (1 / self.draw_odds)
        else:
            return (1 / self.home_odds) + (1 / self.away_odds)

    def calculateArbitragePercentage(self):
        return round((100 / self.inverse_price - 100), 2)

    def calculateBetAmounts(self):
        home_arb_percentage = 1 / self.home_odds * 100
        away_arb_percentage = 1 / self.away_odds * 100
        if self.has_draw:
            draw_arb_percentage = 1 / self.draw_odds * 100
        else:
            draw_arb_percentage = 0
        total_arb_percentage = home_arb_percentage + away_arb_percentage + draw_arb_percentage
        home_bet_amount = round(self.bet_amount * home_arb_percentage / (total_arb_percentage), 2)
        away_bet_amount = round(self.bet_amount * away_arb_percentage / (total_arb_percentage), 2)
        draw_bet_amount = round(self.bet_amount * draw_arb_percentage / (total_arb_percentage), 2)
        return {'home_bet_amount':home_bet_amount, 'away_bet_amount':away_bet_amount, 'draw_bet_amount':draw_bet_amount}