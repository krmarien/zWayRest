from zwayrest import oauth
from zwayrest.helper.router import Router
from zwayrest.restapi.resource import Resource

class Auth(Resource):
    def __init__(self):
        super(Auth, self).__init__()

    @oauth.token_handler
    def get(self):
        return None

Router.add_route(Auth, '/auth', 'account.auth')
