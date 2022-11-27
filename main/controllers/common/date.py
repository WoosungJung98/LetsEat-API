from datetime import datetime
from dateutil import parser

DATETIME_PATTERN = "%Y-%m-%d %H:%M:%S"
DATE_PATTERN = "%Y-%m-%d"


def convert_datetime(dt):
  if dt is None:
    return None

  if isinstance(dt, str):
    dt = parser.parse(dt)
  return dt.strftime(DATETIME_PATTERN)


def convert_date(dt):
  if dt is None:
    return None

  if isinstance(dt, str):
    dt = parser.parse(dt).date()
  return dt.strftime(DATE_PATTERN)
