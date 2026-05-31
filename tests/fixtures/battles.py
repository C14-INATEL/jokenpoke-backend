# tests/fixtures/battles.py
from unittest.mock import MagicMock

import pytest

from app.domain.entities.card import Card
from app.domain.entities.deck import Deck
from app.domain.entities.pokemon import Pokemon
from app.domain.entities.user import User


# ---------------------------------------------------------------------------
# Helpers (funções livres — não são fixtures, mas são usadas por elas)
# ---------------------------------------------------------------------------

def make_pokemon(name: str, move: str, pid: int = 1) -> Pokemon:
    return Pokemon(id=pid, original_name=name, name=name, move=move, description="")


def make_card(name: str, move: str, owner_id: int = 1, pid: int = 1) -> Card:
    return Card(pokemon=make_pokemon(name, move, pid), owner_id=owner_id)


def make_deck(moves: list[str], owner_id: int = 1) -> Deck:
    cards = [
        make_card(f"Pokemon{i}", move, owner_id, i)
        for i, move in enumerate(moves, 1)
    ]
    return Deck(cards=cards)


def make_user(uid: int, has_deck: bool = True, deck: Deck | None = None) -> MagicMock:
    user = MagicMock(spec=User)
    user.id = uid
    user.has_deck.return_value = has_deck
    user.deck = deck
    return user


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def attacker_deck():
    return make_deck(["pedra", "papel", "tesoura"], owner_id=1)


@pytest.fixture
def defender_deck():
    return make_deck(["pedra", "papel", "tesoura"], owner_id=2)


@pytest.fixture
def attacker(attacker_deck):
    return make_user(uid=1, has_deck=True, deck=attacker_deck)


@pytest.fixture
def defender(defender_deck):
    return make_user(uid=2, has_deck=True, deck=defender_deck)