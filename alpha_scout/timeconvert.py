from datetime import datetime
from pytz import timezone

class TimeZone:
    time_format = "%H:%M"
    iso_format = '%Y-%m-%dT%H:%M:%SZ'

    all_time_zones = {'Pacific':timezone('US/Pacific'), 'Mountain':timezone('US/Mountain'),
                    'Central':timezone('US/Central'), 'Eastern':timezone('US/Eastern')}
    
    def toLocalTime(self, time):
        time_obj = datetime.strptime(time, self.iso_format)
        return time_obj.astimezone(self.local_time_zone).strftime('%b %d, %-I:%m %p')
    
    def __init__(self, time_zone):
        self.local_time_zone = self.all_time_zones[time_zone]