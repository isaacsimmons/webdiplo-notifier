__author__ = 'ids'

import smtplib
from email.mime.text import MIMEText

class Mailer:

    def __init__(self, recipients, sender, smtp_username, smtp_password, smtp_server, smtp_port):
        self.recipients = recipients.split(';')
        self.send_address = sender
        self.username = smtp_username
        self.password = smtp_password
        self.server = smtp_server
        self.port = smtp_port

    def send_alerts(self, alerts):
        if not alerts:
            return

        body = '\n'.join(alerts)
        msg = MIMEText(body)

        msg['Subject'] = 'Diplomacy Alerts'
        msg['From'] = self.send_address
        msg['To'] = ', '.join(self.recipients)

        print msg.as_string()

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        print 'Sending mail to', self.recipients

        smtp = smtplib.SMTP(self.server, self.port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self.username, self.password)
        smtp.sendmail(self.send_address, self.recipients, msg.as_string())
        smtp.quit()

    def prepare_alerts(self, last_alerts, current_alerts):

        alerts = []

        for game_name in current_alerts:
            if game_name in last_alerts:
                alerts.extend(self.diff(game_name, last_alerts[game_name], current_alerts[game_name]))

        for game_name in last_alerts:
            if game_name not in current_alerts:
                alerts.append('Left game ' + game_name)

        return alerts

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