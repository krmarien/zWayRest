import requests
from zwayrest.restapi.resource import Resource as RestResource
from zwayrest.model.zwave.auth.user import User

class Resource(RestResource):
    def get_user(self):
        rest_user = super(Resource, self).get_user()

        if rest_user is None:
            return abort(401)

        user = User.query.filter_by(id=rest_user.id).first()

        return user
