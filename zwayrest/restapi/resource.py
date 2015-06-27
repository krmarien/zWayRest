from flask import request, abort
from flask.ext.restful import reqparse, Resource as FlaskResource

class Resource(FlaskResource):
    def __init__(self):
        req_argparse = reqparse.RequestParser()
        req_argparse.add_argument('filter', type = str, default = "", help = 'No filters provided, or wrong')
        req_argparse.add_argument('embed', type = str, default = "", help = 'No embed provided, or wrong')
        req_argparse.add_argument('limit', type = int, default = None, help = 'Wrong limit provided')
        req_argparse.add_argument('options', type = str, default = None, help = 'Wrong options provided')

        args = req_argparse.parse_args()

        self.filters = [chunk.strip() for chunk in args['filter'].split(',')]
        self.embed = [chunk.strip() for chunk in args['embed'].split(',')]
        self.limit = args['limit']
        if args['options'] is not None:
            self.options = [chunk.strip() for chunk in args['options'].split(',')]
        else:
            self.options = []

    @property
    def user(self):
        if not hasattr(request, 'oauth'):
            return abort(401)

        return request.oauth.user
