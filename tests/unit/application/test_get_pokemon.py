import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

# Adaptando os imports para um caso de uso focado em buscar um Pokémon
from app.application.use_cases.get_pokemon import GetPokemonUseCase
from app.shared.exceptions.not_found_exception import NotFoundException

class TestGetPokemonUseCase:

    def test_get_pokemon_mock_success(self):
        # Arrange: Criação dos mocks da sessão de banco e do caso de uso
        db_mock = MagicMock(spec=Session)
        use_case = GetPokemonUseCase(db=db_mock)
        
        # Criação do mock do repositório
        use_case.pokemon_repo = MagicMock()

        # Simulando o objeto Pokémon que o banco retornaria
        pokemon_falso = MagicMock()
        pokemon_falso.name = "Pikachu"
        pokemon_falso.move = "Choque do Trovão"
        
        # Configurando o repositório para retornar o nosso mock
        use_case.pokemon_repo.get_by_id.return_value = pokemon_falso

        # Act: Executando o caso de uso
        resultado = use_case.execute(pokemon_id=25)

        # Assert: Verificações
        assert resultado.name == "Pikachu"
        assert resultado.move == "Choque do Trovão"
        
        # Garante que o repositório foi chamado corretamente com o ID 25
        use_case.pokemon_repo.get_by_id.assert_called_once_with(25)


    def test_get_pokemon_mock_not_found(self):
        # Arrange: Configuração dos mocks
        db_mock = MagicMock(spec=Session)
        use_case = GetPokemonUseCase(db=db_mock)
        
        use_case.pokemon_repo = MagicMock()
        
        # Configurando o repositório para retornar None (simulando que não achou no banco)
        use_case.pokemon_repo.get_by_id.return_value = None

        # Act & Assert: Validando se a exceção correta é lançada
        with pytest.raises(NotFoundException, match="Pokémon com ID 999 não encontrado."):
            use_case.execute(pokemon_id=999)

        # Garante que o método get_by_id foi de fato acionado para tentar a busca
        use_case.pokemon_repo.get_by_id.assert_called_once_with(999)