import pytest
from app.domain.entities.deck import Deck

def test_deck_criacao_com_3_cartas(valid_cards_list):
    meu_deck = Deck(cards=valid_cards_list)
    
    assert len(meu_deck.cards) == 3
    assert meu_deck.cards == valid_cards_list

def test_deck_erro_com_2_cartas(valid_cards_list):
    cartas_incompletas = valid_cards_list[:2] 

    with pytest.raises(ValueError, match="Um deck deve ter exatamente 3 cartas."):
        Deck(cards=cartas_incompletas)

def test_deck_erro_com_4_cartas(valid_cards_list):
    cartas_excesso = valid_cards_list + [valid_cards_list[0]]
    
    with pytest.raises(ValueError, match="Um deck deve ter exatamente 3 cartas."):
        Deck(cards=cartas_excesso)

def test_deck_get_card_primeira_posicao(valid_cards_list):
    meu_deck = Deck(cards=valid_cards_list)
    
    primeira_carta_buscada = meu_deck.get_card(0)
    
    assert primeira_carta_buscada == valid_cards_list[0]
    assert primeira_carta_buscada.pokemon.id == 6

def test_deck_get_random_card_pertence_ao_deck(valid_cards_list):
    meu_deck = Deck(cards=valid_cards_list)
    
    carta_aleatoria = meu_deck.get_random_card()
    
    assert carta_aleatoria in meu_deck.cards

def test_deck_get_card_fora_do_limite(valid_cards_list):
    meu_deck = Deck(cards=valid_cards_list)
    
    with pytest.raises(IndexError):
        meu_deck.get_card(5)