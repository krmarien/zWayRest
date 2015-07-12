from flask import abort
from flask.ext.restful import reqparse
from zwayrest import app, db, model
from zwayrest.helper.oauth import OAuth
from zwayrest.helper.router import Router
from zwayrest.restapi.zwave.resource import Resource

class CommandGroupList(Resource):
    def __init__(self):
        super(CommandGroupList, self).__init__()

    @OAuth.check_acl('zwave.command_group_list.get')
    def get(self):
        command_groups = model.zwave.command_group.CommandGroup.query.all()

        command_group_list = []

        for command_group in command_groups:
            command_group_list.insert(0, command_group.marshal(self.filters, self.embed))

        return {'command_groups' : command_group_list}

Router.add_route(CommandGroupList, '/zwave/command_groups', 'zwave.command_group_list')

class CommandGroup(Resource):
    def __init__(self):
        super(CommandGroup, self).__init__()

    @OAuth.check_acl('zwave.command_group.get')
    def get(self, command_group_id):
        command_group = model.zwave.command_group.CommandGroup.query.filter_by(id=command_group_id).first()

        if command_group is None:
            return abort(404)

        return {'command_group' : command_group.marshal(self.filters, self.embed)}

    @OAuth.check_acl('zwave.command_group.put')
    def put(self, command_group_id):
        command_group = model.zwave.command_group.CommandGroup.query.filter_by(id=command_group_id).first()

        if command_group is None:
            return abort(404)

        reqparse_put = reqparse.RequestParser()
        reqparse_put.add_argument('name', required = True, type = unicode, location = 'json')
        reqparse_put.add_argument('description', required = True, type = unicode, location = 'json')
        args = reqparse_put.parse_args()

        command_group.name = args['name']
        command_group.description = args['description']

        db.session.commit()

        return {'command_group' : command_group.marshal(self.filters, self.embed)}

Router.add_route(CommandGroup, '/zwave/command_groups/<int:command_group_id>', 'zwave.command_group')
