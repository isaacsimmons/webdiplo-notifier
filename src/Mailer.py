__author__ = 'ids'

class Mailer:

    def __init__(self, email):
        self.email = email

    def send_alerts(self, last_alerts, current_alerts):

        alerts = []

        for gameName in current_alerts:
            if gameName in last_alerts:
                alerts.extend(self.diff(last_alerts[gameName], current_alerts[gameName]))
            else:
                alerts.append('Joined game ' + gameName)

        for gameName in last_alerts:
            if gameName not in current_alerts:
                alerts.append('Left game ' + gameName)


        print 'Sending alerts to', self.email
#        print last_alerts
#        print current_alerts

        print alerts

    def diff(self, last_state, current_state):
        alerts = []

        return alerts