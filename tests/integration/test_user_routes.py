def _register_user(client, username: str) -> dict:
    response = client.post(
        "/auth/register",
        json={"username": username, "password": "poke12345"},
    )
    assert response.status_code == 200

    users = client.get("/users/").json()
    user = next(u for u in users if u["username"] == username)

    return {
        "id": user["id"],
        "token": response.json()["access_token"],
        "cards": user["cards"],
    }


class TestGetAllUsers:
    def test_get_all_users_returns_200_and_list(self, client):
        _register_user(client, "users_list_one")
        _register_user(client, "users_list_two")

        response = client.get("/users/")

        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, list)
        assert len(body) == 2

    def test_get_all_users_response_structure(self, client):
        _register_user(client, "users_structure")

        response = client.get("/users/")

        assert response.status_code == 200
        user = response.json()[0]
        assert set(user.keys()) == {
            "id",
            "username",
            "points",
            "rank",
            "cards",
            "deck",
        }
        assert isinstance(user["cards"], list)
        assert isinstance(user["deck"], list)


class TestGetUserById:
    def test_get_user_by_id_success(self, client):
        user = _register_user(client, "get_user_success")

        response = client.get(f"/users/{user['id']}")

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == user["id"]
        assert body["username"] == "get_user_success"
        assert body["points"] == 0
        assert body["rank"] == "Beginner"
        assert isinstance(body["cards"], list)
        assert isinstance(body["deck"], list)

    def test_get_user_by_id_not_found_returns_404(self, client):
        response = client.get("/users/99999")

        assert response.status_code == 404
        assert "detail" in response.json()


class TestDeleteUser:
    def test_delete_user_success(self, client):
        user = _register_user(client, "delete_user_success")

        response = client.delete(f"/users/{user['id']}")

        assert response.status_code == 200
        assert "delete_user_success" in response.json()["message"]

        get_response = client.get(f"/users/{user['id']}")
        assert get_response.status_code == 404

    def test_delete_user_not_found_returns_404(self, client):
        response = client.delete("/users/99999")

        assert response.status_code == 404
        assert "detail" in response.json()
