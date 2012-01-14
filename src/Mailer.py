__author__ = 'ids'

class Mailer:

    def __init__(self, email):
        self.email = email

    def send_alerts(self, last_alerts, current_alerts):

        alerts = []

        for game_name in current_alerts:
            if game_name in last_alerts:
                alerts.extend(self.diff(game_name, last_alerts[game_name], current_alerts[game_name]))
            else:
                alerts.append('Joined game ' + game_name)

        for game_name in last_alerts:
            if game_name not in current_alerts:
                alerts.append('Left game ' + game_name)

        print 'Sending alerts to', self.email

        print alerts

    def diff(self, game_name, last_state, current_state):
        alerts = []

        #phase
        if last_state['phase'] != current_state['phase']:
            alerts.append(game_name + ' has advanced to ' + current_state['phase'])

        #messages
        for country in current_state['messages']:
            if country not in last_state['messages']:
                alerts.append('New message from ' + country + ' in ' + game_name)

        #timeout
        timeout = False
        if current_state['timeout'] and not last_state['timeout']:
            alerts.append('About to miss turn in ' + game_name)
            timeout = True

        #waiting
        if current_state['waiting'] and not last_state['waiting'] and not timeout:
            alerts.append('Waiting for you in ' + game_name)

        return alerts