from zwayrest import db
from zwayrest.model.model_base import ModelBase
from zwayrest.model.auth.role import Role
from flask.ext.restful import fields, marshal
from werkzeug import generate_password_hash, check_password_hash

user2role = db.Table('user2role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(db.Model, ModelBase):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    fullname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    pwdhash = db.Column(db.String(100))
    roles = db.relationship('Role', secondary=user2role, lazy='select', backref=db.backref('users'))
    active = db.Column(db.Boolean, default=True, nullable=False)
    failed_logins = db.Column(db.Integer, default=0, nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    marshal_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'fullname': fields.String,
        'email': fields.String
    }

    def __repr__(self):
        return '<User %r> %r %r' % (self.id, self.username, self.email)

    def get_roles(self):
        roles = set([])

        for role in self.roles:
            roles.add(role)
            roles = roles | role.get_parents()
        return roles

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    @staticmethod
    def get_marshal_fields(filters=[], embed=[]):
        current_fields = User.marshal_fields

        if 'roles' in embed:
            current_fields['roles'] = fields.Nested(Role.get_marshal_fields(filters, embed))

        return current_fields

    def marshal(self, filters=[], embed=[]):
        current_fields = User.get_marshal_fields(filters, embed)

        return marshal(self, current_fields)
