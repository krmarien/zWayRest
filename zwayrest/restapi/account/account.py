from flask import abort
from flask.ext.restful import reqparse
from zwayrest import db
from zwayrest.helper.oauth import OAuth
from zwayrest.helper.router import Router
from zwayrest.restapi.resource import Resource

class Account(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('options', type = str, location = 'json')

        super(Account, self).__init__()

    @OAuth.check_acl('account.account.get')
    def get(self):
        if self.get_user() is None:
            return abort(401)

        return {'user': self.get_user().marshal(self.filters, self.embed)}

    @OAuth.check_acl('account.account.put')
    def put(self):
        args = self.reqparse.parse_args()

        if self.get_user() is None:
            return abort(401)

        user = self.get_user()

        if args['options'] == 'password':
            reqparse_put = reqparse.RequestParser()
            reqparse_put.add_argument('old_password', required = True, type = str, location = 'json')
            reqparse_put.add_argument('new_password', required = True, type = str, location = 'json')
            reqparse_put.add_argument('repeat_password', required = True, type = str, location = 'json')
            args = reqparse_put.parse_args()

            if not user.check_password(args['old_password']):
                return {'error': 'Passwords do not match'},409

            if args['new_password'] != args['repeat_password']:
                return {'error': 'Passwords do not match'},409

            user.set_password(args['new_password'])

            db.session.commit()
        else:
            reqparse_put = reqparse.RequestParser()
            reqparse_put.add_argument('fullname', required = True, type = str, location = 'json')
            reqparse_put.add_argument('email', required = True, type = str, location = 'json')
            args = reqparse_put.parse_args()

            user.fullname = args['fullname']
            user.email = args['email']

            db.session.commit()

        return {'user': user.marshal(self.filters, self.embed)}

Router.add_route(Account, '/account', 'account')
