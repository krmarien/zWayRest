from zwayrest import db
import uuid

def uuid_gen():
    return str(uuid.uuid4())

class GrantToken(db.Model):
    id = db.Column(db.String(128), primary_key=True, default=uuid_gen)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')
    client_id = db.Column(db.String(40), db.ForeignKey('client.client_id'), nullable=False)
    client = db.relationship('Client')
    code = db.Column(db.String(255), index=True, nullable=False)
    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
