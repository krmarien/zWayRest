import random
from test_base import TestBase
from zwayrest import model, db

class TestModelZwave(TestBase):
    def test_zwave_user(self):
        test_role = model.auth.role.Role(name='test_role', actions=[])
        db.session.add(test_role)
        test_role = model.auth.role.Role.query.first()

        test_device = model.zwave.device.Device(name='test_device')
        db.session.add(test_device)
        test_device = model.zwave.device.Device.query.first()

        test_user = model.zwave.auth.zwave_user.ZwaveUser(username='username', fullname='Full Name', email='email@test.com', pwdhash="", roles=[test_role], devices=[test_device])
        db.session.add(test_user)
        db.session.commit()

        assert model.zwave.auth.zwave_user.ZwaveUser.query.count() == 1
        assert model.auth.user.User.query.count() == 1

        test_user = model.zwave.auth.zwave_user.ZwaveUser.query.first()

        assert test_user.username == 'username'
        assert test_user.fullname == 'Full Name'
        assert test_user.email == 'email@test.com'
        assert len(test_user.roles) == 1
        assert test_user.roles[0].name == 'test_role'
        assert len(test_user.devices) == 1
        assert test_user.devices[0].name == 'test_device'

    def test_command_group(self):
        test_command_group = model.zwave.command_group.CommandGroup(name='test_command_group', description='Test Description', zway_id=4)
        db.session.add(test_command_group)

        assert model.zwave.command_group.CommandGroup.query.count() == 1

        test_command_group = model.zwave.command_group.CommandGroup.query.first()

        assert test_command_group.name == 'test_command_group'
        assert test_command_group.zway_id == 4
        assert test_command_group.description == 'Test Description'

    def test_device_type(self):
        test_device_type = model.zwave.device_type.DeviceType(name='test_device_type', zway_id=5, description='Test Description')
        db.session.add(test_device_type)

        assert model.zwave.device_type.DeviceType.query.count() == 1

        test_device_type = model.zwave.device_type.DeviceType.query.first()

        assert test_device_type.name == 'test_device_type'
        assert test_device_type.zway_id == 5
        assert test_device_type.description == 'Test Description'

    def test_device(self):
        device_type = model.zwave.device_type.DeviceType(name='test_device_type', description='Test Description')
        db.session.add(device_type)
        device_type = model.zwave.device_type.DeviceType.query.first()

        zway_id = random.random()
        test_device = model.zwave.device.Device(zway_id=zway_id, name='test_device', description='Test Description', device_type=device_type)
        db.session.add(test_device)
        test_device = model.zwave.device.Device.query.first()

        assert test_device.zway_id == zway_id
        assert test_device.name == 'test_device'
        assert test_device.description == 'Test Description'
        assert test_device.device_type.name == 'test_device_type'

    def test_instance(self):
        zway_id = random.random()
        device = model.zwave.device.Device(zway_id=zway_id, name='test_device', description='Test Description')
        db.session.add(device)
        device = model.zwave.device.Device.query.first()

        test_command_group = model.zwave.command_group.CommandGroup(name='test_command_group', description='Test Description')
        db.session.add(test_command_group)
        test_command_group = model.zwave.command_group.CommandGroup.query.first()

        test_instance = model.zwave.instance.Instance(name='test_instance', description='Test Description', device=device, command_groups=[test_command_group])
        db.session.add(test_instance)

        assert model.zwave.instance.Instance.query.count() == 1

        test_instance = model.zwave.instance.Instance.query.first()

        assert test_instance.name == 'test_instance'
        assert test_instance.description == 'Test Description'
        assert test_instance.device.zway_id == zway_id
        assert len(test_instance.command_groups) == 1
        assert test_instance.command_groups[0].name == 'test_command_group'

        device = model.zwave.device.Device.query.first()

        assert len(device.instances) == 1
        assert device.instances[0].name == 'test_instance'
