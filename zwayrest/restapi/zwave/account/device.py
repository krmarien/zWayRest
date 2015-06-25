from flask import abort
from zwayrest import db
from zwayrest.helper.oauth import OAuth
from zwayrest.helper.router import Router
from zwayrest.model.zwave.device import Device
from zwayrest.restapi.zwave.resource import Resource

class DeviceList(Resource):
    def __init__(self):
        super(DeviceList, self).__init__()

    @OAuth.check_acl('zwave.account.device_list.get')
    def get(self):
        if self.get_user() is None:
            return abort(401)

        devices = Device.query.all()

        return {'devices' : []}

Router.add_route(DeviceList, '/zwave/account/devices', 'zwave.account.device_list')
