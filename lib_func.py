from dateutil import parser
import datetime
import requests
import pytz
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def convert_timezone(date_time_string):

    if not date_time_string:
        return None

    dt_offset = date_time_string

    if date_time_string.endswith("CEST"):
        dt_offset = date_time_string[:-len("CEST")].strip() + "+02:00"
    elif date_time_string.endswith("CET"):
        dt_offset = date_time_string[:-len("CET")].strip() + "+01:00"
    elif date_time_string.endswith("UTC"):
        dt_offset = date_time_string[:-len("UTC")].strip() + "+00:00"
    elif date_time_string.endswith("+0000"):
        dt_offset = date_time_string[:-len("+0000")].strip() + "+00:00"
    elif date_time_string.endswith(".0000000"):
        dt_offset = date_time_string[:-len(".0000000")].strip() + ".00+00:00"
    return dt_offset


def convert_date(date_time):
    date_time = convert_timezone(date_time)
    parsed = None
    try:
        parsed = parser.parse(date_time)
    except ValueError as e:
        logger.debug('convert_date: {}, {}'.format(date_time, e))
    return parsed


def make_soup(url):
    page = requests.get(url)
    html_doc = page.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


def sort_events_by_time(events):
    def _handle_NoneType(t):
        events_now = datetime.datetime.now(pytz.UTC)
        if not t:
            return events_now - datetime.timedelta(days=100)
        return t
    return sorted(events, key=lambda y: _handle_NoneType(y['time']))


def sort_events_by_sport(events):
    return sorted(events, key=lambda y: y['sport'])


def print_events(events):
    events_list = sort_events_by_sport(sort_events_by_time(events))
    for e in events_list:
        print_event(e)
    print(len(events_list))


def print_event(event):
    print(";".join([str(event.get('time')),
                    event.get('sport', "<no sport>"),
                    event.get('name', "<no name>"),
                    event.get('tournament', "<no tournament>"),
                    event.get('group', "<no group>"),
                    event.get('round', "<no round>"),
                    event.get('points', "<no points>").strip()]))
