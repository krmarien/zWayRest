import requests
from zwayrest import model, db

class Update(object):

    @staticmethod
    def import_devices(url):
        r = requests.get('http://files.krmarien.be/Extra/zway.json')
        data = r.json()

        for key in data:
            zway_id = int(key)
            # Skip controller
            if zway_id == 1:
                continue

            # Create or update the device
            Update.create_device(zway_id, data[key])

    @staticmethod
    def create_device(zway_id, data):
        device = model.zwave.device.Device.query.filter_by(zway_id=zway_id).first()

        device_type_id = int(data['data']['genericType']['value'])
        device_type = model.zwave.device_type.DeviceType.query.filter_by(zway_id=device_type_id).first()

        if device is None:
            device = model.zwave.device.Device(
                zway_id=zway_id,
                name=data['data']['givenName']['value'],
                description='',
                device_type=device_type
            )
            db.session.add(device)
        else:
            device.name = data['data']['givenName']['value']
            device.device_type = device_type

        for key in data['instances']:
            instance_id = int(key)

            Update.create_instance(device, instance_id, data['instances'][key])

        db.session.commit()

    @staticmethod
    def create_instance(device, zway_id, data):
        instance = model.zwave.instance.Instance.query.filter_by(zway_id=zway_id, device=device).first()

        if instance is None:
            instance = model.zwave.instance.Instance(name='', description='', device=device, zway_id=zway_id)
            db.session.add(instance)

        for key in data['commandClasses']:
            command_group_id = int(key)
            Update.create_command_group(instance, command_group_id, data['commandClasses'][key])

    @staticmethod
    def create_command_group(instance, zway_id, data):
        commandGroup = model.zwave.command_group.CommandGroup.query.filter_by(zway_id=zway_id).first()

        if commandGroup is None:
            commandGroup = model.zwave.command_group.CommandGroup(zway_id=zway_id, name=data['name'])
            db.session.add(commandGroup)

        instance.command_groups.append(commandGroup)
