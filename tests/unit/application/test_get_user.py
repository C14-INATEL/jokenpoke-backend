import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from app.application.use_cases.get_user_by_id import GetUserByIdUseCase
from app.application.use_cases.get_all_users import GetAllUsersUseCase
from app.shared.exceptions.not_found_exception import NotFoundException


class TestGetUserByIdUseCase:

    def test_get_user_by_id_mock_success(self):
        # Arrange: Criação dos mocks da sessão de banco e do caso de uso
        db_mock = MagicMock(spec=Session)
        use_case = GetUserByIdUseCase(db=db_mock)

        use_case.user_repo = MagicMock()
        use_case.pokemon_repo = MagicMock()

        # Simulando Pokémon fictícios que o pokemon_repo devolveria
        poke_bulbasaur = MagicMock()
        poke_bulbasaur.id = 1
        poke_bulbasaur.name = "Bulbasaur"
        poke_bulbasaur.move = "Razor Leaf"
        poke_bulbasaur.description = "Pokémon planta"

        poke_charmander = MagicMock()
        poke_charmander.id = 4
        poke_charmander.name = "Charmander"
        poke_charmander.move = "Ember"
        poke_charmander.description = "Pokémon fogo"

        # Simulando as cartas do usuário (collection)
        carta1 = MagicMock()
        carta1.id = 101
        carta1.pokemon_id = 1

        carta2 = MagicMock()
        carta2.id = 102
        carta2.pokemon_id = 4

        # Simulando o item de deck (referencia carta1)
        deck_item = MagicMock()
        deck_item.card_id = 101

        # Simulando o usuário retornado pelo repositório
        usuario_falso = MagicMock()
        usuario_falso.id = 10
        usuario_falso.username = "Ash Ketchum"
        usuario_falso.cards = [carta1, carta2]
        usuario_falso.deck = [deck_item]

        use_case.user_repo.get_by_id_with_relations.return_value = usuario_falso

        # pokemon_repo.get_by_id devolve o Pokémon correto por ID
        def pokemon_por_id(pokemon_id):
            return {1: poke_bulbasaur, 4: poke_charmander}.get(pokemon_id)

        use_case.pokemon_repo.get_by_id.side_effect = pokemon_por_id

        # Act
        resultado = use_case.execute(user_id=10)

        # Assert: chaves obrigatórias no dicionário retornado
        assert "id" in resultado
        assert "username" in resultado
        assert "collection" in resultado
        assert "deck" in resultado

        assert resultado["id"] == 10
        assert resultado["username"] == "Ash Ketchum"

        # Verifica que a collection foi preenchida com os atributos corretos
        assert len(resultado["collection"]) == 2
        assert resultado["collection"][0]["name"] == "Bulbasaur"
        assert resultado["collection"][0]["move"] == "Razor Leaf"
        assert resultado["collection"][0]["description"] == "Pokémon planta"
        assert resultado["collection"][1]["name"] == "Charmander"

        # Verifica que o deck foi preenchido corretamente (apenas carta1 está no deck)
        assert len(resultado["deck"]) == 1
        assert resultado["deck"][0]["name"] == "Bulbasaur"
        assert resultado["deck"][0]["move"] == "Razor Leaf"
        assert resultado["deck"][0]["description"] == "Pokémon planta"

        use_case.user_repo.get_by_id_with_relations.assert_called_once_with(10)
        
    def test_get_user_by_id_not_found_mock(self):
        db_mock = MagicMock(spec=Session)
        use_case = GetUserByIdUseCase(db=db_mock)
        use_case.user_repo = MagicMock()
        
        # Mock: Repositório retornando None para um ID inexistente
        use_case.user_repo.get_by_id_with_relations.return_value = None

        # Act & Assert: Garante que a exceção NotFoundException é lançada
        with pytest.raises(NotFoundException):
            use_case.execute(user_id=999)

class TestGetAllUsersUseCase:

    def test_get_all_users_mock(self):
        db_mock = MagicMock(spec=Session)
        use_case = GetAllUsersUseCase(db=db_mock)
        use_case.user_repo = MagicMock()

        u1 = MagicMock()
        u1.id = 1
        u1.username = "Red"
        u1.cards = []
        u1.deck = []

        u2 = MagicMock()
        u2.id = 2
        u2.username = "Blue"
        u2.cards = []
        u2.deck = []

        use_case.user_repo.get_all_with_relations.return_value = [u1, u2]

        resultado = use_case.execute()

        assert isinstance(resultado, list)
        assert len(resultado) == 2
        
        # Verifica formatação do primeiro usuário
        assert resultado[0]["id"] == 1
        assert resultado[0]["username"] == "Red"
        
        # Verifica formatação do segundo usuário
        assert resultado[1]["id"] == 2
        assert resultado[1]["username"] == "Blue"

        use_case.user_repo.get_all_with_relations.assert_called_once()