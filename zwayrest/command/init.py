from zwayrest import db, model
from zwayrest.model.auth.action import Action
from zwayrest.model.auth.client import Client
from zwayrest.model.auth.role import Role
from collections import OrderedDict
import random
from flask.ext.script import Manager, Option

InitCommand = Manager(usage="Initialize zwayrest database")

roles = OrderedDict([
    ('guest', {
        'parent': None,
        'actions': []
    }),
    ('user', {
        'parent': 'guest',
        'actions': [
            'account.account.get',
            'account.account.put',
            'account.session_list.get',
            'account.session.get',
            'account.session.delete',
            'zwave.device.get',
            'zwave.device_list.get',
            'zwave.zway.get'
        ]
    }),
    ('admin', {
        'parent': 'user',
        'actions': [
            'zwave.device.put',
            'zwave.device_list.all.get',
        ]
    })
])

@InitCommand.command
def empty_db():
    """Emtpy database"""
    confirm = raw_input("Are you sure you want to empty the database [y/n]: ")

    if confirm == 'y' or confirm == 'yes':
        db.drop_all()
        db.create_all()

@InitCommand.command
def build_acl():
    """Build ACL Tree"""

    print "Building ACL Tree ..."
    for role_name, info in roles.iteritems():
        parent_id = None
        actions = []

        if info['parent'] is not None:
            parent = Role.query.filter_by(name=info['parent']).one()
            parent_id = parent.id

        for action_name in info['actions']:
            action = Action.query.filter_by(name=action_name).first()
            if action is None:
               db.session.add(Action(name=action_name))

            actions.append(Action.query.filter_by(name=action_name).one())

        role = Role.query.filter_by(name=role_name).first()
        if role is None:
            db.session.add(Role(name=role_name, parent_id=parent_id, actions=actions))
        else:
            role.parent_id = parent_id
            role.actions = actions

        db.session.commit()

@InitCommand.command
def create_client():
    """Create Client"""

    print "Creating client ..."

    name = raw_input("Client Name: ")
    description = raw_input("Client Description: ")
    scopes = raw_input("Scopes (comma separated list): ")

    save_client(name, description, scopes)

def save_client(name, description, scopes):
    client_id = "%032x" % random.getrandbits(160)
    client_secret = "%032x" % random.getrandbits(220)

    client = Client(name=name, description=description, client_id=client_id, client_secret=client_secret, is_confidential=True, _redirect_uris='/', _default_scopes=scopes)
    db.session.add(client)
    client = Client.query.filter_by(name=name).first()
    db.session.commit()

    print "Client added with:"
    print "   Id: %s" % client.client_id
    print "   Secret: %s" % client.client_secret
    print "   Scopes: %s" % client._default_scopes

    return client
