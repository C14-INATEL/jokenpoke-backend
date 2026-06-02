class TestRegister:
    def test_register_success(self, client):
        response = client.post(
            "/auth/register",
            json={"username": "pikachu", "password": "thunderbolt123"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["message"] == "Usuário registrado com sucesso"
        assert "access_token" in body
        assert isinstance(body["access_token"], str)
        assert len(body["access_token"]) > 0

    def test_register_duplicate_username_returns_error(self, client):
        payload = {"username": "charmander", "password": "fire123"}

        first = client.post("/auth/register", json=payload)
        assert first.status_code == 200

        second = client.post("/auth/register", json=payload)
        assert second.status_code == 400
        assert "detail" in second.json()


class TestLogin:
    def test_login_success(self, client):
        client.post(
            "/auth/register",
            json={"username": "squirtle", "password": "watergun99"},
        )

        response = client.post(
            "/auth/login",
            data={"username": "squirtle", "password": "watergun99"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["message"] == "Login realizado com sucesso"
        assert "access_token" in body
        assert isinstance(body["access_token"], str)
        assert len(body["access_token"]) > 0

    def test_login_wrong_password_returns_401(self, client):
        client.post(
            "/auth/register",
            json={"username": "bulbasaur", "password": "vine123"},
        )

        response = client.post(
            "/auth/login",
            data={"username": "bulbasaur", "password": "senhaerrada"},
        )
        assert response.status_code == 401

    def test_login_user_not_found_returns_401(self, client):
        response = client.post(
            "/auth/login",
            data={"username": "naoexiste", "password": "qualquer"},
        )
        assert response.status_code == 401
