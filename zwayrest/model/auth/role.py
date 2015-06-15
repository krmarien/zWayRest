from zwayrest import db
from zwayrest.model.model_base import ModelBase
from flask.ext.restful import fields, marshal

role2action = db.Table('role2action',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('action_id', db.Integer, db.ForeignKey('action.id'))
)

class Role(db.Model, ModelBase):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    parent_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    parent = db.relationship('Role', uselist=False, remote_side=[id])
    actions = db.relationship('Action', secondary=role2action, backref=db.backref('roles'))

    marshal_fields = {
        'id': fields.Integer,
        'name': fields.String
    }

    def get_parents(self):
        parents = set([])
        if self.parent is not None:
            parents.add(self.parent)
            parents = parents | self.parent.get_parents()

        return parents

    @staticmethod
    def get_marshal_fields(filters=[], embed=[]):
        current_fields = Role.marshal_fields

        return current_fields

    def marshal(self, filters=[], embed=[]):
        current_fields = Role.get_marshal_fields(filters, embed)

        return marshal(self, current_fields)
