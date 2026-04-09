from app.domain.entities.pokemon import Pokemon
from app.domain.entities.card import Card

def test_pokemon_instanciacao():
    
    pokemon = Pokemon(
        id=1,
        original_name="Pikachu",
        name="Pikachu",
        move="Choque do Trovão",
        description="Rato elétrico clássico."
    )
    

    assert pokemon.id == 1
    assert pokemon.original_name == "Pikachu"
    assert pokemon.name == "Pikachu"
    assert pokemon.move == "Choque do Trovão"
    assert pokemon.description == "Rato elétrico clássico."


def test_card_name_property():
    
    charmander = Pokemon(
        id=4,
        original_name="Charmander",
        name="Charmander",
        move="Brasa",
        description="Lagarto de fogo."
    )
    card = Card(pokemon=charmander, owner_id=10)
    
  
    assert card.name == "Charmander"