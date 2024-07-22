import pytz as tz

all_leagues = {'Upcoming':'upcoming','NFL':'americanfootball_nfl','NBA':'basketball_nba','MLB':'baseball_mlb'}
all_regions = {'US':'us', 'US2':'us2', 'UK':'uk', 'EU':'eu'}
all_markets = {'Moneyline':'h2h', 'Spreads':'spreads', 'Totals':'totals'}
all_bookmakers = {'FanDuel':'fanduel', 'DraftKings':'draftkings', 'BetMGM':'betmgm', 'Caesars':'williamhill_us',
                  'BetOnline.ag':'betonlineag', 'BetRivers':'betrivers', 'BetUS':'betus', 'MyBookie.ag':'mybookieag',
                  'Bovada':'bovada', 'LowVig.ag':'lowvig', 'Unibet':'unibet_us', 'WynnBET':'wynnbet', 'SI Sportsbook':'sisportsbook'}
odds_formats = ['Decimal', 'American']
all_time_zones = {'Pacific':tz.timezone('US/Pacific'), 'Mountain':tz.timezone('US/Mountain'),
                'Central':tz.timezone('US/Central'), 'Eastern':tz.timezone('US/Eastern')}