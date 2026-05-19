import pytest
from pydantic import ValidationError

from app.schemas.deck_schema import BuildDeckRequest


def test_build_deck_request_sucesso():

    request = BuildDeckRequest(pokemon_ids=[10, 20, 30])

    assert request.pokemon_ids == [10, 20, 30]
    assert len(request.pokemon_ids) == 3


def test_build_deck_request_falha_tamanho_menor():

    with pytest.raises(ValidationError):
        BuildDeckRequest(pokemon_ids=[10, 20])


def test_build_deck_request_falha_tamanho_maior():

    with pytest.raises(ValidationError):
        BuildDeckRequest(pokemon_ids=[10, 20, 30, 40])
