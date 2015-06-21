from zwayrest import db

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

        db.session.commit()
