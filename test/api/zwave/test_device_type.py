from datetime import datetime
import json
from test_base import TestBase
from werkzeug.urls import url_encode
from zwayrest.command import init as InitCommand, user as UserCommand
from zwayrest import model, db

class TestDeviceType(TestBase):
    def test_get_list(self):
        # Build ACL
        InitCommand.build_acl()

        # Create client
        client = InitCommand.save_client('Test', 'Py Test Client', 'test')

        # Create user
        user = UserCommand.save_user('admin', 'Admin', 'adminpwd', 'admin@test.test', 'user')
        username = user.username
        fullname = user.fullname
        email = user.email

        # Create token
        expire_time = datetime.now().replace(microsecond=0)
        token = model.auth.bearer_token.BearerToken(client=client, user=user, token_type='bearer', access_token='sBPYJagb6qTEVEmcuf7m8gf9zsD7cX', refresh_token='q7FCvf49E2ucBAuLlDtpKLlAbm7zFD', expires=expire_time, remote_address=None, user_agent='', _scopes='zway')
        db.session.add(token)
        db.session.commit()

        db.session.add(model.zwave.device_type.DeviceType(name='test_device_type', description='Test device type 1'))
        db.session.add(model.zwave.device_type.DeviceType(name='test_device_type_2', description='Test device type 2'))

        # Get device type info
        data = dict(access_token=token.access_token)
        response = self.app.get('/api/v1/zwave/device_types?%s' % url_encode(data))
        device_types_data = self.check_api_response(response)
        assert len(device_types_data['device_types']) == 2
        assert device_types_data['device_types'][0]['name'] == 'test_device_type_2'
        assert device_types_data['device_types'][0]['description'] == 'Test device type 2'
        assert device_types_data['device_types'][1]['name'] == 'test_device_type'
        assert device_types_data['device_types'][1]['description'] == 'Test device type 1'

    def test_get(self):
        # Build ACL
        InitCommand.build_acl()

        # Create client
        client = InitCommand.save_client('Test', 'Py Test Client', 'test')

        # Create user
        user = UserCommand.save_user('admin', 'Admin', 'adminpwd', 'admin@test.test', 'user')
        username = user.username
        fullname = user.fullname
        email = user.email

        # Create token
        expire_time = datetime.now().replace(microsecond=0)
        token = model.auth.bearer_token.BearerToken(client=client, user=user, token_type='bearer', access_token='sBPYJagb6qTEVEmcuf7m8gf9zsD7cX', refresh_token='q7FCvf49E2ucBAuLlDtpKLlAbm7zFD', expires=expire_time, remote_address=None, user_agent='', _scopes='zway')
        db.session.add(token)
        db.session.commit()

        db.session.add(model.zwave.device_type.DeviceType(name='test_device_type', description='Test device type 1'))
        db.session.add(model.zwave.device_type.DeviceType(name='test_device_type_2', description='Test device type 2'))

        device_type = model.zwave.device_type.DeviceType.query.first();

        # Get device type info
        data = dict(access_token=token.access_token)
        response = self.app.get('/api/v1/zwave/device_types/%d?%s' % (device_type.id, url_encode(data)))
        device_types_data = self.check_api_response(response)
        assert device_types_data['device_type']['name'] == device_type.name
        assert device_types_data['device_type']['description'] == device_type.description

    def test_put(self):
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

        db.session.add(model.zwave.device_type.DeviceType(name='test_device_type', description='Test device type 1'))
        db.session.add(model.zwave.device_type.DeviceType(name='test_device_type_2', description='Test device type 2'))

        device_type = model.zwave.device_type.DeviceType.query.first();

        # Get device type info
        data = dict(access_token=token.access_token)
        post_data = dict(name='new_name', description='New description')
        response = self.app.put('/api/v1/zwave/device_types/%d?%s' % (device_type.id, url_encode(data)), data=json.dumps(post_data), content_type='application/json')

        device_types_data = self.check_api_response(response)
        assert device_types_data['device_type']['name'] == post_data['name']
        assert device_types_data['device_type']['description'] == post_data['description']

        device_type = model.zwave.device_type.DeviceType.query.filter_by(id=device_type.id).first();

        assert device_type.name == post_data['name']
        assert device_type.description == post_data['description']
