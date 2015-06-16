from zwayrest import db
from zwayrest.model.model_base import ModelBase
from flask.ext.restful import fields, marshal

class Client(db.Model, ModelBase):
    name = db.Column(db.String(40))
    description = db.Column(db.String(400))
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True, nullable=False)
    is_confidential = db.Column(db.Boolean)
    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    marshal_fields = {
        'name': fields.String,
        'description': fields.String,
    }

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []

    @staticmethod
    def get_marshal_fields(filters=[], embed=[]):
        current_fields = Client.marshal_fields

        return current_fields

    def marshal(self, filters=[], embed=[]):
        current_fields = Client.get_marshal_fields(filters, embed)

        return marshal(self, current_fields)
