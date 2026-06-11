from fastapi import status


class TestGetAllPokemons:
    def test_get_all_pokemons_returns_200(self, client):
        response = client.get("/pokemons/")

        assert response.status_code == status.HTTP_200_OK

    def test_get_all_pokemons_returns_list(self, client):
        response = client.get("/pokemons/")

        body = response.json()
        assert isinstance(body, list)
        assert len(body) > 0

    def test_get_all_pokemons_response_structure(self, client):
        response = client.get("/pokemons/")

        body = response.json()
        first = body[0]
        assert "id" in first
        assert "name" in first
        assert "move" in first
        assert "description" in first
