from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from app.application.use_cases.update_user import UpdateUserUseCase


def test_update_user_success_mock():
    db_mock = MagicMock(spec=Session)
    use_case = UpdateUserUseCase(db=db_mock)

    use_case.user_repo = MagicMock()

    # Mock do usuário atual retornado por get_by_id
    usuario_atual = MagicMock()
    usuario_atual.id = 1
    usuario_atual.username = "Ash Ketchum"
    use_case.user_repo.get_by_id.return_value = usuario_atual

    # Mock do usuário atualizado retornado por update
    usuario_atualizado = MagicMock()
    usuario_atualizado.id = 1
    usuario_atualizado.username = "Satoshi"
    use_case.user_repo.update.return_value = usuario_atualizado

    resultado = use_case.execute(user_id=1, username="Satoshi")

    # Verifica se retornou os dados atualizados
    assert resultado == {"id": 1, "username": "Satoshi"}

    # Verifica se get_by_id foi chamado para buscar o usuário
    use_case.user_repo.get_by_id.assert_called_once_with(1)

    # Verifica se update foi chamado com os dados corretos (novo username)
    use_case.user_repo.update.assert_called_once_with(1, "Satoshi")
