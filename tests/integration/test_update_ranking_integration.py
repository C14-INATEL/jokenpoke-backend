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


def _build_deck(client, user: dict) -> None:
    pokemon_ids = [card["id"] for card in user["cards"][:3]]

    response = client.post(
        f"/decks/{user['id']}/build",
        json={"pokemon_ids": pokemon_ids},
    )

    assert response.status_code == 200


def _auth_headers(user: dict) -> dict:
    return {"Authorization": f"Bearer {user['token']}"}


class TestUpdateRankingIntegration:
    def test_battle_returns_ranking_data_in_response(self, client):
        """Verifica que a resposta da batalha inclui dados de ranking."""
        attacker = _register_user(client, "rank_attacker")
        defender = _register_user(client, "rank_defender")
        _build_deck(client, attacker)
        _build_deck(client, defender)

        response = client.post(
            f"/battle/{defender['id']}",
            headers=_auth_headers(attacker),
        )

        assert response.status_code == 200
        body = response.json()

        assert "ranking" in body
        ranking = body["ranking"]
        assert set(ranking.keys()) == {
            "old_rank",
            "new_rank",
            "old_points",
            "new_points",
            "status",
            "message",
        }
        assert ranking["old_rank"] == "Beginner"
        assert ranking["old_points"] == 0

    def test_ranking_points_update_after_battle(self, client):
        """
        Verifica que os pontos do atacante são atualizados no banco
        de dados após uma batalha, consultando o endpoint GET /ranking/.
        """
        attacker = _register_user(client, "pts_attacker")
        defender = _register_user(client, "pts_defender")
        _build_deck(client, attacker)
        _build_deck(client, defender)

        ranking_before = client.get("/ranking/").json()
        attacker_before = next(
            u for u in ranking_before if u["username"] == "pts_attacker"
        )
        initial_points = attacker_before["points"]
        initial_rank = attacker_before["rank"]

        battle_response = client.post(
            f"/battle/{defender['id']}",
            headers=_auth_headers(attacker),
        )
        assert battle_response.status_code == 200
        battle_ranking = battle_response.json()["ranking"]

        ranking_after = client.get("/ranking/").json()
        attacker_after = next(
            u for u in ranking_after if u["username"] == "pts_attacker"
        )

        assert attacker_after["points"] == battle_ranking["new_points"]
        assert attacker_after["rank"] == battle_ranking["new_rank"]
        assert (
            attacker_after["points"] != initial_points
            or attacker_after["rank"] != initial_rank
            or battle_ranking["status"] == "maintained"
        )

    def test_ranking_status_reflects_match_outcome(self, client):
        """
        Verifica que o status do ranking (maintained/promoted/demoted)
        é coerente com o resultado da partida.
        """
        attacker = _register_user(client, "status_attacker")
        defender = _register_user(client, "status_defender")
        _build_deck(client, attacker)
        _build_deck(client, defender)

        response = client.post(
            f"/battle/{defender['id']}",
            headers=_auth_headers(attacker),
        )

        assert response.status_code == 200
        body = response.json()
        winner = body["winner"]
        ranking = body["ranking"]

        if winner == "attacker":
            assert (
                ranking["new_points"] > ranking["old_points"]
                or ranking["status"] == "promoted"
            )
        elif winner == "defender":
            assert (
                ranking["new_points"] < ranking["old_points"]
                or ranking["status"] == "demoted"
            )
        else:
            assert ranking["new_points"] == ranking["old_points"]
            assert ranking["status"] == "maintained"

    def test_multiple_battles_accumulate_ranking_changes(self, client):
        """
        Verifica que múltiplas batalhas acumulam as mudanças de ranking
        corretamente no banco de dados.
        """
        attacker = _register_user(client, "multi_attacker")
        defender = _register_user(client, "multi_defender")
        _build_deck(client, attacker)
        _build_deck(client, defender)

        previous_points = 0
        previous_rank = "Beginner"

        for _ in range(3):
            response = client.post(
                f"/battle/{defender['id']}",
                headers=_auth_headers(attacker),
            )
            assert response.status_code == 200

            ranking = response.json()["ranking"]
            assert ranking["old_points"] == previous_points
            assert ranking["old_rank"] == previous_rank

            previous_points = ranking["new_points"]
            previous_rank = ranking["new_rank"]

        ranking_final = client.get("/ranking/").json()
        attacker_final = next(
            u for u in ranking_final if u["username"] == "multi_attacker"
        )

        assert attacker_final["points"] == previous_points
        assert attacker_final["rank"] == previous_rank
