from zwayrest import db
from zwayrest.model.model_base import ModelBase
from zwayrest import model
from flask.ext.restful import fields, marshal

instance2command_group = db.Table('instance2command_group',
    db.Column('instance_id', db.Integer, db.ForeignKey('instance.id')),
    db.Column('command_group_id', db.Integer, db.ForeignKey('command_group.id'))
)

class Instance(db.Model, ModelBase):
    id = db.Column(db.Integer, primary_key = True)
    zway_id = db.Column(db.Integer, unique = True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship('Device', backref="instances")
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    command_groups = db.relationship('CommandGroup', secondary=instance2command_group, lazy='select')

    marshal_fields = {
        'id': fields.Integer,
        'zway_id': fields.Integer,
        'name': fields.String,
        'description': fields.String
    }

    def __repr__(self):
        return '<Instance %r> %r' % (self.id, self.name)

    @staticmethod
    def get_marshal_fields(filters=[], embed=[]):
        current_fields = Instance.marshal_fields

        if 'device' in embed:
            current_fields['device'] = fields.Nested(model.zwave.device.Device.get_marshal_fields(filters, embed))

        if 'command_groups' in embed:
            current_fields['command_groups'] = fields.Nested(model.zwave.command_group.CommandGroup.get_marshal_fields(filters, embed))

        return current_fields

    def marshal(self, filters=[], embed=[]):
        current_fields = Instance.get_marshal_fields(filters, embed)

        return marshal(self, current_fields)
