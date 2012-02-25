__author__ = 'ids'
__comments__ = 'LOL my first Python program'

import sys
import urllib
import urllib2
from FileReader import FileReader
from GameParser import GameParser
from Mailer import Mailer
from DiffUtil import prepare_alerts

MY_GAMES_URL = 'http://webdiplomacy.net/gamelistings.php?gamelistType=My%20games&page='

class game_status (object):
    def __init__(self, name, stage, messages, about_to_miss, waiting_for_you):
        self.name = name
        self.variant = variant
        self.your_country = your_country
        self.stage = stage
        self.messages = messages
        self.time_left = time_left
        self.about_to_miss = about_to_miss
        self.waiting_for_you = waiting_for_you

def read_games_page(name, password, page_num):
    page_url = MY_GAMES_URL + str(page_num)

    data = urllib2.urlopen(page_url,
        urllib.urlencode({'loginuser': name, 'loginpass': password})).read()

    print 'Read', len(data), 'bytes from ', page_url

    parser = GameParser(name)
    parser.feed(data)

    games = parser.games
    alerts = parser.extract_alert_status(games)

    return alerts

#Read multiple pages of games?

def main(argv):
    reader = FileReader()

    props = reader.read_properties()
    if not props:
        print('No properties file found')
        return

    current_alerts = read_games_page(props['username'], props['password'], 1)
    last_alerts = reader.load_state()
    reader.save_state(current_alerts)

    mailer = Mailer(props['email'], props['smtp_from'], props['smtp_user'], props['smtp_pass'], props['smtp_server'], props['smtp_port'])

    alerts = prepare_alerts(last_alerts, current_alerts)
    mailer.send_alerts(alerts)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
