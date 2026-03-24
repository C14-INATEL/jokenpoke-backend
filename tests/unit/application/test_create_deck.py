# tests/unit/application/test_create_deck.py
import pytest
from app.application.use_cases.create_deck import CreateDeckUseCase

class TestCreateDeckUseCase:
    
    def test_execute_with_exactly_three_cards_should_create_deck(self, valid_cards_list):
        use_case = CreateDeckUseCase()

        deck = use_case.execute(valid_cards_list)

        assert len(deck.cards) == 3
        assert deck.cards[0].name == "Charizard"
        assert deck.cards[1].pokemon.original_name == "Pikachu"

    def test_execute_with_insufficient_cards_should_raise_error(self, valid_cards_list):
        use_case = CreateDeckUseCase()
        insufficient_cards = valid_cards_list[:2]

        with pytest.raises(ValueError, match="O deck deve ter exatamente 3 cartas."):
            use_case.execute(insufficient_cards)