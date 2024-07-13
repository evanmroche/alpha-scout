from datetime import datetime
from pytz import timezone

class TimeZone:
    localTimeZone = None

    timeFormat = "%H:%M"
    isoFormat = '%Y-%m-%dT%H:%M:%SZ'

    pacific = timezone('US/Pacific')
    mountain = timezone('US/Mountain')
    central = timezone('US/Central')
    eastern = timezone('US/Eastern')

    timeZoneDict = {'Pacific':pacific, 'Mountain':mountain,
                    'Central':central, 'Eastern':eastern}
    
    def ToLocalTime(self, time):
        timeObj = datetime.strptime(time, self.isoFormat)
        return timeObj.astimezone(self.localTimeZone).strftime('%b %d, %-I:%m %p')
    
    def __init__(self, timeZone):
        self.localTimeZone = self.timeZoneDict[timeZone]