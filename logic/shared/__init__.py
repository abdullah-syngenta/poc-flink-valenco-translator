import calendar

import dateutil
from pytz import tzinfo


class Shared:
    def convert_to_timezone(self, date_time, tz: tzinfo):
        return date_time.astimezone(tz)

    def convert_to_unix_timestamp_milliseconds(self, date_time):
        return int(calendar.timegm(date_time.utctimetuple()) * 1000)

    def get_tz(self, tz_offset):
        tz = dateutil.tz.tzoffset('', float(tz_offset) * 60 * 60)
        return tz
