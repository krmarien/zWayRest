from zwayrest import db
from zwayrest.model.auth.role import Role

user2role = db.Table('user2role',
    db.Column('user_id', db.Integer, db.ForeignKey('auth.user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('auth.role.id')),
    schema='auth'
)

class User(db.Model):
    __table_args__ = {"schema": "auth"}

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    fullname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    pwdhash = db.Column(db.String(100))
    projects = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=user2role, lazy='select', backref=db.backref('users'))

    def __repr__(self):
        return '<User %r> %r %r' % (self.id, self.username, self.email)

    def is_authenticated(self):
       return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

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
