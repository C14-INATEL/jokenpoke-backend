from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest
from jose import jwt

from app.infrastructure.security.jwt_handler import create_token, decode_token
from app.shared.exceptions.unauthorized_exception import UnauthorizedException

FAKE_SECRET = "test-secret"
FAKE_ALGORITHM = "HS256"

mock_settings = {
    "app.infrastructure.security.jwt_handler.settings.jwt_secret_key": FAKE_SECRET,
    "app.infrastructure.security.jwt_handler.settings.jwt_algorithm": FAKE_ALGORITHM,
}


@pytest.fixture(autouse=True)
def patch_settings():
    with patch.multiple(
        "app.infrastructure.security.jwt_handler.settings",
        jwt_secret_key=FAKE_SECRET,
        jwt_algorithm=FAKE_ALGORITHM,
    ):
        yield


class TestCreateToken:
    def test_retorna_token_valido(self):
        token = create_token(user_id=1)
        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_contem_user_id_correto(self):
        token = create_token(user_id=42)
        payload = jwt.decode(token, FAKE_SECRET, algorithms=[FAKE_ALGORITHM])
        assert payload["sub"] == "42"

    def test_token_contem_expiracao(self):
        before = datetime.now(UTC)
        token = create_token(user_id=1)
        payload = jwt.decode(token, FAKE_SECRET, algorithms=[FAKE_ALGORITHM])

        exp = datetime.fromtimestamp(payload["exp"], tz=UTC)
        assert exp > before + timedelta(hours=1, minutes=59)

    def test_user_ids_diferentes_geram_tokens_diferentes(self):
        token_1 = create_token(user_id=1)
        token_2 = create_token(user_id=2)
        assert token_1 != token_2


class TestDecodeToken:
    def test_decodifica_token_valido(self):
        token = create_token(user_id=7)
        result = decode_token(token)
        assert result == 7

    def test_lanca_excecao_para_token_invalido(self):
        with pytest.raises(UnauthorizedException):
            decode_token("token.invalido.aqui")

    def test_lanca_excecao_para_token_expirado(self):
        payload = {
            "sub": "1",
            "exp": datetime.now(UTC) - timedelta(hours=1),
        }
        expired_token = jwt.encode(payload, FAKE_SECRET, algorithm=FAKE_ALGORITHM)

        with pytest.raises(UnauthorizedException):
            decode_token(expired_token)

    def test_lanca_excecao_para_token_sem_sub(self):
        payload = {"exp": datetime.now(UTC) + timedelta(hours=2)}
        token_sem_sub = jwt.encode(payload, FAKE_SECRET, algorithm=FAKE_ALGORITHM)

        with pytest.raises(UnauthorizedException):
            decode_token(token_sem_sub)

    def test_lanca_excecao_para_token_assinado_com_secret_errado(self):
        payload = {"sub": "1", "exp": datetime.now(UTC) + timedelta(hours=2)}
        token_errado = jwt.encode(payload, "secret-errado", algorithm=FAKE_ALGORITHM)

        with pytest.raises(UnauthorizedException):
            decode_token(token_errado)
