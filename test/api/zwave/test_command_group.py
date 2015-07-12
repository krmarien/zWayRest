from datetime import datetime
import json
from test_api_base import TestApiBase
from werkzeug.urls import url_encode
from zwayrest.command import init as InitCommand, user as UserCommand
from zwayrest import model, db

class TestCommandGroup(TestApiBase):
    def test_get_list(self):
        user_access_token = self.get_access_token_for_role('user')

        command_group_1 = model.zwave.command_group.CommandGroup(zway_id=5, name='test_command_group', description='Test command group 1')
        db.session.add(command_group_1)
        command_group_2 = model.zwave.command_group.CommandGroup(zway_id=3, name='test_command_group_2', description='Test command group 2')
        db.session.add(command_group_2)

        db.session.commit()

        # Get command group info
        data = dict(access_token=user_access_token.access_token)
        response = self.app.get('/api/v1/zwave/command_groups?%s' % url_encode(data))
        command_groups_data = self.check_api_response(response)
        assert len(command_groups_data['command_groups']) == 2
        assert command_groups_data['command_groups'][0]['zway_id'] == 3
        assert command_groups_data['command_groups'][0]['name'] == 'test_command_group_2'
        assert command_groups_data['command_groups'][0]['description'] == 'Test command group 2'
        assert command_groups_data['command_groups'][1]['zway_id'] == 5
        assert command_groups_data['command_groups'][1]['name'] == 'test_command_group'
        assert command_groups_data['command_groups'][1]['description'] == 'Test command group 1'

    def test_get(self):
        user_access_token = self.get_access_token_for_role('user')

        command_group_1 = model.zwave.command_group.CommandGroup(zway_id=5, name='test_command_group', description='Test command group 1')
        db.session.add(command_group_1)
        command_group_2 = model.zwave.command_group.CommandGroup(zway_id=3, name='test_command_group_2', description='Test command group 2')
        db.session.add(command_group_2)

        db.session.commit()

        # Get device info
        data = dict(access_token=user_access_token.access_token)
        response = self.app.get('/api/v1/zwave/command_groups/%d?%s' % (command_group_1.id, url_encode(data)))
        command_groups_data = self.check_api_response(response)
        assert command_groups_data['command_group']['zway_id'] == 5
        assert command_groups_data['command_group']['name'] == 'test_command_group'
        assert command_groups_data['command_group']['description'] == 'Test command group 1'

    def test_put(self):
        admin_access_token = self.get_access_token_for_role('admin')

        command_group_1 = model.zwave.command_group.CommandGroup(zway_id=5, name='test_command_group', description='Test command group 1')
        db.session.add(command_group_1)
        command_group_2 = model.zwave.command_group.CommandGroup(zway_id=3, name='test_command_group_2', description='Test command group 2')
        db.session.add(command_group_2)

        db.session.commit()

        # Update device info
        data = dict(access_token=admin_access_token.access_token)
        post_data = dict(name='new_name', description='new_description')
        response = self.app.put('/api/v1/zwave/command_groups/%d?%s' % (command_group_1.id, url_encode(data)), data=json.dumps(post_data), content_type='application/json')
        command_groups_data = self.check_api_response(response)
        assert command_groups_data['command_group']['zway_id'] == 5
        assert command_groups_data['command_group']['name'] == 'new_name'
        assert command_groups_data['command_group']['description'] == 'new_description'
