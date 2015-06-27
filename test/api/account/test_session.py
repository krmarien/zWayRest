from datetime import datetime
import json
from test_base import TestBase
from werkzeug.urls import url_encode
from zwayrest.command import init as InitCommand, user as UserCommand
from zwayrest import model, db

class TestSession(TestBase):

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

        # Create another user
        otheruser = UserCommand.save_user('otheruser', 'Other', 'pwd', 'other@test.test', 'admin')

        # Create token
        expire_time = datetime.now().replace(microsecond=0)
        token = model.auth.bearer_token.BearerToken(client=client, user=user, token_type='bearer', access_token='sBPYJagb6qTEVEmcuf7m8gf9zsD7cX', refresh_token='q7FCvf49E2ucBAuLlDtpKLlAbm7zFD', expires=expire_time, remote_address=None, user_agent='', _scopes='zway')
        access_token = token.access_token
        db.session.add(token)

        # Create another token with more info
        expire_time = datetime.now().replace(microsecond=0)
        last_active = datetime.now().replace(microsecond=0)
        token = model.auth.bearer_token.BearerToken(client=client, user=user, token_type='bearer', access_token='Xqd8px7X6OO2gqc0vhlmJd1oUYaj2X', refresh_token='iRwV7aDH5VCwsvIZvJGWAui9O1wiP1', expires=expire_time, last_active=last_active, remote_address='127.0.0.1', user_agent='Safari', _scopes='zway')
        db.session.add(token)

        # Create a second token of another user
        token = model.auth.bearer_token.BearerToken(client=client, user=otheruser, token_type='bearer', access_token='GyG2o8NquLD6kAI4sbDq9ozwJBdE7I', refresh_token='CmjqpDHq3uQlp8oRJrGg0lvWCLgOgo', expires=expire_time, remote_address=None, user_agent='', _scopes='zway')
        db.session.add(token)

        db.session.commit()

        # Get sessions info
        data = dict(access_token=access_token)
        response = self.app.get('/api/v1/account/sessions?%s' % url_encode(data))
        token_data = self.check_api_response(response)
        assert len(token_data['sessions']) == 2
        assert token_data['sessions'][0]['user']['username'] == username
        assert token_data['sessions'][1]['user']['username'] == username
        assert token_data['sessions'][1]['client']['name'] == 'Test'
        assert token_data['sessions'][1]['remote_address'] == '127.0.0.1'
        assert token_data['sessions'][1]['user_agent'] == 'Safari'
        assert token_data['sessions'][1]['expires'] == expire_time.isoformat() + '+0000'
        assert token_data['sessions'][1]['last_active'] == last_active.isoformat() + '+0000'

    def test_delete(self):
        # Build ACL
        InitCommand.build_acl()

        # Create client
        client = InitCommand.save_client('Test', 'Py Test Client', 'test')

        # Create another user
        user = UserCommand.save_user('admin', 'Admin', 'adminpwd', 'admin@test.test', 'admin')
        username = user.username
        fullname = user.fullname
        email = user.email

        # Create other user
        otheruser = UserCommand.save_user('otheruser', 'Other', 'pwd', 'other@test.test', 'admin')

        # Create token
        expire_time = datetime.now().replace(microsecond=0)
        token = model.auth.bearer_token.BearerToken(client=client, user=user, token_type='bearer', access_token='sBPYJagb6qTEVEmcuf7m8gf9zsD7cX', refresh_token='q7FCvf49E2ucBAuLlDtpKLlAbm7zFD', expires=expire_time, remote_address=None, user_agent='', _scopes='zway')
        access_token = token.access_token
        db.session.add(token)

        # Create a second token to delete
        token = model.auth.bearer_token.BearerToken(client=client, user=user, token_type='bearer', access_token='Xqd8px7X6OO2gqc0vhlmJd1oUYaj2X', refresh_token='iRwV7aDH5VCwsvIZvJGWAui9O1wiP1', expires=expire_time, remote_address=None, user_agent='', _scopes='zway')
        db.session.add(token)
        token_id = model.auth.bearer_token.BearerToken.query.filter_by(user=user, access_token='Xqd8px7X6OO2gqc0vhlmJd1oUYaj2X').first().id

        # Create a second token of another user
        token = model.auth.bearer_token.BearerToken(client=client, user=otheruser, token_type='bearer', access_token='GyG2o8NquLD6kAI4sbDq9ozwJBdE7I', refresh_token='CmjqpDHq3uQlp8oRJrGg0lvWCLgOgo', expires=expire_time, remote_address=None, user_agent='', _scopes='zway')
        db.session.add(token)
        other_token_id = model.auth.bearer_token.BearerToken.query.filter_by(user=otheruser).first().id

        db.session.commit()

        # Check that there are two sessions
        data = dict(access_token=access_token)
        response = self.app.get('/api/v1/account/sessions?%s' % url_encode(data))
        token_data = self.check_api_response(response)
        assert len(token_data['sessions']) == 2

        # Delete session
        data = dict(access_token=access_token)
        response = self.app.delete('/api/v1/account/sessions/%s?%s' % (token_id, url_encode(data)))
        token_data = self.check_api_response(response)
        assert token_data['session']['user']['username'] == username

        # Get sessions info
        data = dict(access_token=access_token)
        response = self.app.get('/api/v1/account/sessions?%s' % url_encode(data))
        token_data = self.check_api_response(response)
        assert len(token_data['sessions']) == 1

        # Try to delete session of another user
        data = dict(access_token=access_token)
        response = self.app.delete('/api/v1/account/sessions/%s?%s' % (other_token_id, url_encode(data)))
        token_data = self.check_api_response(response, 404)
