from zwayrest import db, model
from flask.ext.script import Manager, Option

ZwaveInitCommand = Manager(usage="Initialize zwayrest database")

device_types = [
    {
        'zway_id': 1,
        'name': 'Portable Controller',
    },
    {
        'zway_id': 2,
        'name': 'Static Controller',
    },
    {
        'zway_id': 3,
        'name': 'GenericTypeAVControl',
    },
    {
        'zway_id': 4,
        'name': 'Display',
    },
    {
        'zway_id': 8,
        'name': 'Thermostat',
    },
    {
        'zway_id': 9,
        'name': 'WindowCovering',
    },
    {
        'zway_id': 15,
        'name': 'Repeater Slave',
    },
    {
        'zway_id': 16,
        'name': 'Binary Switch',
    },
    {
        'zway_id': 17,
        'name': 'Multilevel Switch',
    },
    {
        'zway_id': 18,
        'name': 'Switch Remote',
    },
    {
        'zway_id': 20,
        'name': 'ZIP Gateway',
    },
    {
        'zway_id': 21,
        'name': 'ZIP Node',
    },
    {
        'zway_id': 22,
        'name': 'Ventilation',
    },
    {
        'zway_id': 24,
        'name': 'Remote Switch',
    },
    {
        'zway_id': 32,
        'name': 'Binary Sensor',
    },
    {
        'zway_id': 33,
        'name': 'Multilevel Sensor',
    },
    {
        'zway_id': 48,
        'name': 'Meter Pulse',
    },
    {
        'zway_id': 49,
        'name': 'Meter',
    },
    {
        'zway_id': 64,
        'name': 'Entry Control',
    },
    {
        'zway_id': 80,
        'name': 'Semi Interoperable',
    },
    {
        'zway_id': 161,
        'name': 'Alarm Sensor',
    }
]

@ZwaveInitCommand.command
def create_device_types():
    """Create all device types"""

    for type_data in device_types:
        device_type = model.zwave.device_type.DeviceType.query.filter_by(zway_id=type_data['zway_id']).first()

        if device_type is None:
            device_type = model.zwave.device_type.DeviceType(name=type_data['name'], zway_id=type_data['zway_id'])
            db.session.add(device_type)
        else:
            device_type.name = type_data['name']

    db.session.commit()
