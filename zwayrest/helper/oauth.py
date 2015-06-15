from datetime import datetime, timedelta
from zwayrest import app, oauth, db
from zwayrest.model.auth.client import Client
from zwayrest.model.auth.grant_token import GrantToken
from zwayrest.model.auth.bearer_token import BearerToken
from zwayrest.model.auth.user import User
from zwayrest.model.auth.role import Role
from zwayrest.model.auth.action import Action
from flask import request, abort
from functools import wraps

class OAuth(object):
    @oauth.clientgetter
    def load_client(client_id):
        return Client.query.filter_by(client_id=client_id).first()

    @oauth.grantgetter
    def load_grant(client_id, code):
        # Currently not used
        return None

    @oauth.grantsetter
    def save_grant(client_id, code, request, *args, **kwargs):
        # Currently not used
        return None

    @oauth.tokengetter
    def load_token(access_token=None, refresh_token=None):
        if access_token:
            return BearerToken.query.filter_by(access_token=access_token).first()
        elif refresh_token:
            return BearerToken.query.filter_by(refresh_token=refresh_token).first()

    @oauth.tokensetter
    def save_token(token, request, *args, **kwargs):
        toks = BearerToken.query.filter_by(client_id=request.client.client_id, user_id=request.user.id)

        expires_in = token.pop('expires_in')
        expires = datetime.utcnow() + timedelta(seconds=expires_in)

        tok = BearerToken(
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
            _scopes=token['scope'],
            expires=expires,
            client_id=request.client.client_id,
            user_id=request.user.id,
        )
        db.session.add(tok)
        db.session.commit()
        return tok

    @oauth.usergetter
    def get_user(username, password, *args, **kwargs):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def get_current_user():
        if request.oauth is None:
            return None
        return request.oauth.user

    @staticmethod
    def check_acl(action):
        def wrapper(f):
            @wraps(f)
            @oauth.require_oauth()
            def decorated(*args, **kwargs):
                if request.oauth.user is None:
                    return abort(401)

                roles = request.oauth.user.get_roles()

                ids = []
                for role in roles:
                    ids.append(role.id)

                number = db.session.query(Action)\
                    .filter(Role.actions.any(Action.name==action))\
                    .filter(Role.id.in_(ids)).count()

                if number > 0:
                    return f(*args, **kwargs)
                else:
                    return abort(401)
            return decorated if not app.config['DISABLE_AUTH'] else f
        return wrapper
