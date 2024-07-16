from datetime import datetime
import pytz as tz
import streamlit as st
from alpha_scout import options

class TimeZone:
    def __init__(self, time_zone):
        self.local_time_zone = options.all_time_zones[time_zone]

    utc = tz.timezone('UTC')

    time_format = "%H:%M"
    iso_format = '%Y-%m-%dT%H:%M:%SZ'
 
    def toLocalTime(self, time):
        dt_obj = datetime.strptime(time, self.iso_format).replace(tzinfo=tz.utc)

        return dt_obj.astimezone(self.local_time_zone).strftime('%b %d, %-I:%M %p')