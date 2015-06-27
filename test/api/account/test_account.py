from datetime import datetime
import json
from test_api_base import TestApiBase
from werkzeug.urls import url_encode
from zwayrest.command import init as InitCommand, user as UserCommand
from zwayrest import model, db

class TestAccount(TestApiBase):

    def test_get(self):
        admin_access_token = self.get_access_token_for_role('admin')

        # Get user info
        data = dict(access_token=admin_access_token.access_token)
        response = self.app.get('/api/v1/account?%s' % url_encode(data))
        user_data = self.check_api_response(response)
        assert user_data['account']['email'] == admin_access_token.user.email
        assert user_data['account']['username'] == admin_access_token.user.username
        assert user_data['account']['fullname'] == admin_access_token.user.fullname

    def test_put_account(self):
        admin_access_token = self.get_access_token_for_role('admin')

        # Update account info
        data = dict(access_token=admin_access_token.access_token)
        post_data = dict(fullname='New Name', email='new@email.test')
        response = self.app.put('/api/v1/account?%s' % url_encode(data), data=json.dumps(post_data), content_type='application/json')
        user_data = self.check_api_response(response)
        assert user_data['account']['email'] == 'new@email.test'
        assert user_data['account']['username'] == admin_access_token.user.username
        assert user_data['account']['fullname'] == 'New Name'

    def test_put_password(self):
        admin_access_token = self.get_access_token_for_role('admin')

        # Update password
        data = dict(access_token=admin_access_token.access_token)
        post_data = dict(old_password='pwd', new_password='newpwd', password_repeat='newpwd', options='password')
        response = self.app.put('/api/v1/account?%s' % url_encode(data), data=json.dumps(post_data), content_type='application/json')
        user_data = self.check_api_response(response)
        assert user_data['account']['email'] == admin_access_token.user.email
        assert user_data['account']['username'] == admin_access_token.user.username
        assert user_data['account']['fullname'] == admin_access_token.user.fullname

        user = model.auth.user.User.query.first()
        assert user.check_password('newpwd')

        # Try to update with wrong old password
        data = dict(access_token=admin_access_token.access_token)
        post_data = dict(old_password='wrongpwd', new_password='newpwd', password_repeat='newpwd', options='password')
        response = self.app.put('/api/v1/account?%s' % url_encode(data), data=json.dumps(post_data), content_type='application/json')
        user_data = self.check_api_response(response, 409)

        user = model.auth.user.User.query.first()
        assert user.check_password('newpwd')

        # Try to update with wrong repeated password
        data = dict(access_token=admin_access_token.access_token)
        post_data = dict(old_password='newpwd', new_password='anothernewpwd', password_repeat='wrongnewpwd', options='password')
        response = self.app.put('/api/v1/account?%s' % url_encode(data), data=json.dumps(post_data), content_type='application/json')
        user_data = self.check_api_response(response, 409)

        user = model.auth.user.User.query.first()
        assert user.check_password('newpwd')
