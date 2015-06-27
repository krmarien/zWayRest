from datetime import datetime
import json
from test_api_base import TestApiBase
from werkzeug.urls import url_encode
from zwayrest.command import init as InitCommand, user as UserCommand
from zwayrest import model, db

class TestDevice(TestApiBase):
    def test_get_list(self):
        user_access_token = self.get_access_token_for_role('user')
        admin_access_token = self.get_access_token_for_role('admin')

        device_1 = model.zwave.device.Device(zway_id=5, name='test_device', description='Test device 1')
        db.session.add(device_1)
        device_2 = model.zwave.device.Device(zway_id=3, name='test_device_2', description='Test device 2')
        db.session.add(device_2)

        user_access_token.user.devices = [device_1]

        command_group = model.zwave.command_group.CommandGroup(name='test_group', description='Test instance')
        db.session.add(command_group)

        instance = model.zwave.instance.Instance(name='test_instance', description='Test instance', device=device_1, command_groups=[command_group])
        db.session.add(instance)

        db.session.commit()

        # Get device info
        data = dict(access_token=user_access_token.access_token)
        response = self.app.get('/api/v1/zwave/devices?%s' % url_encode(data))
        devices_data = self.check_api_response(response)
        assert len(devices_data['devices']) == 1
        assert devices_data['devices'][0]['zway_id'] == 5
        assert devices_data['devices'][0]['name'] == 'test_device'
        assert devices_data['devices'][0]['description'] == 'Test device 1'

        data = dict(access_token=admin_access_token.access_token, options='all')
        response = self.app.get('/api/v1/zwave/devices?%s' % url_encode(data))
        devices_data = self.check_api_response(response)
        assert len(devices_data['devices']) == 2

        data = dict(access_token=user_access_token.access_token, options='all')
        response = self.app.get('/api/v1/zwave/devices?%s' % url_encode(data))
        self.check_api_response(response, 401)

        # Get device info with instances
        data = dict(access_token=user_access_token.access_token, embed='instances')
        response = self.app.get('/api/v1/zwave/devices?%s' % url_encode(data))
        devices_data = self.check_api_response(response)
        assert len(devices_data['devices']) == 1
        assert devices_data['devices'][0]['zway_id'] == 5
        assert devices_data['devices'][0]['name'] == 'test_device'
        assert devices_data['devices'][0]['description'] == 'Test device 1'
        assert len(devices_data['devices'][0]['instances']) == 1
        assert devices_data['devices'][0]['instances'][0]['name'] == 'test_instance'

        # Get device info with instances and command groups
        data = dict(access_token=user_access_token.access_token, embed='instances, command_groups')
        response = self.app.get('/api/v1/zwave/devices?%s' % url_encode(data))
        devices_data = self.check_api_response(response)
        assert len(devices_data['devices']) == 1
        assert devices_data['devices'][0]['zway_id'] == 5
        assert devices_data['devices'][0]['name'] == 'test_device'
        assert devices_data['devices'][0]['description'] == 'Test device 1'
        assert len(devices_data['devices'][0]['instances']) == 1
        assert devices_data['devices'][0]['instances'][0]['name'] == 'test_instance'
        assert len(devices_data['devices'][0]['instances'][0]['command_groups']) == 1

    def test_get(self):
        user_access_token = self.get_access_token_for_role('user')
        admin_access_token = self.get_access_token_for_role('admin')

        device_1 = model.zwave.device.Device(zway_id=5, name='test_device', description='Test device 1')
        db.session.add(device_1)
        device_1 = model.zwave.device.Device.query.filter_by(zway_id=5).first()
        device_1_id = device_1.id
        device_2 = model.zwave.device.Device(zway_id=3, name='test_device_2', description='Test device 2')
        db.session.add(device_2)
        device_2 = model.zwave.device.Device.query.filter_by(zway_id=3).first()
        device_2_id = device_2.id

        user_access_token.user.devices = [device_1]

        db.session.commit()

        # Get device info
        data = dict(access_token=user_access_token.access_token)
        response = self.app.get('/api/v1/zwave/devices/%d?%s' % (device_1_id, url_encode(data)))
        devices_data = self.check_api_response(response)
        assert devices_data['device']['zway_id'] == 5
        assert devices_data['device']['name'] == 'test_device'
        assert devices_data['device']['description'] == 'Test device 1'

        response = self.app.get('/api/v1/zwave/devices/%d?%s' % (device_2_id, url_encode(data)))
        self.check_api_response(response, 404)

        data = dict(access_token=admin_access_token.access_token)
        response = self.app.get('/api/v1/zwave/devices/%d?%s' % (device_2_id, url_encode(data)))
        devices_data = self.check_api_response(response)
        assert devices_data['device']['zway_id'] == 3
        assert devices_data['device']['name'] == 'test_device_2'
        assert devices_data['device']['description'] == 'Test device 2'

    def test_put(self):
        user_access_token = self.get_access_token_for_role('user')
        admin_access_token = self.get_access_token_for_role('admin')

        device_1 = model.zwave.device.Device(zway_id=5, name='test_device', description='Test device 1')
        db.session.add(device_1)
        device_1 = model.zwave.device.Device.query.filter_by(zway_id=5).first()
        device_1_id = device_1.id
        device_2 = model.zwave.device.Device(zway_id=3, name='test_device_2', description='Test device 2')
        db.session.add(device_2)
        device_2 = model.zwave.device.Device.query.filter_by(zway_id=3).first()
        device_2_id = device_2.id

        user_access_token.user.devices = [device_1]

        db.session.add(model.zwave.device_type.DeviceType(name='test_device_type', description='Test device type 1'))
        device_type = model.zwave.device_type.DeviceType.query.first()

        db.session.commit()

        # Update device info
        data = dict(access_token=admin_access_token.access_token)
        post_data = dict(name='new_name', description='new_description', device_type=device_type.id)
        response = self.app.put('/api/v1/zwave/devices/%d?%s' % (device_1_id, url_encode(data)), data=json.dumps(post_data), content_type='application/json')
        devices_data = self.check_api_response(response)
        assert devices_data['device']['zway_id'] == 5
        assert devices_data['device']['name'] == post_data['name']
        assert devices_data['device']['description'] == post_data['description']
        assert devices_data['device']['device_type']['id'] == post_data['device_type']

        device_1 = model.zwave.device.Device.query.filter_by(zway_id=5).first()
        assert device_1.name == post_data['name']
        assert device_1.description == post_data['description']
        assert device_1.device_type.id == post_data['device_type']
