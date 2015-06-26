from datetime import datetime
import json
import re
from test_base import TestBase
from werkzeug.urls import url_encode
from zwayrest import model, db
from zwayrest.command import init as InitCommand, user as UserCommand

class TestAcl(TestBase):

    def check_api_response_allowed(self, response):
        assert response.headers['Content-Type'] == 'application/json'
        assert response.status_code != 401

        return json.loads(response.data)

    def check_api_response_denied(self, response):
        return self.check_api_response(response, 401)

    def test_acl(self):
        # Build ACL
        InitCommand.build_acl()

        # Create client
        client = InitCommand.save_client('Test', 'Py Test Client', 'test')

        for role in InitCommand.roles:
            # Create user
            user = UserCommand.save_user(role, role, 'pwd', '%s@test.test' % role, role)
            username = user.username

            # Request token
            data = dict(grant_type='password', password='pwd', username=username, scope='test', client_id=client.client_id, client_secret=client.client_secret)
            response = self.app.get('/api/v1/auth?%s' % url_encode(data))
            user_token = self.check_api_response(response)
            assert user_token['token_type'] == 'Bearer'
            assert user_token['scope'] == 'test'

            active_roles = self.get_roles(role)

            # Check allowed actions
            for active_role in active_roles:
                for action in InitCommand.roles[active_role]['actions']:
                    print 'Allowed: ' + role + ' - ' + action
                    response = self.get_response(action, user_token['access_token'])
                    self.check_api_response_allowed(response)

            # Check denied actions
            for active_role in InitCommand.roles:
                if active_role in active_roles:
                    continue

                for action in InitCommand.roles[active_role]['actions']:
                    print 'Denied: ' + role + ' - ' + action
                    response = self.get_response(action, user_token['access_token'])
                    self.check_api_response_denied(response)

    def get_roles(self, name):
        if name is None:
            return set([])

        all_roles = set([])
        all_roles.add(name)

        return all_roles | self.get_roles(InitCommand.roles[name]['parent'])

    def get_response(self, resource, access_token):
        url = self.get_url(re.sub(r'(.*)\..*', r'\1', resource), access_token)
        method = re.sub(r'.*\.(.*)', r'\1', resource)

        if method == 'post':
            return self.app.post(url)
        elif method == 'get':
            return self.app.get(url)
        elif method == 'delete':
            return self.app.delete(url)
        elif method == 'put':
            return self.app.put(url)
        else:
            assert 0

    def get_url(self, action, access_token):
        query = {
            'access_token': access_token
        }

        url = ''
        if action == 'account.account':
            url = '/account'
        elif action == 'account.session':
            user = model.auth.user.User.query.first()

            token = model.auth.bearer_token.BearerToken.query.filter_by(user=user).first()

            url = '/account/sessions/%s' % (token.id)
        elif action == 'account.session_list':
            url = '/account/sessions'
        elif action == 'zwave.device':
            db.session.add(model.zwave.device.Device(name='Test Device', description='Test description'))
            db.session.commit()

            device = model.zwave.device.Device.query.first()

            token = model.auth.bearer_token.BearerToken.query.filter_by(access_token=access_token).first()
            token.user.devices = [device]
            db.session.commit()

            url = '/zwave/devices/%d' % (device.id)
        elif action == 'zwave.device_list':
            url = '/zwave/devices'
        elif action == 'zwave.device_list.all':
            query['options'] = 'all'
            url = '/zwave/devices'
        elif action == 'zwave.zway':
            url = '/zwave/zway/test'
        else:
            assert(0)

        return '/api/v1%s?%s' % (url, '&'.join(['%s=%s' % (chunk, query[chunk]) for chunk in query]))
