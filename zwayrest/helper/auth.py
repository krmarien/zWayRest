import smtplib
from zwayrest import app, db

class Auth(object):

    @staticmethod
    def login_succeeded(user):
        user.failed_logins = 0
        db.session.commit()

    @staticmethod
    def login_failed(user):
        user.failed_logins += 1

        if user.failed_logins >= 3:
            user.active = False

            Auth.send_deactivation_mail(user)

        db.session.commit()

    @staticmethod
    def send_deactivation_mail(user):
        sender = app.config['SMTP_SENDER']
        to = [user.email]

        message = """\
From: %s
To: %s
Subject: zWay Account deactivated

Dear,

Your account for zWayRest and zWayFront was disabled.
Please contact the system administrator to enable it again.

Regards,
""" % (sender, ", ".join(to))

        try:
            server = smtplib.SMTP(app.config['SMTP_HOST'], app.config['SMTP_PORT'])
            server.sendmail(sender, ", ".join(to), message)
            server.quit()
        except:
            print "Failed to send deactivate mail"
