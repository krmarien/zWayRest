from zwayrest import db
from zwayrest.model.model_base import ModelBase
from zwayrest.model.auth.client import Client
from zwayrest.model.auth.user import User
from flask.ext.restful import fields, marshal
import uuid

def uuid_gen():
    return str(uuid.uuid4())

class BearerToken(db.Model, ModelBase):
    id = db.Column(db.String(128), primary_key=True, default=uuid_gen)
    client_id = db.Column(db.String(40), db.ForeignKey('client.client_id'), nullable=False)
    client = db.relationship('Client')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime())
    last_active = db.Column(db.DateTime())
    remote_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    _scopes = db.Column(db.Text)

    marshal_fields = {
        'id': fields.String,
        'remote_address': fields.String,
        'user_agent': fields.String
    }

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    @staticmethod
    def get_marshal_fields(filters=[], embed=[]):
        current_fields = BearerToken.marshal_fields

        current_fields['client'] = fields.Nested(Client.get_marshal_fields(filters, embed))
        current_fields['user'] = fields.Nested(User.get_marshal_fields(filters, embed))

        return current_fields

    def marshal(self, filters=[], embed=[]):
        current_fields = BearerToken.get_marshal_fields(filters, embed)

        marshalled = marshal(self, current_fields)

        if self.expires is None:
            marshalled['expires'] = ''
        else:
            marshalled['expires'] = self.expires.isoformat() + '+0000'

        if self.last_active is None:
            marshalled['last_active'] = ''
        else:
            marshalled['last_active'] = self.last_active.isoformat() + '+0000'

        return marshalled
