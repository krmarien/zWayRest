import requests
from zwayrest.restapi.resource import Resource as RestResource
from zwayrest.model.zwave.auth.user import ZwaveUser

class Resource(RestResource):
    @property
    def user(self):
        rest_user = super(Resource, self).user

        if rest_user is None:
            return abort(401)

        user = User.query.filter_by(id=rest_user.id).first()

        return user
