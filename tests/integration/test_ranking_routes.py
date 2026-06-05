def _register_user(client, username: str) -> dict:
    response = client.post(
        "/auth/register",
        json={"username": username, "password": "poke12345"},
    )
    assert response.status_code == 200
    return response.json()


class TestGetRanking:
    def test_ranking_with_users_returns_200_and_sorted_list(self, client):
        # Criação de usuários (pontos iniciais são 0)
        _register_user(client, "user_one")
        _register_user(client, "user_two")

        response = client.get("/ranking/")
        assert response.status_code == 200
        
        body = response.json()
        assert isinstance(body, list)
        assert len(body) == 2
        
        # Como ambos têm 0 pontos, a ordenação de desempate é id ASC.
        # Mas vamos validar a ordenação geral descrescente de pontos de qualquer forma
        points = [user["points"] for user in body]
        assert points == sorted(points, reverse=True)

    def test_ranking_response_structure(self, client):
        _register_user(client, "user_structure")

        response = client.get("/ranking/")
        assert response.status_code == 200
        
        body = response.json()
        assert len(body) == 1
        
        user_ranking = body[0]
        assert set(user_ranking.keys()) == {
            "position",
            "username",
            "points",
            "rank",
        }
        assert user_ranking["username"] == "user_structure"
        assert isinstance(user_ranking["position"], int)
        assert isinstance(user_ranking["points"], int)
        assert isinstance(user_ranking["rank"], str)

    def test_ranking_position_assigned_correctly(self, client):
        # Registra 3 usuários. O desempate por id ASC garante a ordem de registro
        u1 = "first_user"
        u2 = "second_user"
        u3 = "third_user"
        
        _register_user(client, u1)
        _register_user(client, u2)
        _register_user(client, u3)

        response = client.get("/ranking/")
        assert response.status_code == 200
        
        body = response.json()
        assert len(body) == 3
        
        # Posições sequenciais corretas
        assert body[0]["position"] == 1
        assert body[1]["position"] == 2
        assert body[2]["position"] == 3
        
        # Usernames corretos seguindo a ordem de ID (ordem de inserção)
        assert body[0]["username"] == u1
        assert body[1]["username"] == u2
        assert body[2]["username"] == u3

    def test_ranking_empty_database_returns_200_and_empty_list(self, client):
        response = client.get("/ranking/")
        assert response.status_code == 200
        
        body = response.json()
        assert body == []
