from flask import abort
from flask.ext.restful import reqparse
from zwayrest import db, model
from zwayrest.helper.oauth import OAuth
from zwayrest.helper.router import Router
from zwayrest.restapi.zwave.resource import Resource

class InstanceList(Resource):
    def __init__(self):
        super(InstanceList, self).__init__()

    @OAuth.check_acl('zwave.device.instance_list.get')
    def get(self, device_id):
        device = model.zwave.device.Device.query.filter_by(id=device_id).first()

        if device is None:
            return abort(404)

        if device not in self.user.devices and not OAuth.has_access('zwave.device_list.all.get'):
            return abort(404)

        instances = model.zwave.instance.Instance.query.filter_by(device=device).all()

        instance_list = []

        for instance in instances:
            instance_list.insert(0, instance.marshal(self.filters, self.embed))

        return {'instances' : instance_list}

Router.add_route(InstanceList, '/zwave/devices/<int:device_id>/instances', 'zwave.device.instance_list')

class Instance(Resource):
    def __init__(self):
        super(Instance, self).__init__()

    @OAuth.check_acl('zwave.device.instance.get')
    def get(self, device_id, instance_id):
        instance = model.zwave.instance.Instance.query.filter_by(device_id=device_id, id=instance_id).first()

        if instance is None:
            return abort(404)

        if instance.device not in self.user.devices and not OAuth.has_access('zwave.device_list.all.get'):
            return abort(404)

        return {'instance' : instance.marshal(self.filters, self.embed)}

    @OAuth.check_acl('zwave.device.instance.put')
    def put(self, device_id, instance_id):
        instance = model.zwave.instance.Instance.query.filter_by(device_id=device_id, id=instance_id).first()

        if instance is None:
            return abort(404)

        if instance.device not in self.user.devices and not OAuth.has_access('zwave.device_list.all.get'):
            return abort(401)

        reqparse_put = reqparse.RequestParser()
        reqparse_put.add_argument('name', required = True, type = unicode, location = 'json')
        reqparse_put.add_argument('description', required = True, type = unicode, location = 'json')
        args = reqparse_put.parse_args()

        instance.name = args['name']
        instance.description = args['description']

        db.session.commit()

        return {'instance' : instance.marshal(self.filters, self.embed)}

Router.add_route(Instance, '/zwave/devices/<int:device_id>/instances/<int:instance_id>', 'zwave.device.instance')
