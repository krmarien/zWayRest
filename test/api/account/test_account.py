from datetime import datetime
import json
from test_base import TestBase
from werkzeug.urls import url_encode
from zwayrest.command import init as InitCommand, user as UserCommand
from zwayrest import model, db

class TestAccount(TestBase):

    def test_get(self):
        # Build ACL
        InitCommand.build_acl()

        # Create client
        client = InitCommand.save_client('Test', 'Py Test Client', 'test')

        # Create user
        user = UserCommand.save_user('admin', 'Admin', 'adminpwd', 'admin@test.test', 'admin')
        username = user.username
        fullname = user.fullname
        email = user.email

        # Create token
        expire_time = datetime.now().replace(microsecond=0)
        token = model.auth.bearer_token.BearerToken(client=client, user=user, token_type='bearer', access_token='sBPYJagb6qTEVEmcuf7m8gf9zsD7cX', refresh_token='q7FCvf49E2ucBAuLlDtpKLlAbm7zFD', expires=expire_time, remote_address=None, user_agent='', _scopes='zway')
        db.session.add(token)
        db.session.commit()

        # Get user info
        data = dict(access_token=token.access_token)
        response = self.app.get('/api/v1/account?%s' % url_encode(data))
        user_data = self.check_api_response(response)
        assert user_data['account']['email'] == email
        assert user_data['account']['username'] == username
        assert user_data['account']['fullname'] == fullname

    def test_put_account(self):
        # Build ACL
        InitCommand.build_acl()

        # Create client
        client = InitCommand.save_client('Test', 'Py Test Client', 'test')

        # Create user
        user = UserCommand.save_user('admin', 'Admin', 'adminpwd', 'admin@test.test', 'admin')
        username = user.username
        email = user.email

        # Create token
        expire_time = datetime.now().replace(microsecond=0)
        token = model.auth.bearer_token.BearerToken(client=client, user=user, token_type='bearer', access_token='sBPYJagb6qTEVEmcuf7m8gf9zsD7cX', refresh_token='q7FCvf49E2ucBAuLlDtpKLlAbm7zFD', expires=expire_time, remote_address=None, user_agent='', _scopes='zway')
        db.session.add(token)
        db.session.commit()

        # Update account info
        data = dict(access_token=token.access_token)
        post_data = dict(fullname='New Name', email='new@email.test')
        response = self.app.put('/api/v1/account?%s' % url_encode(data), data=json.dumps(post_data), content_type='application/json')
        user_data = self.check_api_response(response)
        assert user_data['account']['email'] == 'new@email.test'
        assert user_data['account']['username'] == username
        assert user_data['account']['fullname'] == 'New Name'

    def test_put_password(self):
        # Build ACL
        InitCommand.build_acl()

        # Create client
        client = InitCommand.save_client('Test', 'Py Test Client', 'test')

        # Create user
        user = UserCommand.save_user('admin', 'Admin', 'adminpwd', 'admin@test.test', 'admin')
        username = user.username
        fullname = user.fullname
        email = user.email

        # Create token
        expire_time = datetime.now().replace(microsecond=0)
        token = model.auth.bearer_token.BearerToken(client=client, user=user, token_type='bearer', access_token='sBPYJagb6qTEVEmcuf7m8gf9zsD7cX', refresh_token='q7FCvf49E2ucBAuLlDtpKLlAbm7zFD', expires=expire_time, remote_address=None, user_agent='', _scopes='zway')
        access_token = token.access_token
        db.session.add(token)
        db.session.commit()

        # Update password
        data = dict(access_token=access_token)
        post_data = dict(old_password='adminpwd', new_password='newpwd', password_repeat='newpwd', options='password')
        response = self.app.put('/api/v1/account?%s' % url_encode(data), data=json.dumps(post_data), content_type='application/json')
        user_data = self.check_api_response(response)
        assert user_data['account']['email'] == email
        assert user_data['account']['username'] == username
        assert user_data['account']['fullname'] == fullname

        user = model.auth.user.User.query.first()
        assert user.check_password('newpwd')

        # Try to update with wrong old password
        data = dict(access_token=access_token)
        post_data = dict(old_password='wrongpwd', new_password='newpwd', password_repeat='newpwd', options='password')
        response = self.app.put('/api/v1/account?%s' % url_encode(data), data=json.dumps(post_data), content_type='application/json')
        user_data = self.check_api_response(response, 409)

        user = model.auth.user.User.query.first()
        assert user.check_password('newpwd')

        # Try to update with wrong repeated password
        data = dict(access_token=access_token)
        post_data = dict(old_password='newpwd', new_password='anothernewpwd', password_repeat='wrongnewpwd', options='password')
        response = self.app.put('/api/v1/account?%s' % url_encode(data), data=json.dumps(post_data), content_type='application/json')
        user_data = self.check_api_response(response, 409)

        user = model.auth.user.User.query.first()
        assert user.check_password('newpwd')
