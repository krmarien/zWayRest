from zwayrest import db

role2action = db.Table('role2action',
   db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
   db.Column('action_id', db.Integer, db.ForeignKey('action.id'))
)

class Role(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(64), unique = True)
   parent_id = db.Column(db.Integer, db.ForeignKey('role.id'))
   parent = db.relationship('Role', uselist=False, remote_side=[id])
   actions = db.relationship('Action', secondary=role2action, backref=db.backref('roles'))

   def get_parents(self):
      parents = set([])
      if self.parent is not None:
          parents.add(self.parent)
          parents = parents | self.parent.get_parents()

      return parents
