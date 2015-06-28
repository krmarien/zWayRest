from datetime import datetime
import json
from test_api_base import TestApiBase
from werkzeug.urls import url_encode
from zwayrest.command import init as InitCommand, user as UserCommand
from zwayrest import model, db

class TestInstance(TestApiBase):
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

        # Get instance info
        data = dict(access_token=user_access_token.access_token)
        response = self.app.get('/api/v1/zwave/devices/%d/instances?%s' % (device_1.id, url_encode(data)))
        instances_data = self.check_api_response(response)
        assert len(instances_data['instances']) == 1
        assert instances_data['instances'][0]['name'] == 'test_instance'
        assert instances_data['instances'][0]['description'] == 'Test instance'

        data = dict(access_token=admin_access_token.access_token)
        response = self.app.get('/api/v1/zwave/devices/%d/instances?%s' % (device_2.id, url_encode(data)))
        instances_data = self.check_api_response(response)
        assert len(instances_data['instances']) == 0

        data = dict(access_token=user_access_token.access_token, options='all')
        response = self.app.get('/api/v1/zwave/devices/%d/instances?%s' % (device_2.id, url_encode(data)))
        self.check_api_response(response, 404)

        # Get instance info with command groups
        data = dict(access_token=user_access_token.access_token, embed='command_groups')
        response = self.app.get('/api/v1/zwave/devices/%d/instances?%s' % (device_1.id, url_encode(data)))
        instances_data = self.check_api_response(response)
        assert len(instances_data['instances']) == 1
        assert instances_data['instances'][0]['name'] == 'test_instance'
        assert instances_data['instances'][0]['description'] == 'Test instance'
        assert len(instances_data['instances'][0]['command_groups']) == 1

    def test_get(self):
        user_access_token = self.get_access_token_for_role('user')
        admin_access_token = self.get_access_token_for_role('admin')

        device_1 = model.zwave.device.Device(zway_id=5, name='test_device', description='Test device 1')
        db.session.add(device_1)
        device_1 = model.zwave.device.Device.query.filter_by(zway_id=5).first()
        device_2 = model.zwave.device.Device(zway_id=3, name='test_device_2', description='Test device 2')
        db.session.add(device_2)
        device_2 = model.zwave.device.Device.query.filter_by(zway_id=3).first()

        user_access_token.user.devices = [device_1]

        command_group = model.zwave.command_group.CommandGroup(name='test_group', description='Test instance')
        db.session.add(command_group)

        instance_1 = model.zwave.instance.Instance(name='test_instance', description='Test instance', device=device_1, command_groups=[command_group])
        db.session.add(instance_1)
        instance_1 = model.zwave.instance.Instance.query.filter_by(device=device_1).first()

        instance_2 = model.zwave.instance.Instance(name='test_instance_2', description='Test instance 2', device=device_2, command_groups=[command_group])
        db.session.add(instance_2)
        instance_2 = model.zwave.instance.Instance.query.filter_by(device=device_2).first()

        db.session.commit()

        # Get instance info
        data = dict(access_token=user_access_token.access_token)
        response = self.app.get('/api/v1/zwave/devices/%d/instances/%d?%s' % (device_1.id, instance_1.id, url_encode(data)))
        instances_data = self.check_api_response(response)
        assert instances_data['instance']['name'] == 'test_instance'
        assert instances_data['instance']['description'] == 'Test instance'

        response = self.app.get('/api/v1/zwave/devices/%d/instances/%d?%s' % (device_2.id, instance_2.id, url_encode(data)))
        self.check_api_response(response, 404)

        data = dict(access_token=admin_access_token.access_token)
        response = self.app.get('/api/v1/zwave/devices/%d/instances/%d?%s' % (device_2.id, instance_2.id, url_encode(data)))
        instances_data = self.check_api_response(response)
        assert instances_data['instance']['name'] == 'test_instance_2'
        assert instances_data['instance']['description'] == 'Test instance 2'

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

        instance_1 = model.zwave.instance.Instance(name='test_instance', description='Test instance', device=device_1)
        db.session.add(instance_1)
        instance_1 = model.zwave.instance.Instance.query.filter_by(device=device_1).first()

        instance_2 = model.zwave.instance.Instance(name='test_instance_2', description='Test instance 2', device=device_2)
        db.session.add(instance_2)
        instance_2 = model.zwave.instance.Instance.query.filter_by(device=device_2).first()

        db.session.commit()

        # Update instance info
        data = dict(access_token=admin_access_token.access_token)
        post_data = dict(name='new_name', description='new_description')
        response = self.app.put('/api/v1/zwave/devices/%d/instances/%d?%s' % (device_1.id, instance_1.id, url_encode(data)), data=json.dumps(post_data), content_type='application/json')
        instances_data = self.check_api_response(response)
        assert instances_data['instance']['name'] == post_data['name']
        assert instances_data['instance']['description'] == post_data['description']

        instance_1 = model.zwave.instance.Instance.query.filter_by(device=device_1).first()
        assert instance_1.name == post_data['name']
        assert instance_1.description == post_data['description']
