from datetime import datetime
import json
from test_api_base import TestApiBase
from werkzeug.urls import url_encode
from zwayrest.command import init as InitCommand, user as UserCommand
from zwayrest import model, db

class TestDeviceType(TestApiBase):
    def test_get_list(self):
        user_access_token = self.get_access_token_for_role('user')

        db.session.add(model.zwave.device_type.DeviceType(name='test_device_type', description='Test device type 1'))
        db.session.add(model.zwave.device_type.DeviceType(name='test_device_type_2', description='Test device type 2'))

        # Get device type info
        data = dict(access_token=user_access_token.access_token)
        response = self.app.get('/api/v1/zwave/device_types?%s' % url_encode(data))
        device_types_data = self.check_api_response(response)
        assert len(device_types_data['device_types']) == 2
        assert device_types_data['device_types'][0]['name'] == 'test_device_type_2'
        assert device_types_data['device_types'][0]['description'] == 'Test device type 2'
        assert device_types_data['device_types'][1]['name'] == 'test_device_type'
        assert device_types_data['device_types'][1]['description'] == 'Test device type 1'

    def test_get(self):
        user_access_token = self.get_access_token_for_role('user')

        db.session.add(model.zwave.device_type.DeviceType(name='test_device_type', description='Test device type 1'))
        db.session.add(model.zwave.device_type.DeviceType(name='test_device_type_2', description='Test device type 2'))

        device_type = model.zwave.device_type.DeviceType.query.first();

        # Get device type info
        data = dict(access_token=user_access_token.access_token)
        response = self.app.get('/api/v1/zwave/device_types/%d?%s' % (device_type.id, url_encode(data)))
        device_types_data = self.check_api_response(response)
        assert device_types_data['device_type']['name'] == device_type.name
        assert device_types_data['device_type']['description'] == device_type.description

    def test_put(self):
        user_access_token = self.get_access_token_for_role('admin')

        db.session.add(model.zwave.device_type.DeviceType(name='test_device_type', description='Test device type 1'))
        db.session.add(model.zwave.device_type.DeviceType(name='test_device_type_2', description='Test device type 2'))

        device_type = model.zwave.device_type.DeviceType.query.first();

        # Get device type info
        data = dict(access_token=user_access_token.access_token)
        post_data = dict(name='new_name', description='New description')
        response = self.app.put('/api/v1/zwave/device_types/%d?%s' % (device_type.id, url_encode(data)), data=json.dumps(post_data), content_type='application/json')

        device_types_data = self.check_api_response(response)
        assert device_types_data['device_type']['name'] == post_data['name']
        assert device_types_data['device_type']['description'] == post_data['description']

        device_type = model.zwave.device_type.DeviceType.query.filter_by(id=device_type.id).first();

        assert device_type.name == post_data['name']
        assert device_type.description == post_data['description']
