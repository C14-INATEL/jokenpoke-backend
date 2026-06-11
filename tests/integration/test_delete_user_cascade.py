import pytest
from fastapi import status


@pytest.fixture
def registered_user_with_deck(client):
    response = client.post(
        "/auth/register",
        json={"username": "trainerwithdeck", "password": "poke123"},
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]

    users = client.get("/users/").json()
    user = next(u for u in users if u["username"] == "trainerwithdeck")
    user_id = user["id"]
    card_ids = [c["id"] for c in user["cards"][:3]]

    response = client.post(
        f"/decks/{user_id}/build",
        json={"pokemon_ids": card_ids},
    )
    assert response.status_code == status.HTTP_200_OK

    return {"id": user_id, "token": token}


class TestDeleteUserCascade:
    def test_delete_user_without_deck_returns_200(self, client):
        response = client.post(
            "/auth/register",
            json={"username": "nodecktrainer", "password": "poke123"},
        )
        assert response.status_code == status.HTTP_200_OK

        users = client.get("/users/").json()
        user = next(u for u in users if u["username"] == "nodecktrainer")
        user_id = user["id"]

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK

    def test_delete_user_with_deck_returns_200(self, client, registered_user_with_deck):
        user_id = registered_user_with_deck["id"]

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK

    def test_delete_user_removes_user_from_listing(
        self, client, registered_user_with_deck
    ):
        user_id = registered_user_with_deck["id"]

        client.delete(f"/users/{user_id}")

        users = client.get("/users/").json()
        deleted = next((u for u in users if u["id"] == user_id), None)
        assert deleted is None

    def test_delete_user_removes_deck_entries(self, client, registered_user_with_deck):
        user_id = registered_user_with_deck["id"]

        user_before = client.get(f"/users/{user_id}").json()
        assert len(user_before["deck"]) > 0

        client.delete(f"/users/{user_id}")

        response = client.get(f"/users/{user_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_removes_cards(self, client, registered_user_with_deck):
        user_id = registered_user_with_deck["id"]

        user_before = client.get(f"/users/{user_id}").json()
        assert len(user_before["cards"]) > 0

        client.delete(f"/users/{user_id}")

        response = client.get(f"/users/{user_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_not_found_returns_404(self, client):
        response = client.delete("/users/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
