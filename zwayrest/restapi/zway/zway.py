import requests
import urllib
from zwayrest import app
from zwayrest.helper.oauth import OAuth
from zwayrest.helper.router import Router
from zwayrest.restapi.resource import Resource

class Zway(Resource):
    def __init__(self):
        super(Zway, self).__init__()

    @OAuth.check_acl('zway.get')
    def get(self, path):
        path = urllib.unquote(path).decode('utf8').strip('/')
        base = app.config['ZWAY_URL'].strip('/')

        url = '%s/%s' % (base, path)

        #r = requests.get(url)

        #return r.json()
        return {'zway': url}

Router.add_route(Zway, '/zway/<string:path>', 'zway')
