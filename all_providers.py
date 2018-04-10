import betonline_parser
import sportowefakty
from lib_func import print_events


def get_events_from_all_providers():
    print "Getting data from betonline..."
    all_events = betonline_parser.get_events()
    print "Getting data from sportowefakty..."
    all_events.extend(sportowefakty.get_events())
    return all_events


if __name__ == "__main__":
    print_events(get_events_from_all_providers())
