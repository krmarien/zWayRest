from flask import abort
from flask.ext.restful import reqparse
from zwayrest import db, model
from zwayrest.helper.oauth import OAuth
from zwayrest.helper.router import Router
from zwayrest.restapi.zwave.resource import Resource

class DeviceTypeList(Resource):
    def __init__(self):
        super(DeviceTypeList, self).__init__()

    @OAuth.check_acl('zwave.device_type_list.get')
    def get(self):
        device_types = model.zwave.device_type.DeviceType.query.all()

        device_type_list = []

        for device_type in device_types:
            device_type_list.insert(0, device_type.marshal(self.filters, self.embed))

        return {'device_types' : device_type_list}

Router.add_route(DeviceTypeList, '/zwave/device_types', 'zwave.device_type_list')

class DeviceType(Resource):
    def __init__(self):
        super(DeviceType, self).__init__()

    @OAuth.check_acl('zwave.device_type.get')
    def get(self, device_type_id):
        device_type = model.zwave.device_type.DeviceType.query.filter_by(id=device_type_id).first()

        return {'device_type' : device_type.marshal(self.filters, self.embed)}

    @OAuth.check_acl('zwave.device_type.put')
    def put(self, device_type_id):
        device_type = model.zwave.device_type.DeviceType.query.filter_by(id=device_type_id).first()

        reqparse_put = reqparse.RequestParser()
        reqparse_put.add_argument('name', required = True, type = unicode, location = 'json')
        reqparse_put.add_argument('description', required = True, type = unicode, location = 'json')
        args = reqparse_put.parse_args()

        device.name = args['name']
        device.description = args['description']

        db.session.commit()

        return {'device_type' : device_type.marshal(self.filters, self.embed)}

Router.add_route(DeviceType, '/zwave/device_types/<int:device_type_id>', 'zwave.device_type')
