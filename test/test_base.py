import json
import pytest
from zwayrest import app, db

class TestBase(object):

    def setup_class(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zwayrest:zwayrest@localhost/zwayrest_test'

        self.app = app.test_client()

        #db.create_all()

    def teardown_class(self):
        #db.session.remove()
        #db.drop_all()
        pass

    def check_api_response(self, response, status_code=200):
        assert response.headers['Content-Type'] == 'application/json'
        assert response.status_code == status_code

        return json.loads(response.data)

    @pytest.fixture(autouse=True)
    def db_connection(self, request):
        db.create_all()
        def fin():
            db.session.remove()
            db.drop_all()
        request.addfinalizer(fin)
