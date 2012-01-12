__author__ = 'ids'


import urllib
import urllib2
from HTMLParser import HTMLParser

print "hi"

my_games_url = 'http://webdiplomacy.net/gamelistings.php?gamelistType=My%20games&page='


def read_properties():
    prop_file = file('user.properties')
    props = {}
    for prop_line in prop_file:
        prop_def= prop_line.strip()
        if not len(prop_def):
            continue
        if prop_def[0] in ( '!', '#' ):
            continue
        punctuation= [ prop_def.find(c) for c in ':= ' ] + [ len(prop_def) ]
        found= min( [ pos for pos in punctuation if pos != -1 ] )
        name= prop_def[:found].rstrip()
        value= prop_def[found:].lstrip(":= ").rstrip()
        props[name]= value
    prop_file.close()
    return props

props = read_properties()

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


def readGame(div):
    game_status = {}

    #not-yet-started

    return game_status


class STATES:
    NONE = 0
    NAME_WAIT = 1


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.games = []
        self.state = None

    def handle_starttag(self, tag, attrs):
        print 'start: ', tag, attrs
        if tag == 'div' and len(attrs) == 1 and len(attrs[0]) == 2 and attrs[0][0] == 'class' and attrs[0][1].startswith('gamePanel '):
            self.games.append({})
            self.games[-1]['variant'] = attrs[0][1][10:]
            #TODO: test other variants (or possibly just stop extracting this value)
        if tag == 'span' and len(attrs) == 3 and len(attrs[0]) == 2 and attrs[0][0] == 'class' and attrs[0][1] == 'timeremaining':
            self.games[-1]['time_left'] = int((long(attrs[1][1]) - long(attrs[2][1])) / 60L)
        if tag == 'span' and len(attrs) == 1 and len(attrs[0]) == 2 and attrs[0][0] == 'class' and attrs[0][1] == 'gameName':
            self.state = STATES.NAME_WAIT

        #    def handle_endtag(self, tag):
#        return tag
#        print 'end: ', tag
    def handle_data(self, data):
        if self.state == STATES.NAME_WAIT:
            self.state = STATES.NONE
            self.games[-1]['name'] = data
#        return data
        print 'data: ', data

def read_games_page(name, password, page):
#    html = urllib2.urlopen('http://webdiplomacy.net/index.php',
#        urllib.urlencode({'loginuser': user, 'loginpass': pwd})).read()
    data = urllib2.urlopen(my_games_url + str(page),
        urllib.urlencode({'loginuser': name, 'loginpass': password})).read()
#    print data
    parser = MyHTMLParser()
    parser.feed(data)

    print parser.games


    #(<html><head>)<title>Error - webDiplomacy</title>


read_games_page(props['username'], props['password'], 1)

#<span class="gameDate">Autumn, 1901</span>, <span class="gamePhase">Builds</span>

#<div class="titleBarRightSide">
#<span class="gameTimeRemaining"><span class="gameTimeRemainingNextPhase">Next:</span> <span class="timeremaining" unixtime="1326426531" unixtimefrom="1326393816">9 hours, 5 minutes</span> (<span class="timestamp" unixtime="1326426531">03:48 AM UTC</span>)</span>
#</div>



