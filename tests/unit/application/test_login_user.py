import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from app.application.use_cases.login_user import LoginUserUseCase
from app.shared.exceptions.unauthorized_exception import UnauthorizedException


def test_login_user_invalid_password_mock():
    db_mock = MagicMock(spec=Session)
    use_case = LoginUserUseCase(db=db_mock)

    use_case.user_repo = MagicMock()

    # Usuário válido simulado retornado por get_by_username
    usuario_mock = MagicMock()
    usuario_mock.id = 1
    usuario_mock.username = "Ash Ketchum"
    usuario_mock.password = "hashed_password"
    use_case.user_repo.get_by_username.return_value = usuario_mock

    with patch("app.application.use_cases.login_user.verify_password", return_value=False), \
         patch("app.application.use_cases.login_user.create_token") as mock_create_token:

        # Verifica que levanta exceção de acesso negado
        with pytest.raises(UnauthorizedException, match="Credenciais inválidas"):
            use_case.execute("Ash Ketchum", "senha_errada")

        # Garante que o token JWT nunca foi gerado
        mock_create_token.assert_not_called()
