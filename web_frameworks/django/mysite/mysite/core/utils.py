import pytz
from django.utils import dateparse
from django.conf import settings


class Utils(object):

    @staticmethod
    def parse_datetime(datetime_str):
        return pytz.timezone(settings.TIME_ZONE).localize(
            dateparse.parse_datetime(datetime_str.strip()), is_dst=None)
