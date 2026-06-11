from fastapi import status


def _register_user(client, username: str) -> dict:
    response = client.post(
        "/auth/register",
        json={"username": username, "password": "poke12345"},
    )
    assert response.status_code == status.HTTP_200_OK

    users = client.get("/users/").json()
    user = next(u for u in users if u["username"] == username)

    return {
        "id": user["id"],
        "token": response.json()["access_token"],
        "cards": user["cards"],
    }


def _build_deck(client, user: dict) -> None:
    pokemon_ids = [card["id"] for card in user["cards"][:3]]

    response = client.post(
        f"/decks/{user['id']}/build",
        json={"pokemon_ids": pokemon_ids},
    )

    assert response.status_code == status.HTTP_200_OK


def _auth_headers(user: dict) -> dict:
    return {"Authorization": f"Bearer {user['token']}"}


class TestBattleRoutes:
    def test_battle_success_between_users_with_decks(self, client):
        attacker = _register_user(client, "battle_attacker")
        defender = _register_user(client, "battle_defender")
        _build_deck(client, attacker)
        _build_deck(client, defender)

        response = client.post(
            f"/battle/{defender['id']}",
            headers=_auth_headers(attacker),
        )

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert set(body.keys()) == {"rounds", "winner", "ranking", "reward_card"}
        assert body["winner"] in {"attacker", "defender", "draw"}
        assert isinstance(body["rounds"], list)
        assert len(body["rounds"]) > 0
        assert set(body["ranking"].keys()) == {
            "old_rank",
            "new_rank",
            "old_points",
            "new_points",
            "status",
            "message",
        }
        if body["reward_card"] is not None:
            assert set(body["reward_card"].keys()) == {
                "id",
                "name",
                "move",
                "description",
            }

        first_round = body["rounds"][0]
        assert set(first_round.keys()) == {
            "round_number",
            "attacker_card",
            "defender_card",
            "attacker_move",
            "defender_move",
            "winner",
        }
        assert first_round["winner"] in {"attacker", "defender", "draw"}

    def test_battle_attacker_without_deck_returns_domain_error(self, client):
        attacker = _register_user(client, "attacker_no_deck")
        defender = _register_user(client, "defender_with_deck")
        _build_deck(client, defender)

        response = client.post(
            f"/battle/{defender['id']}",
            headers=_auth_headers(attacker),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "deck" in response.json()["detail"].lower()

    def test_battle_defender_without_deck_returns_domain_error(self, client):
        attacker = _register_user(client, "attacker_with_deck")
        defender = _register_user(client, "defender_no_deck")
        _build_deck(client, attacker)

        response = client.post(
            f"/battle/{defender['id']}",
            headers=_auth_headers(attacker),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "deck" in response.json()["detail"].lower()

    def test_battle_against_self_returns_domain_error(self, client):
        attacker = _register_user(client, "self_battle_user")

        response = client.post(
            f"/battle/{attacker['id']}",
            headers=_auth_headers(attacker),
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "si mesmo" in response.json()["detail"]

    def test_battle_defender_not_found_returns_404(self, client):
        attacker = _register_user(client, "missing_defender_attacker")

        response = client.post(
            "/battle/99999",
            headers=_auth_headers(attacker),
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "detail" in response.json()
