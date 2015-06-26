from zwayrest import db, model
from zwayrest.model.zwave.auth.zwave_user import ZwaveUser as User
from zwayrest.model.auth.role import Role
from zwayrest.model.auth.grant_token import GrantToken
from zwayrest.model.auth.bearer_token import BearerToken
import getpass
import re
from flask.ext.script import Manager, Option

UserCommand = Manager(usage="Manage the users")

@UserCommand.command
def create():
    """Create User"""

    print "Creating user ..."
    username = raw_input("Username: ")
    while username.strip() == "":
        username = raw_input("Provide valid username: ")

    fullname = raw_input("Full Name: ")
    while fullname.strip() == "":
        fullname = raw_input("Provide valid full name: ")

    pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))

    pwd1, pwd2 = pprompt()
    while pwd1 != pwd2:
        print('Passwords do not match. Try again')
        pwd1, pwd2 = pprompt()

    email = raw_input("Email: ")
    while not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        email = raw_input("Provide valid email: ")

    print "Available roles: "
    availableRoles = Role.query.all()
    for role in availableRoles:
        if role.parent is not None:
            print "   - %s extends %s" % (role.name, role.parent.name)
        else:
            print "   - %s" % role.name

    roles = ""
    while roles.strip() == "":
        roles = raw_input("Roles (comma separated list): ")

    save_user(username, fullname, pwd2, email, roles)

def save_user(username, fullname, password, email, roles):
    enteredRoles = roles.split(',')

    roleObjects = []
    for role in enteredRoles:
        roleObject = Role.query.filter_by(name=role.strip()).first()
        if roleObject is None:
            print "Role %s not found" % role
        else:
            roleObjects.append(roleObject)

    user = User(username=username, fullname=fullname, email=email, pwdhash="", roles=roleObjects)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    user = User.query.filter_by(username=username).first()

    print "User added with:"
    print "   Username: %s" % user.username
    print "   Full Name: %s" % user.fullname
    print "   Email: %s" % user.email
    print "   Roles: %s" % roles

    return user

@UserCommand.command
def set_password():
    """Set the password for a user"""

    username = raw_input("Username: ")
    while User.query.filter_by(username=username).first() is None:
        username = raw_input("Provide valid username: ")

    user = User.query.filter_by(username=username).first()

    print "You will update the password of the user:"
    print "   Username: %s" % user.username
    print "   Full Name: %s" % user.fullname
    print "   Email: %s" % user.email

    pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))

    pwd1, pwd2 = pprompt()
    while pwd1 != pwd2:
        print('Passwords do not match. Try again')
        pwd1, pwd2 = pprompt()

    user.set_password(pwd2)
    db.session.commit()

    print ""

    print "Password successfully updated"

@UserCommand.command
def update_roles():
    """Update the roles of a user"""

    username = raw_input("Username: ")
    while User.query.filter_by(username=username).first() is None:
        username = raw_input("Provide valid username: ")

    user = User.query.filter_by(username=username).first()

    roles = []
    for role in user.roles:
        roles.append(role.name)

    print "You will update the password of the user:"
    print "   Username: %s" % user.username
    print "   Full Name: %s" % user.fullname
    print "   Email: %s" % user.email
    print "   Roles: %s" % (', '.join(roles))
    print ""

    print "Available roles: "
    availableRoles = Role.query.all()
    for role in availableRoles:
        if role.parent is not None:
            print "   - %s extends %s" % (role.name, role.parent.name)
        else:
            print "   - %s" % role.name

    roles = ""
    while roles.strip() == "":
        roles = raw_input("Roles (comma separated list): ")

    enteredRoles = roles.split(',')

    user.roles = []
    for role in enteredRoles:
        roleObject = Role.query.filter_by(name=role.strip()).first()
        if roleObject is None:
            print "Role %s not found" % role
        else:
            user.roles.append(roleObject)

    db.session.commit()

    print "The roles where successfully updated"

@UserCommand.command
def disable():
    """Disable a user"""

    username = raw_input("Username: ")
    while User.query.filter_by(username=username).first() is None:
        username = raw_input("Provide valid username: ")

    user = User.query.filter_by(username=username).first()

    roles = []
    for role in user.roles:
        roles.append(role.name)

    print "You will update the password of the user:"
    print "   Username: %s" % user.username
    print "   Full Name: %s" % user.fullname
    print "   Email: %s" % user.email
    print "   Roles: %s" % (', '.join(roles))
    print ""

    user.set_password('')

    tokens = GrantToken.query.filter_by(user=user).all()

    for token in tokens:
        db.session.delete(token)

    tokens = BearerToken.query.filter_by(user=user).all()

    for token in tokens:
        db.session.delete(token)

    db.session.commit()

    print "The user was successfully disabled"
