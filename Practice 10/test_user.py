import pytest

from prj import User

class TestUser:
    @pytest.fixture
    def user(self):
        return User(login="alice", password="secret", role="developer")

    def test_authenticate_success(self, user):
        assert user.authenticate("alice", "secret")

    def test_authenticate_failure(self, user):
        assert not user.authenticate("alice", "wrong")
        assert not user.authenticate("bob", "secret")

    def test_authorize_success(self, user):
        assert user.authorize(["developer", "manager"])

    def test_authorize_failure(self, user):
        assert not user.authorize(["admin"])