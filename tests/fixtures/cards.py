# tests/fixtures/cards.py
import pytest
from app.domain.entities.pokemon import Pokemon
from app.domain.entities.card import Card

@pytest.fixture
def charizard_pokemon():
    return Pokemon(
        id=6,
        original_name="Charizard",
        name="Charizard",
        move="tesoura",
        description="Spits fire that is hot enough to melt boulders. Known to cause forest fires unintentionally."
    )

@pytest.fixture
def pikachu_pokemon():
    return Pokemon(
        id=25,
        original_name="Pikachu",
        name="Pikachu",
        move="fogo",
        description="When several of these Pokémon gather, their electricity could build and cause lightning storms."
    )

@pytest.fixture
def mewtwo_pokemon():
    return Pokemon(
        id=150,
        original_name="Mewtwo",
        name="Mewtwo",
        move="agua",
        description="It was created by a scientist after years of horrific gene splicing and DNA engineering experiments."
    )

@pytest.fixture
def valid_cards_list(charizard_pokemon, pikachu_pokemon, mewtwo_pokemon):
    """Retorna uma lista com exatamente 3 cartas válidas."""
    return [
        Card(pokemon=charizard_pokemon, owner_id=1),
        Card(pokemon=pikachu_pokemon, owner_id=1),
        Card(pokemon=mewtwo_pokemon, owner_id=1)
    ]