import pytest
from fastapi import status


@pytest.fixture
def registered_user(client):
    response = client.post(
        "/auth/register",
        json={"username": "decktrainer", "password": "poke123"},
    )
    assert response.status_code == status.HTTP_200_OK

    token = response.json()["access_token"]

    users = client.get("/users/").json()
    user = next(u for u in users if u["username"] == "decktrainer")

    return {"id": user["id"], "token": token, "cards": user["cards"]}


class TestBuildDeck:
    def test_build_deck_success(self, client, registered_user):
        user_id = registered_user["id"]
        pokemon_ids = [c["id"] for c in registered_user["cards"][:3]]

        response = client.post(
            f"/decks/{user_id}/build",
            json={"pokemon_ids": pokemon_ids},
        )

        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
        assert "decktrainer" in response.json()["message"]

    def test_build_deck_user_not_found_returns_404(self, client):
        response = client.post(
            "/decks/99999/build",
            json={"pokemon_ids": [1, 2, 3]},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_build_deck_pokemon_not_owned_returns_400(self, client, registered_user):
        user_id = registered_user["id"]
        owned_ids = {c["id"] for c in registered_user["cards"]}

        all_pokemons = client.get("/pokemons/").json()
        unowned = [p["id"] for p in all_pokemons if p["id"] not in owned_ids]

        response = client.post(
            f"/decks/{user_id}/build",
            json={"pokemon_ids": unowned[:3]},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_build_deck_wrong_size_returns_422(self, client, registered_user):
        user_id = registered_user["id"]

        response = client.post(
            f"/decks/{user_id}/build",
            json={"pokemon_ids": [1, 2]},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
