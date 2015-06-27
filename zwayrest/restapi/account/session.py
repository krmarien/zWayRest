from flask import abort
from zwayrest import db, model
from zwayrest.helper.oauth import OAuth
from zwayrest.helper.router import Router
from zwayrest.restapi.resource import Resource

class SessionList(Resource):
    def __init__(self):
        super(SessionList, self).__init__()

    @OAuth.check_acl('account.session_list.get')
    def get(self):
        if self.user is None:
            return abort(401)

        sessions = model.auth.bearer_token.BearerToken.query.filter_by(user=self.user).all();

        session_list = []

        for session in sessions:
            session_list.insert(0, session.marshal(self.filters, self.embed))

        return {'sessions' : session_list}

Router.add_route(SessionList, '/account/sessions', 'account.session_list')

class Session(Resource):
    def __init__(self):
        super(Session, self).__init__()

    @OAuth.check_acl('account.session.get')
    def get(self, session_id):
        if self.user is None:
            return abort(401)

        session = model.auth.bearer_token.BearerToken.query.filter_by(user=self.user, id=session_id).first();

        if session is None:
            return abort(404)

        return {'session' : session.marshal(self.filters, self.embed)}

    @OAuth.check_acl('account.session.delete')
    def delete(self, session_id):
        if self.user is None:
            return abort(401)

        session = model.auth.bearer_token.BearerToken.query.filter_by(user=self.user, id=session_id).first();

        if session == None:
            abort(404)

        marshaled = session.marshal(self.filters, self.embed);

        db.session.delete(session)
        db.session.commit()

        return {'session': marshaled}

Router.add_route(Session, '/account/sessions/<string:session_id>', 'account.session')
