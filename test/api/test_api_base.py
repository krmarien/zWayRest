from datetime import datetime
import random
import string
from test_base import TestBase
from zwayrest import db, model
from zwayrest.command import init as InitCommand, user as UserCommand

class TestApiBase(TestBase):

    def get_access_token_for_role(self, role):
        # Build ACL
        if not hasattr(self, 'has_acl') or not self.has_acl is True:
            InitCommand.build_acl()
            self.has_acl = True

        # Create client
        if not hasattr(self, 'has_client') or not self.has_client is True:
            self.client = InitCommand.save_client('Test', 'Py Test Client', 'test')
            self.has_client = True

        # Create user
        user = UserCommand.save_user(role, role, 'pwd', '%s@test.test' % (role), role)

        # Create token
        expire_time = datetime.now().replace(microsecond=0)
        token = model.auth.bearer_token.BearerToken(client=self.client, user=user, token_type='bearer', access_token=self.get_random_token(), refresh_token=self.get_random_token(), expires=expire_time, remote_address=None, user_agent='', _scopes='zway')
        db.session.add(token)

        db.session.commit()

        return model.auth.bearer_token.BearerToken.query.filter_by(access_token=token.access_token).first()

    def get_random_token(self, length=30):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
