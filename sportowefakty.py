import datetime
from lib_func import make_soup, convert_date, print_events


def get_provider_name():
    return 'sportowefakty'


def get_events():
    sports = {"football": "pilka-nozna"}
    events_now = datetime.datetime.now()
    days_range = range(-1, 31)  # 4 days
    events_dict = {}
    for i in days_range:
        events_time = events_now + datetime.timedelta(days=i)
        year = str(events_time.year)
        month = str(events_time.month)
        day = str(events_time.day)
        url = 'http://sportowefakty.wp.pl/' + sports['football'] + '/kalendarz/' + year + '/' + month + '/' + day
        soup = make_soup(url)
        section = soup.find(attrs={"class": "chrono_table"})
        if section and section.table and section.table.tbody:
            for tr in section.table.tbody.find_all('tr'):
                event = {'sport': 'football'}
                for td in tr.find_all('td'):
                    td_class = td.get('class')
                    if 'title' in td_class:
                        event['name'] = td.a.string
                        for a in td.span.find_all('a'):
                            if not event.get('tournament'):
                                event['tournament'] = a.string
                            else:
                                event['queue'] = a.string
                    elif 'points' in td_class:
                        if td.a:
                            event['points'] = td.a.string
                        else:
                            event['points'] = td.string
                        event['time'] = None
                    elif 'score' in td_class:
                        event['time'] = convert_date(td.time.get('datetime'))

                events_dict[(event['name'], event['time'])] = event
        else:
            grouped_table = soup.find(attrs={"id": "grouped_table"})
            if grouped_table:
                for tbody in grouped_table.find_all('tbody'):
                    queue = ""
                    for tr in tbody.find_all('tr'):
                        if tr.get('class'):
                            for td in tr.find_all('td'):
                                if td.get('colspan'):
                                    queue = td.string
                        else:
                            event = {'round': queue, 'sport': 'football'}
                            for td in tr.find_all('td'):
                                td_class = td.get('class')
                                if 'date' in td_class:
                                    event['time'] = convert_date(td.time.get('datetime'))
                                elif 'title' in td_class:
                                    for tag in td:
                                        if tag.name == "span":
                                            event['group'] = tag.string
                                        elif tag.name == "a":
                                            event['name'] = tag.string
                                elif 'points' in td_class:
                                    if td.a:
                                        event['points'] = td.a.string
                                    else:
                                        event['points'] = td.string

                            events_dict[(event['name'], event['time'])] = event

    return events_dict.values()


if __name__ == "__main__":
    print_events(get_events())
