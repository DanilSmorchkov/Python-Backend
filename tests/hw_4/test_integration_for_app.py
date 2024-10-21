import pytest
from fastapi.testclient import TestClient
from faker import Faker
from http import HTTPStatus
from urllib.error import HTTPError

from hw_4_tests.demo_service.api.main import create_app
from hw_4_tests.demo_service.core import users

faker = Faker()


@pytest.fixture()
def demo_service():
    app = create_app()
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def create_users(demo_service):
    users = [
        {
            'username': faker.user_name(),
            'name': faker.name(),
            'birthdate': faker.date_time().isoformat(),
            'password': faker.password()
        }
        for _ in range(10)
    ]
    return [demo_service.post("/user-register", json=user).json() for user in users]


def test_post_users(demo_service):
    user = {
        'username': faker.user_name(),
        'name': faker.name(),
        'birthdate': faker.date_time().isoformat(),
        'password': faker.password()
    }
    response = demo_service.post("/user-register", json=user)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['username'] == user['username']
    assert data['name'] == user['name']
    assert data['birthdate'] == user['birthdate']
    assert data['role'] == users.UserRole.USER


def test_get_users(demo_service, create_users):
    # id
    for i in range(2, 12):
        response = demo_service.post("/user-get", params={'id': i}, auth=('admin', 'superSecretAdminPassword123'))
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data['uid'] == i
        assert data['username'] == create_users[i-2]['username']
        assert data['name'] == create_users[i-2]['name']
        assert data['birthdate'] == create_users[i-2]['birthdate']

    # username
    for i in range(2, 12):
        response = demo_service.post("/user-get", params={'username': create_users[i-2]['username']},
                                     auth=('admin', 'superSecretAdminPassword123'))
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data['uid'] == i
        assert data['username'] == create_users[i-2]['username']
        assert data['name'] == create_users[i-2]['name']
        assert data['birthdate'] == create_users[i-2]['birthdate']

    # id and username

    response = demo_service.post("/user-get", params={'username': faker.user_name(), 'id': 4},
                          auth=('admin', 'superSecretAdminPassword123'))
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # not id or username
    response = demo_service.post("/user-get", params={},
                                 auth=('admin', 'superSecretAdminPassword123'))
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # not found
    response = demo_service.post("/user-get", params={'id': 15},
                                 auth=('admin', 'superSecretAdminPassword123'))
    assert response.status_code == HTTPStatus.NOT_FOUND

    # uncorrected password
    response = demo_service.post("/user-get", params={'id': 4},
                                 auth=('admin', 'superSecretAdminPassword'))
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_promote_user(demo_service, create_users):
    for i in range(2, 12):
        response = demo_service.post("/user-promote", params={'id': i},
                                     auth=('admin', 'superSecretAdminPassword123'))
        assert response.status_code == HTTPStatus.OK

    # not admin
    user = {
        'username': faker.user_name(),
        'name': faker.name(),
        'birthdate': faker.date_time().isoformat(),
        'password': faker.password()
    }
    response = demo_service.post("/user-register", json=user)
    assert response.status_code == HTTPStatus.OK

    response = demo_service.post("/user-promote", params={'id': 4},
                                 auth=(user['username'], user['password']))
    assert response.status_code == HTTPStatus.FORBIDDEN
