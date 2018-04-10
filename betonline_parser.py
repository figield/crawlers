import re
from lib_func import convert_date, make_soup, print_events


def get_provider_name():
    return 'betonline'


def get_events():
    soup = make_soup('https://betonline.net.pl/prognozy')
    events_dict = {}
    for i in xrange(7):
        li_data_sports = soup.find_all(attrs={"data-sport": str(i)})
        for li in li_data_sports:
            sport_url = li.find('img').attrs['src']
            sport_url_clean = re.sub('[/_\.]', ' ', sport_url)
            sport_url_tokens = sport_url_clean.split()
            sport_name = sport_url_tokens[-3]
            event = {'sport': sport_name}
            event_name = li.find('a').attrs['title']
            event['name'] = event_name
            time_tag = li.find('time')
            time = convert_date(time_tag.string + 'CET')  # TODO add TZ
            event['time'] = time
            status = li.find_all('div')
            for div_tag in status:
                div_classes = div_tag.get('class')
                if div_classes and 'status' in div_classes:
                    points = div_tag.string.strip()
                    event['points'] = points

            events_dict[(event['name'], event['time'])] = event

    return events_dict.values()


if __name__ == "__main__":
    print_events(get_events())
