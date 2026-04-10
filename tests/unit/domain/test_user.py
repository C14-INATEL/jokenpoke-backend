from app.domain.entities.pokemon import Pokemon
from app.domain.entities.card import Card
from app.domain.entities.deck import Deck
from app.domain.entities.user import User


def test_user_has_deck_falso():

    user = User(id=1, username="christian")

    assert user.has_deck() == False


def test_user_has_deck_verdadeiro():

    charizard = Pokemon(id=6, original_name="Charizard", name="Charizard", move="tesoura", description="Cospe fogo.")
    pikachu = Pokemon(id=25, original_name="Pikachu", name="Pikachu", move="Choque do Trovão", description="Rato elétrico.")
    mewtwo = Pokemon(id=150, original_name="Mewtwo", name="Mewtwo", move="Psíquico", description="Criado por engenharia genética.")

    cards = [
        Card(pokemon=charizard, owner_id=1),
        Card(pokemon=pikachu, owner_id=1),
        Card(pokemon=mewtwo, owner_id=1),
    ]
    deck = Deck(cards=cards)

    user = User(id=1, username="christian", deck=deck)

    assert user.has_deck() == True
