from datetime import datetime
import json
from test_api_base import TestApiBase
from werkzeug.urls import url_encode
from zwayrest.command import init as InitCommand, user as UserCommand
from zwayrest import model, db

class TestSession(TestApiBase):

    def test_get(self):
        admin_access_token = self.get_access_token_for_role('admin')
        other_access_token = self.get_access_token_for_role('user')

        # Create another token with more info
        expire_time = datetime.now().replace(microsecond=0)
        last_active = datetime.now().replace(microsecond=0)
        token = model.auth.bearer_token.BearerToken(client=self.client, user=admin_access_token.user, token_type='bearer', access_token='Xqd8px7X6OO2gqc0vhlmJd1oUYaj2X', refresh_token='iRwV7aDH5VCwsvIZvJGWAui9O1wiP1', expires=expire_time, last_active=last_active, remote_address='127.0.0.1', user_agent='Safari', _scopes='zway')
        db.session.add(token)

        db.session.commit()

        # Get sessions info
        data = dict(access_token=admin_access_token.access_token)
        response = self.app.get('/api/v1/account/sessions?%s' % url_encode(data))
        token_data = self.check_api_response(response)
        assert len(token_data['sessions']) == 2
        assert token_data['sessions'][0]['user']['username'] == admin_access_token.user.username
        assert token_data['sessions'][1]['user']['username'] == admin_access_token.user.username
        assert token_data['sessions'][1]['client']['name'] == 'Test'
        assert token_data['sessions'][1]['remote_address'] == '127.0.0.1'
        assert token_data['sessions'][1]['user_agent'] == 'Safari'
        assert token_data['sessions'][1]['expires'] == expire_time.isoformat() + '+0000'
        assert token_data['sessions'][1]['last_active'] == last_active.isoformat() + '+0000'

    def test_delete(self):
        admin_access_token = self.get_access_token_for_role('admin')
        other_access_token = self.get_access_token_for_role('user')

        # Create a second token to delete
        expire_time = datetime.now().replace(microsecond=0)
        token = model.auth.bearer_token.BearerToken(client=self.client, user=admin_access_token.user, token_type='bearer', access_token='Xqd8px7X6OO2gqc0vhlmJd1oUYaj2X', refresh_token='iRwV7aDH5VCwsvIZvJGWAui9O1wiP1', expires=expire_time, remote_address=None, user_agent='', _scopes='zway')
        db.session.add(token)
        token = model.auth.bearer_token.BearerToken.query.filter_by(user=admin_access_token.user, access_token='Xqd8px7X6OO2gqc0vhlmJd1oUYaj2X').first()

        db.session.commit()

        # Check that there are two sessions
        data = dict(access_token=admin_access_token.access_token)
        response = self.app.get('/api/v1/account/sessions?%s' % url_encode(data))
        token_data = self.check_api_response(response)
        assert len(token_data['sessions']) == 2

        # Delete session
        data = dict(access_token=admin_access_token.access_token)
        response = self.app.delete('/api/v1/account/sessions/%s?%s' % (token.id, url_encode(data)))
        token_data = self.check_api_response(response)
        assert token_data['session']['user']['username'] == admin_access_token.user.username

        # Get sessions info
        data = dict(access_token=admin_access_token.access_token)
        response = self.app.get('/api/v1/account/sessions?%s' % url_encode(data))
        token_data = self.check_api_response(response)
        assert len(token_data['sessions']) == 1

        # Try to delete session of another user
        data = dict(access_token=admin_access_token.access_token)
        response = self.app.delete('/api/v1/account/sessions/%s?%s' % (other_access_token.id, url_encode(data)))
        token_data = self.check_api_response(response, 404)
