from app.domain.entities.battle import BattleResult, RoundResult
from app.domain.entities.user import User
from app.domain.rules.battle_rules import resolve_move
from app.shared.exceptions.domain_exception import DomainException


class StartBattleUseCase:
    def execute(
        self,
        attacker: User,
        defender: User,
    ) -> BattleResult:

        if not attacker.has_deck() or not defender.has_deck():
            raise ValueError("Ambos os jogadores precisam ter deck.")

        if attacker.deck is None or defender.deck is None:
            raise DomainException("Deck não encontrado.")

        attacker_wins = 0
        defender_wins = 0
        rounds = []

        for i in range(3):
            if attacker_wins == 2 or defender_wins == 2:
                break

            attacker_card = attacker.deck.get_card(i)
            defender_card = defender.deck.get_random_card()

            result = resolve_move(attacker_card.move, defender_card.move)

            if result == 1:
                attacker_wins += 1
                winner = "attacker"
            elif result == 2:
                defender_wins += 1
                winner = "defender"
            else:
                winner = "draw"

            rounds.append(
                RoundResult(
                    round_number=i + 1,
                    attacker_card=attacker_card.name,
                    defender_card=defender_card.name,
                    winner=winner,
                )
            )

        if attacker_wins > defender_wins:
            final_winner = "attacker"
        elif defender_wins > attacker_wins:
            final_winner = "defender"
        else:
            final_winner = "draw"

        return BattleResult(rounds=rounds, winner=final_winner)
