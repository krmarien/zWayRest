from zwayrest import db
from zwayrest.model.auth.user import User
from zwayrest.model.zwave.device import Device
from flask.ext.restful import fields, marshal

user2device = db.Table('user2device',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('device_id', db.Integer, db.ForeignKey('device.id'))
)

class ZwaveUser(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    devices = db.relationship('Device', secondary=user2device, lazy='select')
