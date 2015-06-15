from zwayrest import app, api

class Router(object):

    @staticmethod
    def add_route(resource, url, endpoint):
        api.add_resource(resource, app.config['API_VERSION'] + url, endpoint = endpoint)
