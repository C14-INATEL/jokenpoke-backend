import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from app.application.use_cases.build_deck import BuildDeckUseCase
from app.shared.exceptions.domain_exception import DomainException

class TestBuildDeckUseCase:

    def test_build_deck_mock_success(self):
        db_mock = MagicMock(spec=Session)
        use_case = BuildDeckUseCase(db=db_mock)
        
        use_case.user_repo = MagicMock()
        use_case.deck_repo = MagicMock()

        usuario_falso = MagicMock()
        usuario_falso.username = "Ash Ketchum"
        
        carta1 = MagicMock(); carta1.pokemon_id = 1; carta1.id = 101   
        carta2 = MagicMock(); carta2.pokemon_id = 4; carta2.id = 102   
        carta3 = MagicMock(); carta3.pokemon_id = 7; carta3.id = 103  
        carta4 = MagicMock(); carta4.pokemon_id = 25; carta4.id = 104  
        carta5 = MagicMock(); carta5.pokemon_id = 133; carta5.id = 105 
        
        usuario_falso.cards = [carta1, carta2, carta3, carta4, carta5]
        
        use_case.user_repo.get_by_id_with_relations.return_value = usuario_falso

        resultado = use_case.execute(user_id=1, pokemon_ids=[1, 4, 7])

        assert resultado == "Ash Ketchum"
        
        use_case.user_repo.get_by_id_with_relations.assert_called_once_with(1)
        use_case.deck_repo.clear_user_deck.assert_called_once_with(1)
        
        use_case.deck_repo.save_deck.assert_called_once_with(1, [101, 102, 103])


    def test_build_deck_missing_pokemon_mock(self):
        db_mock = MagicMock(spec=Session)
        use_case = BuildDeckUseCase(db=db_mock)
        
        use_case.user_repo = MagicMock()
        use_case.deck_repo = MagicMock()

        usuario_falso = MagicMock()
        usuario_falso.username = "Misty"
        
        carta_agua_1 = MagicMock(); carta_agua_1.pokemon_id = 7  
        carta_agua_2 = MagicMock(); carta_agua_2.pokemon_id = 54 
        
        usuario_falso.cards = [carta_agua_1, carta_agua_2]
        
        use_case.user_repo.get_by_id_with_relations.return_value = usuario_falso

        with pytest.raises(DomainException, match="Você não possui o pokémon de ID 6."):
            use_case.execute(user_id=2, pokemon_ids=[6, 7, 54])
            
        use_case.deck_repo.save_deck.assert_not_called()