from app.core.config import settings
from app.domain.entities.battle import BattleResult, RoundResult
from app.domain.entities.user import User
from app.domain.rules.battle_rules import (
    ATTACKER_WINS,
    DEFENDER_WINS,
    resolve_move,
    resolve_winner_label,
)
from app.shared.exceptions.domain_exception import DomainException

WINS_TO_FINISH = 2


class StartBattleUseCase:
    def execute(
        self,
        attacker: User,
        defender: User,
    ) -> BattleResult:
        self._validate_players(attacker, defender)

        attacker_deck = attacker.deck
        defender_deck = defender.deck

        attacker_wins = 0
        defender_wins = 0
        rounds: list[RoundResult] = []

        for index in range(min(settings.battle_rounds, len(attacker_deck.cards))):
            if attacker_wins == WINS_TO_FINISH or defender_wins == WINS_TO_FINISH:
                break

            attacker_card = attacker_deck.get_card(index)
            defender_card = defender_deck.get_random_card()

            result = resolve_move(attacker_card.move, defender_card.move)

            if result == ATTACKER_WINS:
                attacker_wins += 1
            elif result == DEFENDER_WINS:
                defender_wins += 1

            rounds.append(
                RoundResult(
                    round_number=index + 1,
                    attacker_card=attacker_card.name,
                    defender_card=defender_card.name,
                    winner=resolve_winner_label(result),
                    attacker_move=attacker_card.move,
                    defender_move=defender_card.move,
                )
            )

        final_winner = self._resolve_final_winner(attacker_wins, defender_wins)

        return BattleResult(rounds=rounds, winner=final_winner)

    def _validate_players(self, attacker: User, defender: User) -> None:
        if attacker.id == defender.id:
            raise DomainException("Um jogador nao pode batalhar contra si mesmo.")

        if not attacker.has_deck():
            raise DomainException("O atacante precisa ter deck.")

        if not defender.has_deck():
            raise DomainException("O defensor precisa ter deck.")

    def _resolve_final_winner(self, attacker_wins: int, defender_wins: int) -> str:
        if attacker_wins > defender_wins:
            return "attacker"

        if defender_wins > attacker_wins:
            return "defender"

        return "draw"
