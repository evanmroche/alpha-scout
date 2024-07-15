class Event:
    BOOKMAKER_INDEX = 0
    NAME_INDEX = 1
    ODDS_INDEX = 2
    FIRST = 0

    H2H_INDEX = 0
    SPREADS_INDEX = 1
    TOTALS_INDEX = 2

    def __init__(self, df):
        self.df = df
        self.sport_key = df['sport_key']
        self.id = df['id']
        self.commence_time = df['commence_time']
        self.sport_title = df['sport_title']
        self.home_team = df['home_team']
        self.away_team = df['away_team']

    