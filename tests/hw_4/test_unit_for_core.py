import pytest
from datetime import datetime
from pydantic import SecretStr

from hw_4_tests.demo_service.core.users import UserRole, password_is_longer_than_8, UserService, UserInfo, UserEntity


@pytest.fixture
def user_service():
    return UserService(password_validators=[password_is_longer_than_8])


@pytest.fixture
def valid_user_info():
    return UserInfo(
        username="Username",
        name="Name",
        birthdate=datetime(2001, 9, 30),
        role=UserRole.USER,
        password=SecretStr('123456789')
    )


@pytest.fixture
def invalid_user_info():
    return UserInfo(
        username="Username",
        name="Name",
        birthdate=datetime(2001, 9, 30),
        role=UserRole.USER,
        password=SecretStr('123')
    )


@pytest.fixture
def valid_admin_info():
    return UserInfo(
        username="Username",
        name="Name",
        birthdate=datetime(2001, 9, 30),
        role=UserRole.ADMIN,
        password=SecretStr('123456789')
    )


def test_user_role():
    assert UserRole.USER == 'user'
    assert UserRole.ADMIN == 'admin'


@pytest.mark.parametrize(
    "password, expected",
    [
        ("1" * 9, True),
        ("1" * 8, False),
        ("1" * 5, False),
    ]
)
def test_password_checker(password, expected):
    assert password_is_longer_than_8(password) is expected


def test_success_register(valid_user_info, user_service):
    user_entity: UserEntity = user_service.register(valid_user_info)
    assert user_entity.uid == 1
    assert user_entity.info.username == valid_user_info.username
    assert user_entity.info.name == valid_user_info.name
    assert user_entity.info.birthdate == valid_user_info.birthdate
    assert user_entity.info.role == valid_user_info.role


def test_re_register(valid_user_info, user_service):
    user_entity: UserEntity = user_service.register(valid_user_info)
    with pytest.raises(ValueError, match="username is already taken"):
        user_entity_2: UserEntity = user_service.register(valid_user_info)


def test_invalid_password(invalid_user_info, user_service):
    with pytest.raises(ValueError, match="invalid password"):
        user_entity: UserEntity = user_service.register(invalid_user_info)


def test_get_by_username(valid_user_info, user_service):
    assert user_service.get_by_username(valid_user_info.username) is None
    user_entity: UserEntity = user_service.register(valid_user_info)
    assert user_service.get_by_username(valid_user_info.username) is user_entity


def test_get_by_uid(valid_user_info, user_service):
    assert user_service.get_by_id(0) is None
    user_entity: UserEntity = user_service.register(valid_user_info)
    assert user_service.get_by_id(user_entity.uid) is user_entity


def test_grant_admin(valid_user_info, user_service):
    with pytest.raises(ValueError, match="user not found"):
        user_service.grant_admin(0)
    user_entity: UserEntity = user_service.register(valid_user_info)
    user_service.grant_admin(user_entity.uid)
    assert user_service.get_by_username(valid_user_info.username).info.role == UserRole.ADMIN
