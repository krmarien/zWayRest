from zwayrest import db
from zwayrest.model.model_base import ModelBase
from flask.ext.restful import fields, marshal

class DeviceType(db.Model, ModelBase):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())

    marshal_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String
    }

    def __repr__(self):
        return '<DeviceType %r> %r' % (self.id, self.name)

    @staticmethod
    def get_marshal_fields(filters=[], embed=[]):
        current_fields = DeviceType.marshal_fields

        return current_fields

    def marshal(self, filters=[], embed=[]):
        current_fields = DeviceType.get_marshal_fields(filters, embed)

        return marshal(self, current_fields)
