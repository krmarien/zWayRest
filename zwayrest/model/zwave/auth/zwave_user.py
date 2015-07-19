from zwayrest import db
from zwayrest import model
from flask.ext.restful import fields, marshal

zwave_user2device = db.Table('zwave_user2device',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('device_id', db.Integer, db.ForeignKey('device.id'))
)

class ZwaveUser(model.auth.user.User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    devices = db.relationship('Device', secondary=zwave_user2device, lazy='select', backref="users")

    __mapper_args__ = {
        'polymorphic_identity': 'zwave_user'
    }

    def __repr__(self):
        return '<ZwaveUser %r> %r %r' % (self.id, self.username, self.email)

    @staticmethod
    def get_marshal_fields(filters=[], embed=[]):
        current_fields = model.auth.user.User.get_marshal_fields(filters, embed)

        if 'devices' in embed:
            current_fields['devices'] = fields.Nested(model.zwave.device.Device.get_marshal_fields(filters, embed))

        return current_fields

    def marshal(self, filters=[], embed=[]):
        current_fields = ZwaveUser.get_marshal_fields(filters, embed)

        return marshal(self, current_fields)
