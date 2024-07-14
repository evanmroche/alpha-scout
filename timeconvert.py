from datetime import datetime
from pytz import timezone

class TimeZone:
    timeFormat = "%H:%M"
    isoFormat = '%Y-%m-%dT%H:%M:%SZ'

    allTimeZones = {'Pacific':timezone('US/Pacific'), 'Mountain':timezone('US/Mountain'),
                    'Central':timezone('US/Central'), 'Eastern':timezone('US/Eastern')}
    
    def ToLocalTime(self, time):
        timeObj = datetime.strptime(time, self.isoFormat)
        return timeObj.astimezone(self.localTimeZone).strftime('%b %d, %-I:%m %p')
    
    def __init__(self, timeZone):
        self.localTimeZone = self.allTimeZones[timeZone]