from flask import abort
from flask.ext.restful import reqparse
from zwayrest import db
from zwayrest.helper.oauth import OAuth
from zwayrest.helper.router import Router
from zwayrest.model.zwave.device import Device as DeviceModel
from zwayrest.model.zwave.device_type import DeviceType
from zwayrest.restapi.zwave.resource import Resource

class DeviceList(Resource):
    def __init__(self):
        super(DeviceList, self).__init__()

    @OAuth.check_acl('zwave.device_list.get')
    def get(self):
        if 'all' in self.options:
            if not OAuth.has_access('zwave.device_list.all.get'):
                return abort(401)

            devices = DeviceModel.query.all()
        else:
            devices = self.user.devices

        deviceList = []

        for device in devices:
            deviceList.insert(0, device.marshal(self.filters, self.embed))

        return {'devices' : deviceList}

Router.add_route(DeviceList, '/zwave/devices', 'zwave.device_list')


class Device(Resource):
    def __init__(self):
        super(Device, self).__init__()

    @OAuth.check_acl('zwave.device.get')
    def get(self, device_id):
        device = DeviceModel.query.filter_by(id=device_id).first()

        if device is None:
            return abort(404)

        print device not in self.user.devices and not OAuth.has_access('zwave.device_list.all.get')
        print device not in self.user.devices
        print not OAuth.has_access('zwave.device_list.all.get')
        if device not in self.user.devices and not OAuth.has_access('zwave.device_list.all.get'):
            return abort(401)

        return {'device' : device.marshal(self.filters, self.embed)}

    @OAuth.check_acl('zwave.device.put')
    def put(self, device_id):
        device = DeviceModel.query.filter_by(id=device_id).first()

        if device is None:
            return abort(404)

        if device not in self.user.devices and not OAuth.has_access('zwave.device_list.all.get'):
            return abort(401)

        reqparse_put = reqparse.RequestParser()
        reqparse_put.add_argument('name', required = True, type = unicode, location = 'json')
        reqparse_put.add_argument('description', required = True, type = unicode, location = 'json')
        reqparse_put.add_argument('device_type', required = True, type = int, location = 'json')
        args = reqparse_put.parse_args()

        device_type = DeviceType.query.filter_by(id=args['device_type']).first()

        if device_type is None:
            return {'error': 'Device type was not found'},409

        device.name = args['name']
        device.description = args['description']
        device.device_type = device_type

        db.session.commit()

        return {'device' : device.marshal(self.filters, self.embed)}

Router.add_route(Device, '/zwave/devices/<int:device_id>', 'zwave.device')
