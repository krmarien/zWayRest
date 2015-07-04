from zwayrest import db
from zwayrest.model.model_base import ModelBase
from flask.ext.restful import fields, marshal

class CommandGroup(db.Model, ModelBase):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    zway_id = db.Column(db.Integer, unique = True)
    description = db.Column(db.Text())

    marshal_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'zway_id': fields.Integer,
        'description': fields.String
    }

    def __repr__(self):
        return '<CommandGroup %r> %r' % (self.id, self.name)

    @staticmethod
    def get_marshal_fields(filters=[], embed=[]):
        current_fields = CommandGroup.marshal_fields

        return current_fields

    def marshal(self, filters=[], embed=[]):
        current_fields = CommandGroup.get_marshal_fields(filters, embed)

        return marshal(self, current_fields)
