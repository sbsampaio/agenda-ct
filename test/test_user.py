from http import HTTPStatus


def test_create_user(client):
    response = client.post("/users/", json={
        "first_name": "Alice",
        "last_name": "Wonderland",
        "email": "alice@example.com",
        "password": "secret"
    })
    assert response.status_code == HTTPStatus.CREATED


def test_create_user_with_already_existing_email(client, user):
    response = client.post("/users/", json={
        "first_name": "Bob",
        "last_name": "Builder",
        "email": user.email,
        "password": "anothersecret"
    })
    assert response.status_code == HTTPStatus.CONFLICT
    
    response_data = response.json()
    
    assert "detail" in response_data
    assert response.json() == {"detail": "Email already registered"}


def test_update_email_already_existing(client, user, token):
    client.post(
        "/users/", json={
            "first_name": "Bob",
            "last_name": "Builder",
            "email": "bob@example.com",
            "password": "anothersecret"
        }
    )

    response_update = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "first_name": "erick",
            "last_name": "silva",
            "email": "bob@example.com",
            "password": "mynewpassword",
        }
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {"detail": "Email already registered"}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "first_name": "bob",
            "last_name": "builder",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.OK


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "first_name": "bob",
            "last_name": "builder",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_wrong_user(client, other_user, token):
    response = client.delete(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}