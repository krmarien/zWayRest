from datetime import datetime
import pytest
from sqlalchemy.exc import IntegrityError
from test_base import TestBase
from zwayrest import model, db

class TestModelAuth(TestBase):

    def test_action(self):
        test_action = model.auth.action.Action(name='test_action')
        db.session.add(test_action)
        db.session.commit()

        assert model.auth.action.Action.query.count() == 1

        test_action = model.auth.action.Action.query.first()

        assert test_action.name == 'test_action'

        test_action2 = model.auth.action.Action(name='test_action2')
        db.session.add(test_action2)
        db.session.commit()

        assert model.auth.action.Action.query.count() == 2

        fail_action = model.auth.action.Action(name='test_action2')

        with pytest.raises(IntegrityError):
            db.session.add(fail_action)
            db.session.commit()

    def test_role(self):
        test_action2 = model.auth.action.Action(name='test_action')
        db.session.add(test_action2)
        test_action = model.auth.action.Action.query.first()

        test_role = model.auth.role.Role(name='test_role', actions=[test_action])
        db.session.add(test_role)
        db.session.commit()

        assert model.auth.role.Role.query.count() == 1

        test_role = model.auth.role.Role.query.first()

        assert test_role.name == 'test_role'
        assert len(test_role.actions) == 1
        assert test_role.actions[0].name == 'test_action'

    def test_user(self):
        test_role = model.auth.role.Role(name='test_role', actions=[])
        db.session.add(test_role)
        test_role = model.auth.role.Role.query.first()

        test_user = model.auth.user.User(username='username', fullname='Full Name', email='email@test.com', pwdhash="", roles=[test_role])
        test_user.set_password('pwd')
        db.session.add(test_user)
        db.session.commit()

        assert model.auth.user.User.query.count() == 1

        test_user = model.auth.user.User.query.first()

        assert test_user.username == 'username'
        assert test_user.fullname == 'Full Name'
        assert test_user.email == 'email@test.com'
        assert len(test_user.roles) == 1
        assert test_user.roles[0].name == 'test_role'
        assert test_user.check_password('pwd') == True

    def test_client(self):
        test_client = model.auth.client.Client(name='client', description='description', client_id='527jdkdsf', client_secret='sdfhlasdf23', is_confidential=True, _redirect_uris='/', _default_scopes='scope1 scope2')
        db.session.add(test_client)
        db.session.commit()

        assert model.auth.client.Client.query.count() == 1

        test_client = model.auth.client.Client.query.first()

        assert test_client.name == 'client'
        assert test_client.description == 'description'
        assert test_client.client_id == '527jdkdsf'
        assert test_client.client_secret == 'sdfhlasdf23'
        assert test_client.client_type == 'confidential'
        assert len(test_client.redirect_uris) == 1
        assert test_client.redirect_uris[0] == '/'
        assert test_client.default_redirect_uri == '/'
        assert len(test_client.default_scopes) == 2
        assert test_client.default_scopes[0] == 'scope1'
        assert test_client.default_scopes[1] == 'scope2'

    def test_bearer_token(self):
        test_client = model.auth.client.Client(name='client', description='description', client_id='527jdkdsf', client_secret='sdfhlasdf23', is_confidential=True, _redirect_uris='/', _default_scopes='scope1')
        db.session.add(test_client)
        test_user = model.auth.user.User(username='username', fullname='Full Name', email='email@test.com', pwdhash="", roles=[])
        db.session.add(test_user)

        expire_time = datetime.now().replace(microsecond=0)
        test_token = model.auth.bearer_token.BearerToken(client=test_client, user=test_user, token_type='type', access_token='832ief', refresh_token='28poief', expires=expire_time, remote_address='127.0.0.1', user_agent='Safari', _scopes='scope1 scope2')
        db.session.add(test_token)
        db.session.commit()

        assert model.auth.bearer_token.BearerToken.query.count() == 1

        test_token = model.auth.bearer_token.BearerToken.query.first()

        assert test_token.client.name == test_client.name
        assert test_token.user.username == test_user.username
        assert test_token.token_type == 'type'
        assert test_token.access_token == '832ief'
        assert test_token.refresh_token == '28poief'
        assert test_token.expires == expire_time
        assert test_token.remote_address == '127.0.0.1'
        assert test_token.user_agent == 'Safari'
        assert len(test_token.scopes) == 2
        assert test_token.scopes[0] == 'scope1'
        assert test_token.scopes[1] == 'scope2'

    def test_grant_token(self):
        test_client = model.auth.client.Client(name='client', description='description', client_id='527jdkdsf', client_secret='sdfhlasdf23', is_confidential=True, _redirect_uris='/', _default_scopes='scope1')
        db.session.add(test_client)
        test_user = model.auth.user.User(username='username', fullname='Full Name', email='email@test.com', pwdhash="", roles=[])
        db.session.add(test_user)

        expire_time = datetime.now().replace(microsecond=0)
        test_token = model.auth.grant_token.GrantToken(client=test_client, user=test_user, code='832ief', expires=expire_time, redirect_uri='/', _scopes='scope1 scope2')
        db.session.add(test_token)
        db.session.commit()

        assert model.auth.grant_token.GrantToken.query.count() == 1

        test_token = model.auth.grant_token.GrantToken.query.first()

        assert test_token.client.name == test_client.name
        assert test_token.user.username == test_user.username
        assert test_token.code == '832ief'
        assert test_token.expires == expire_time
        assert test_token.redirect_uri == '/'
        assert len(test_token.scopes) == 2
        assert test_token.scopes[0] == 'scope1'
        assert test_token.scopes[1] == 'scope2'
