from zwayrest import db
from zwayrest.model.model_base import ModelBase
from zwayrest import model
from flask.ext.restful import fields, marshal

class Device(db.Model, ModelBase):
    id = db.Column(db.Integer, primary_key = True)
    zway_id = db.Column(db.Integer, unique = True)
    name = db.Column(db.String(50))
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_type.id'))
    device_type = db.relationship('DeviceType')
    description = db.Column(db.Text())

    marshal_fields = {
        'id': fields.Integer,
        'zway_id': fields.Integer,
        'name': fields.String,
        'description': fields.String
    }

    def __repr__(self):
        return '<Device %r> %r %r' % (self.id, self.name, self.device_type)

    @staticmethod
    def get_marshal_fields(filters=[], embed=[]):
        current_fields = Device.marshal_fields

        current_fields['device_type'] = fields.Nested(model.zwave.device_type.DeviceType.get_marshal_fields(filters, embed))

        if 'instances' in embed:
            current_fields['instances'] = fields.Nested(model.zwave.instance.Instance.get_marshal_fields(filters, embed))

        if 'users' in embed:
            user_embed = embed
            if 'device' in user_embed:
                del user_embed['device']
            current_fields['users'] = fields.Nested(model.zwave.auth.zwave_user.ZwaveUser.get_marshal_fields(filters, user_embed))

        return current_fields

    def marshal(self, filters=[], embed=[]):
        current_fields = Device.get_marshal_fields(filters, embed)

        return marshal(self, current_fields)
