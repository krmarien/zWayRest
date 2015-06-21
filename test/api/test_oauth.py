from werkzeug.urls import url_encode
from test_base import TestBase
from zwayrest import model
from zwayrest.command import init as InitCommand, user as UserCommand

class TestApiOAuth(TestBase):

    def test_grant_type_password(self):
        # Build ACL
        InitCommand.build_acl()

        # Create client
        client = InitCommand.save_client('Test', 'Py Test Client', 'test')

        # Create user
        user = UserCommand.save_user('admin', 'Admin', 'adminpwd', 'admin@test.test', 'admin')
        username = user.username
        email = user.email

        # Request token
        data = dict(grant_type='password', password='adminpwd', username=user.username, scope='test', client_id=client.client_id, client_secret=client.client_secret)
        response = self.app.get('/api/v1/auth?%s' % url_encode(data))
        token_data = self.check_api_response(response)
        assert token_data['token_type'] == 'Bearer'
        assert token_data['scope'] == 'test'

        # Get user info
        data = dict(access_token=token_data['access_token'])
        response = self.app.get('/api/v1/account?%s' % url_encode(data))
        user_data = self.check_api_response(response)
        assert user_data['account']['email'] == email
        assert user_data['account']['username'] == username

    def test_grant_type_password_max_tries(self):
        # Build ACL
        InitCommand.build_acl()

        # Create client
        client = InitCommand.save_client('Test', 'Py Test Client', 'test')
        client_id = client.client_id
        client_secret = client.client_secret

        # Create user
        user = UserCommand.save_user('admin', 'Admin', 'adminpwd', 'admin@test.test', 'admin')
        username = user.username
        email = user.email

        # Login try 1
        data = dict(grant_type='password', password='wrong', username=user.username, scope='test', client_id=client_id, client_secret=client_secret)
        response = self.app.get('/api/v1/auth?%s' % url_encode(data))
        token_data = self.check_api_response(response, 401)

        user = model.auth.user.User.query.first()
        assert user.failed_logins == 1

        # Login try 2
        data = dict(grant_type='password', password='wrong', username=user.username, scope='test', client_id=client_id, client_secret=client_secret)
        response = self.app.get('/api/v1/auth?%s' % url_encode(data))
        token_data = self.check_api_response(response, 401)

        user = model.auth.user.User.query.first()
        assert user.failed_logins == 2

        # Login try 3
        data = dict(grant_type='password', password='wrong', username=user.username, scope='test', client_id=client_id, client_secret=client_secret)
        response = self.app.get('/api/v1/auth?%s' % url_encode(data))
        token_data = self.check_api_response(response, 401)

        user = model.auth.user.User.query.first()
        assert user.failed_logins == 3
        assert user.active == 0

        # Login try 3
        data = dict(grant_type='password', password='adminpwd', username=user.username, scope='test', client_id=client_id, client_secret=client_secret)
        response = self.app.get('/api/v1/auth?%s' % url_encode(data))
        token_data = self.check_api_response(response, 401)

        user = model.auth.user.User.query.first()
        assert user.failed_logins == 3
        assert user.active == 0

    def test_grant_type_password_multiple_tries(self):
        # Build ACL
        InitCommand.build_acl()

        # Create client
        client = InitCommand.save_client('Test', 'Py Test Client', 'test')
        client_id = client.client_id
        client_secret = client.client_secret

        # Create user
        user = UserCommand.save_user('admin', 'Admin', 'adminpwd', 'admin@test.test', 'admin')
        username = user.username
        email = user.email

        # Login try 1
        data = dict(grant_type='password', password='wrong', username=user.username, scope='test', client_id=client_id, client_secret=client_secret)
        response = self.app.get('/api/v1/auth?%s' % url_encode(data))
        token_data = self.check_api_response(response, 401)

        user = model.auth.user.User.query.first()
        assert user.failed_logins == 1

        # Login try 2
        data = dict(grant_type='password', password='wrong', username=user.username, scope='test', client_id=client_id, client_secret=client_secret)
        response = self.app.get('/api/v1/auth?%s' % url_encode(data))
        token_data = self.check_api_response(response, 401)

        user = model.auth.user.User.query.first()
        assert user.failed_logins == 2

        # Login try 3
        data = dict(grant_type='password', password='adminpwd', username=user.username, scope='test', client_id=client_id, client_secret=client_secret)
        response = self.app.get('/api/v1/auth?%s' % url_encode(data))
        token_data = self.check_api_response(response, 200)

        user = model.auth.user.User.query.first()
        assert user.failed_logins == 0
        assert user.active == True
