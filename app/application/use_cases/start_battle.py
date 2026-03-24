from app.domain.entities.user import User
from app.domain.rules.battle_rules import resolve_move


class StartBattleUseCase:

    def execute(self, jogador1: User, jogador2: User) -> str:

        if not jogador1.deck or not jogador2.deck:
            raise ValueError("Ambos os jogadores precisam ter um deck.")

        vitorias_j1 = 0
        vitorias_j2 = 0

        rodadas = []

        for i in range(3):

            if vitorias_j1 == 2 or vitorias_j2 == 2:
                break

            p1 = jogador1.deck[i]
            p2 = jogador2.deck[i]

            resultado = resolve_move(p1.move, p2.move)

            if resultado == 1:
                vitorias_j1 += 1
                rodadas.append(
                    f"Rodada {i+1}: {jogador1.name} vence com {p1.name}"
                )

            elif resultado == 2:
                vitorias_j2 += 1
                rodadas.append(
                    f"Rodada {i+1}: {jogador2.name} vence com {p2.name}"
                )

            else:
                rodadas.append(
                    f"Rodada {i+1}: Empate entre {p1.name} e {p2.name}"
                )

        if vitorias_j1 > vitorias_j2:
            vencedor = f"{jogador1.name} venceu a batalha"

        elif vitorias_j2 > vitorias_j1:
            vencedor = f"{jogador2.name} venceu a batalha"

        else:
            vencedor = "Batalha empatada"

        resultado = "\n".join(rodadas)

        return f"{resultado}\n{vencedor}"