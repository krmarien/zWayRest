from flask import request
from zwayrest.helper.oauth import OAuth
from zwayrest.helper.router import Router
from zwayrest.restapi.resource import Resource

class Account(Resource):
    def __init__(self):
        super(Account, self).__init__()

    @OAuth.check_acl('account.account.get')
    def get(self):
        if self.get_user() is None:
            return abort(401)

        return {'user': self.get_user().marshal(self.filters, self.embed)}

Router.add_route(Account, '/account', 'account')
