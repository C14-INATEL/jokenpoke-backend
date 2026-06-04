import pytest


@pytest.fixture
def registered_user_with_deck(client):
    response = client.post(
        "/auth/register",
        json={"username": "trainerwithdeck", "password": "poke123"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    users = client.get("/users/").json()
    user = next(u for u in users if u["username"] == "trainerwithdeck")
    user_id = user["id"]
    card_ids = [c["id"] for c in user["cards"][:3]]

    response = client.post(
        f"/decks/{user_id}/build",
        json={"pokemon_ids": card_ids},
    )
    assert response.status_code == 200

    return {"id": user_id, "token": token}


class TestDeleteUserCascade:
    def test_delete_user_without_deck_returns_200(self, client):
        response = client.post(
            "/auth/register",
            json={"username": "nodecktrainer", "password": "poke123"},
        )
        assert response.status_code == 200

        users = client.get("/users/").json()
        user = next(u for u in users if u["username"] == "nodecktrainer")
        user_id = user["id"]

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200

    def test_delete_user_with_deck_returns_200(self, client, registered_user_with_deck):
        user_id = registered_user_with_deck["id"]

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200

    def test_delete_user_with_deck_removes_deck_entries(self, client, registered_user_with_deck):
        user_id = registered_user_with_deck["id"]

        client.delete(f"/users/{user_id}")

        users = client.get("/users/").json()
        deleted = next((u for u in users if u["id"] == user_id), None)
        assert deleted is None

    def test_delete_user_not_found_returns_404(self, client):
        response = client.delete("/users/99999")
        assert response.status_code == 404