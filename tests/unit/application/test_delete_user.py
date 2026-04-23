import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from app.application.use_cases.delete_user import DeleteUserUseCase
from app.shared.exceptions.not_found_exception import NotFoundException

class TestDeleteUserUseCase:

    def test_delete_user_mock_success(self):
        db_mock = MagicMock(spec=Session)
        use_case = DeleteUserUseCase(db=db_mock)
        
        use_case.user_repo = MagicMock()

        usuario_falso = MagicMock()
        usuario_falso.username = "Ash Ketchum"
        
        use_case.user_repo.get_by_id.return_value = usuario_falso

        resultado = use_case.execute(user_id=1)

        assert resultado == "Ash Ketchum"
        
        use_case.user_repo.get_by_id.assert_called_once_with(1)
        
        use_case.user_repo.delete.assert_called_once_with(1)


    def test_delete_user_mock_not_found(self):
        db_mock = MagicMock(spec=Session)
        use_case = DeleteUserUseCase(db=db_mock)
        
        use_case.user_repo = MagicMock()
        
        use_case.user_repo.get_by_id.return_value = None

        with pytest.raises(NotFoundException, match="Usuário com ID 99 não encontrado."):
            use_case.execute(user_id=99)

        use_case.user_repo.delete.assert_not_called()