from zwayrest import db
from zwayrest.model.model_base import ModelBase

instance2command_group = db.Table('instance2command_group',
    db.Column('instance_id', db.Integer, db.ForeignKey('instance.id')),
    db.Column('command_group_id', db.Integer, db.ForeignKey('command_group.id'))
)

class Instance(db.Model, ModelBase):
    id = db.Column(db.Integer, primary_key = True)
    zway_id = db.Column(db.Integer, unique = True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship('Device', backref="instances")
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    command_groups = db.relationship('CommandGroup', secondary=instance2command_group, lazy='select')
