BOOKMAKER_INDEX = 0
NAME_INDEX = 1
ODDS_INDEX = 2
FIRST = 0

H2H_INDEX = 0
SPREADS_INDEX = 1
TOTALS_INDEX = 2

class Request:
    oddsFormat = None
    betSize = None
    timeZone = None
    sportKey = None
    regions = None
    markets = None
    bookmakers = None


class Event:
    def __init__(self, data):
        self.data = data
        self.sport_key = data['sport_key']
        self.id = data['id']
        self.commence_time = data['commence_time']
        self.sport_title = data['sport_title']

    def find_market(self, markets_list, market_key):
        for market in markets_list:
            if market.get('key') == market_key:
                return market
        return None

    def find_best_odds(self, market_key):
        # finding the best odds for each outcome in each event
        best_odds = [[None, None, float('-inf')] for _ in range(2)]
        # [Bookmaker, Name, Price]

        bookmakers = self.data['bookmakers']
        for index, bookmaker in enumerate(bookmakers):
            # Debugging
            print(f'Bookmaker: {bookmaker}')
            print(self.find_market(bookmaker['markets'], market_key))

            # Sets current market
            current_market = self.find_market(bookmaker['markets'], market_key)

            print(current_market)

            # Set num_outcomes
            num_outcomes = len(current_market['outcomes'])
            self.num_outcomes = num_outcomes


            # Determine the odds offered by each bookmaker
            for outcome in range(num_outcomes):
                # Ensure the current bookmaker has this outcome index before proceeding
                if outcome < len(current_market['outcomes']):
                    
                    # Determining if any of the bookmaker odds are better than the current best odds
                    bookmaker_odds = float(current_market['outcomes'][outcome]['price'])
                    current_best_odds = best_odds[outcome][ODDS_INDEX]

                    # Edited this if statement to check bookmakers
                    if bookmaker_odds > current_best_odds and bookmaker['key'] in BOOKMAKERS_ALLOWED:
                        best_odds[outcome][BOOKMAKER_INDEX] = bookmaker['title']
                        if current_market['outcomes'][outcome].get('point', 0):
                            best_odds[outcome][NAME_INDEX] = current_market['outcomes'][outcome]['name'] + ' ' + str(bookmaker['markets'][FIRST]['outcomes'][outcome].get('point'))
                        else:
                            best_odds[outcome][NAME_INDEX] = current_market['outcomes'][outcome]['name']

                        best_odds[outcome][ODDS_INDEX] = bookmaker_odds
        
        # # Check that best_odds is not empty
        # if not best_odds[outcome][BOOKMAKER_INDEX]:
        #     print('Error: No best odds found!')
        #     exit()

        self.all_markets_best_odds = [[] for _ in range(3)]
        # Assigns best odds to each index in all_markets_best_odds
        if market_key == 'h2h':
            self.all_markets_best_odds[H2H_INDEX] += best_odds
        elif market_key == 'spreads':
            self.all_markets_best_odds[SPREADS_INDEX] += best_odds
        elif market_key == 'totals':
            self.all_markets_best_odds[TOTALS_INDEX] += best_odds
    
    def arbitrage(self):
        self.total_arbitrage_percentages = []
        self.expected_earnings = []
        for index, market in enumerate(self.all_markets_best_odds):
            total_arbitrage_percentage = 0
            
            for odds in market:
                if index == H2H_INDEX:
                    print(odds[H2H_INDEX])
                    total_arbitrage_percentage += (1.0 / odds[H2H_INDEX][ODDS_INDEX])
                
                print(f'odds: {odds[H2H_INDEX][ODDS_INDEX]}')
                
            market = total_arbitrage_percentage
            if total_arbitrage_percentage != 0:
                market = (BET_SIZE / total_arbitrage_percentage) - BET_SIZE
            else:
                print("Error: total_arbitrage_percentage is zero")
                market = None
           

        # if the sum of the reciprocals of the odds is less than 1, there is opportunity for arbitrage
        for market in self.all_markets_best_odds:
            if market < 1:
                return True
        return False
    
    # converts decimal/European best odds to American best odds
    def convert_decimal_to_american(self):
        best_odds = self.best_odds
        for odds in best_odds:
            decimal = odds[ODDS_INDEX]
            if decimal >= 2:
                american = (decimal - 1) * 100
            elif decimal < 2:
                american = -100 / (decimal - 1)
            odds[ODDS_INDEX] = round(american, 2)
        return best_odds
    

####################################################################################################################################
# Only function not yet reworked 
####################################################################################################################################
    def calculate_arbitrage_bets(self):
        bet_amounts = []
        for outcome in range(self.num_outcomes):
            individual_arbitrage_percentage = 1 / self.best_odds[outcome][ODDS_INDEX]
            bet_amount = (BET_SIZE * individual_arbitrage_percentage) / self.total_arbitrage_percentage
            bet_amounts.append(round(bet_amount, 2))
        
        self.bet_amounts = bet_amounts
        return bet_amounts
    