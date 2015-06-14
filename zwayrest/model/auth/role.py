from zwayrest import db

role2action = db.Table('role2action',
    db.Column('role_id', db.Integer, db.ForeignKey('auth.role.id')),
    db.Column('action_id', db.Integer, db.ForeignKey('auth.action.id')),
    schema='auth'
)

class Role(db.Model):
    __table_args__ = {"schema": "auth"}

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    parent_id = db.Column(db.Integer, db.ForeignKey('auth.role.id'))
    parent = db.relationship('Role', uselist=False, remote_side=[id])
    actions = db.relationship('Action', secondary=role2action, backref=db.backref('roles'))

    def get_parents(self):
        parents = set([])
        if self.parent is not None:
            parents.add(self.parent)
            parents = parents | self.parent.get_parents()

        return parents
