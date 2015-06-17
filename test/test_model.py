import pytest
from sqlalchemy.exc import IntegrityError
from test_base import TestBase
from zwayrest import model, db


class TestModel(TestBase):

    def test_action(self):
        test_action = model.auth.action.Action(name='test_action')
        db.session.add(test_action)
        db.session.commit()

        assert model.auth.action.Action.query.count() == 1

        test_action = model.auth.action.Action.query.first()

        assert test_action.name == 'test_action'

        test_action2 = model.auth.action.Action(name='test_action2')
        db.session.add(test_action2)
        db.session.commit()

        assert model.auth.action.Action.query.count() == 2

        fail_action = model.auth.action.Action(name='test_action2')

        with pytest.raises(IntegrityError):
            db.session.add(fail_action)
            db.session.commit()

    def test_role(self):
        test_action2 = model.auth.action.Action(name='test_action')
        db.session.add(test_action2)
        test_action = model.auth.action.Action.query.first()

        test_role = model.auth.role.Role(name='test_role', actions=[test_action])
        db.session.add(test_role)
        db.session.commit()

        assert model.auth.role.Role.query.count() == 1

        test_role = model.auth.role.Role.query.first()

        assert test_role.name == 'test_role'
        assert len(test_role.actions) == 1
        assert test_role.actions[0].name == 'test_action'
