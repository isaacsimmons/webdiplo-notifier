from HTMLParser import HTMLParser

__author__ = 'ids'

class STATES:
    NONE = 0
    NAME_WAIT = 1
    DATE_WAIT = 2
    PHASE_WAIT = 3
    TURN_DURATION_WAIT = 4
    COUNTRY_NAME_WAIT = 5
    PLAYER_NAME_WAIT = 6


class GameParser(HTMLParser):
    #TODO: check for global messages
    #TODO: don't warn on 5 min games
    #TODO: multiple result pages
    #TODO: support for pre-game values

    ALERT_THRESHOLD = 300 #300s = 5 minutes
    LIVE_TURN_DURATION = '5m'  #Games with 5 min turns are 'Live' and shouldn't generate alerts

    def __init__(self, username, debug = False):
        HTMLParser.__init__(self)
        self.username = username
        self.debug = debug
        self.reset_parse()

    def reset_parse(self):
        self.games = []
        self.state = STATES.NONE
        self.current_country = {}

    def handle_starttag(self, tag, attrs):
        if self.debug:
            print 'start: ', tag, attrs

        if tag == 'div' and len(attrs) == 1 and len(attrs[0]) == 2 and attrs[0][0] == 'class' and attrs[0][1].startswith('gamePanel '):
            self.games.append({})
            self.games[-1]['variant'] = attrs[0][1][10:]
            #TODO: test other variants (or possibly just stop extracting this value)
        if tag == 'span' and len(attrs) == 3 and len(attrs[0]) == 2 and attrs[0][0] == 'class' and attrs[0][1] == 'timeremaining':
            self.games[-1]['time_left'] = int((long(attrs[1][1]) - long(attrs[2][1])) / 60L)
        if tag == 'span' and len(attrs) == 1 and len(attrs[0]) == 2 and attrs[0][0] == 'class' and attrs[0][1] == 'gameName':
            self.state = STATES.NAME_WAIT
        if tag == 'span' and len(attrs) == 1 and len(attrs[0]) == 2 and attrs[0][0] == 'class' and attrs[0][1] == 'gameDate':
            self.state = STATES.DATE_WAIT
        if tag == 'span' and len(attrs) == 1 and len(attrs[0]) == 2 and attrs[0][0] == 'class' and attrs[0][1] == 'gamePhase':
            self.state = STATES.PHASE_WAIT
        if tag == 'span' and len(attrs) == 1 and len(attrs[0]) == 2 and attrs[0][0] == 'class' and attrs[0][1] == 'gameHoursPerPhase':
            self.state = STATES.TURN_DURATION_WAIT
        if tag == 'tr' and len(attrs) == 1 and len(attrs[0]) == 2 and attrs[0][0] == 'class' and attrs[0][1].startswith('member '):
            self.process_country()
        if tag == 'div' and len(attrs) == 1 and len(attrs[0]) == 2 and attrs[0][0] == 'class' and attrs[0][1] == 'enterBarOpen':
            self.process_country()
        if tag == 'span' and len(attrs) == 1 and len(attrs[0]) == 2 and attrs[0][0] == 'class' and attrs[0][1].endswith(' memberStatusPlaying'):
            self.state = STATES.COUNTRY_NAME_WAIT
        if tag == 'span' and len(attrs) == 1 and len(attrs[0]) == 2 and attrs[0][0] == 'class' and attrs[0][1] == 'memberName':
            self.state = STATES.PLAYER_NAME_WAIT
        if tag == 'a' and len(attrs) == 1 and len(attrs[0]) == 2 and attrs[0][0] == 'href' and attrs[0][1].startswith('profile.php?userID=') and self.state == STATES.PLAYER_NAME_WAIT:
            self.current_country['userId'] = attrs[0][1][19:]
        if tag == 'img' and len(attrs) == 3 and len(attrs[1]) == 2 and attrs[1][0] == 'alt':
            if attrs[1][1] == 'Ready':
                self.current_country['status'] = attrs[1][1]
            if attrs[1][1] == 'Not received':
                self.current_country['status'] = attrs[1][1]
            if attrs[1][1] == 'Completed':
                self.current_country['status'] = attrs[1][1]
        if tag == 'img' and len(attrs) == 3 and len(attrs[1]) == 2 and attrs[1][0] == 'alt' and attrs[1][1] == 'Unread message':
            self.current_country['message'] = True

        #get game ID
        #get game link

    def process_country(self):
        if 'countryName' in self.current_country:
            if 'countries' not in self.games[-1]:
                self.games[-1]['countries'] = []
            self.games[-1]['countries'].append(self.current_country)

        self.current_country = {}

    def handle_data(self, data):
        if not data.strip():
            return
        if self.debug:
            print 'data: ', data

        if self.state == STATES.NAME_WAIT:
            self.state = STATES.NONE
            self.games[-1]['name'] = data
        if self.state == STATES.DATE_WAIT:
            self.state = STATES.NONE
            self.games[-1]['date'] = data
        if self.state == STATES.PHASE_WAIT:
            self.state = STATES.NONE
            self.games[-1]['phase'] = data
        if self.state == STATES.TURN_DURATION_WAIT:
            self.state = STATES.NONE
            self.games[-1]['duration'] = data
        if self.state == STATES.COUNTRY_NAME_WAIT:
            self.state = STATES.NONE
            self.current_country['countryName'] = data
        if self.state == STATES.PLAYER_NAME_WAIT:
            self.state = STATES.NONE
            self.current_country['playerName'] = data

    def extract_alert_status(self, games):
        alerts = {}

        for game in games:
            if 'name' not in game:
                print 'Game entry with no name'
                continue

            if game['duration'] == self.LIVE_TURN_DURATION:
                #no alerts for live games
                continue

            game_alerts = {}

            own_status = None
            num_ready = 0
            messages = []

            for country in game['countries']:
                if country['status'] == 'Ready':
                    num_ready += 1
                if country['playerName'] == self.username:
                    own_status = country['status']
                if 'message' in country:
                    messages.append(country['countryName'])

            #messages
            game_alerts['messages'] = messages

            #phase
            game_alerts['phase'] = game['date'] + ' ' + game['phase']

            #waiting for you
            game_alerts['waiting'] = own_status != 'Ready' and num_ready >= (len(games) - 1)

            #about to miss turn
            game_alerts['timeout'] = game['time_left'] < self.ALERT_THRESHOLD and own_status != 'Ready'

            alerts[game['name']] = game_alerts

        return alerts