from flask import request, abort
from flask.ext.restful import reqparse, Resource as FlaskResource

class Resource(FlaskResource):
    def __init__(self):
        req_argparse = reqparse.RequestParser()
        req_argparse.add_argument('filter', type = str, default = "", help = 'No filters provided, or wrong')
        req_argparse.add_argument('embed', type = str, default = "", help = 'No embed provided, or wrong')
        req_argparse.add_argument('limit', type = int, default = None, help = 'No limit provided, or wrong')

        args = req_argparse.parse_args()

        self.filters = args['filter'].split()
        self.embed = args['embed'].split()
        self.limit = args['limit']

    def get_user(self):
        if not hasattr(request, 'oauth'):
            return abort(401)

        return request.oauth.user
