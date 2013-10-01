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

        print(msg.as_string())

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        print('Sending mail to', self.recipients)

        smtp = smtplib.SMTP(self.server, self.port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self.username, self.password)
        smtp.sendmail(self.send_address, self.recipients, msg.as_string())
        smtp.quit()
