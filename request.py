import requests

class Request:
    oddsFormat = None
    betSize = None
    timeZone = None
    sportKey = None
    regions = None
    markets = None
    bookmakers = None
    ApiKey = None

    def callAPI(self):
        oddsResponse = requests.get(
            f'https://api.the-odds-api.com//v4/sports/{self.sportKey}/odds/?apiKey={self.ApiKey}&regions={self.regions}&markets={self.markets}',
            )
        return oddsResponse
        
        