__author__ = 'ids'
__comments__ = 'LOL my first Python program'

import sys
import urllib
import urllib2
from FileReader import FileReader
from GameParser import GameParser

MY_GAMES_URL = 'http://webdiplomacy.net/gamelistings.php?gamelistType=My%20games&page='

def digest_games(game_list):
    return

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

    parser = GameParser()
    parser.feed(data)

    return parser.games

#Read multiple pages of games?

def main(argv):
    reader = FileReader()

    props = reader.read_properties()
    if not props:
        print('No properties file found')
        return

    games = read_games_page(props['username'], props['password'], 1)

    print games

if __name__ == '__main__':
    sys.exit(main(sys.argv))
